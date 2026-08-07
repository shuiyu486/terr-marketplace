# Notifications

`hook-terr` 支持四类通知器：`sound`、`windows_toast`、`popup`、`custom_command`。

默认普通 Stop 不返回自检 `systemMessage`，也不执行外部通知；Stop 外部通知需要启用 `notify` 的规则，且 runtime 护栏只允许主会话 Stop 触发。由于 Claude Code 的 Stop 表示一次响应结束而非所有工作完成，runtime 优先读取 Stop payload 的实时 `background_tasks` 和 `session_crons`；任一非空时都会抑制外部通知，覆盖运行中 Agent/命令/Workflow，以及 `ScheduleWakeup`、`CronCreate`、`/loop` 等已安排自动续跑。旧版 payload 缺少 `background_tasks` 时，runtime 才从主会话 `transcript_path` 兼容追踪实际异步结果、恢复后的 Agent、成功 `TaskStop` 和 `<task-notification>` 终态；transcript 无法读取时 fail open。Claude task todo 的 `pending` / `in_progress` 只表示工作清单，可能跨会话保留，不参与完成音护栏，避免陈旧 backlog 导致永久静音。持续运行的后台开发服务器仍属于 `background_tasks`，会继续抑制完成音，直到任务自然终止或被成功 `TaskStop`；runtime 无法可靠区分“任务依赖的后台工作”和“用户有意常驻的服务”。主会话 `AskUserQuestion` 求助场景会有意复用 Stop 通道，因此仍会播放同一提示音，但语义是“等待用户输入”而非“任务完成”。通知失败 fail open，不会阻断 Claude Code 主流程；普通规则通知诊断会追加到 hook `systemMessage`，求助通知诊断只写入 stderr。

## sound

Windows 下播放 `.wav` 提示音。默认使用 `C:\\Windows\\Media\\tada.wav`。

`/hook-terr:sound` 支持两种路径：

- `Use default`：跳过试听，直接保存默认 `tada.wav`。
- `Open picker`：打开外部 PowerShell 试听菜单，用户试听后把 id、alias 或 wavPath 回填给 Claude Code，再写入全局 settings。

外部 picker 只负责试听和输出选择，不直接修改 settings。

## windows_toast

Windows 下优先显示 WinRT toast；仅在非静音模式且 WinRT 投递失败时，回退到 `System.Windows.Forms.NotifyIcon` tray balloon。默认可用，但不会由内置默认 stop-notify 规则触发。启用 notify 的规则可通过 `/hook-terr:configure` 或 settings 覆盖选择该通道。

实现要求：hook 将通知脚本写入临时 `.ps1`，再通过系统目录中的绝对 `powershell.exe` 路径直接启动 detached 进程并立即返回，不经过 `cmd.exe` 二次解析临时路径，也不从项目 cwd 搜索同名可执行文件。`silent=true` 会给 WinRT toast 写入静音 audio 配置；由于 NotifyIcon 不能保证静音，静音模式下 WinRT 失败时不再回退。非静音模式的 NotifyIcon fallback 使用 `ApplicationContext` message loop 保活。`timeoutMs` 会限制在 5–30 秒之间。设置 `HOOK_TERR_WINDOWS_TOAST_LOG` 时会把投递或失败路径写入该日志。

## popup

结构化弹窗，支持标题、正文和图标。默认通道配置中可用，但不会由内置默认 stop-notify 规则触发。实现必须非阻塞：hook 只启动弹窗进程，不等待用户关闭；MessageBox 由用户手动关闭，不支持 `timeoutMs`。

## custom_command

高级自定义命令，默认关闭。启用后等价于执行本机命令。

动态值只通过环境变量提供，避免把消息内容拼进 shell/PowerShell 命令源码：

- `HOOK_TERR_EVENT`
- `HOOK_TERR_TITLE`
- `HOOK_TERR_MESSAGE`
- `HOOK_TERR_CWD`
- `HOOK_TERR_TIMESTAMP`

Windows PowerShell 示例：

```powershell
Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show($env:HOOK_TERR_MESSAGE, $env:HOOK_TERR_TITLE) | Out-Null
```

sh/bash 示例：

```sh
notify-send "$HOOK_TERR_TITLE" "$HOOK_TERR_MESSAGE"
```

旧 `custom_command.command` 模板变量已移除，settings 加载阶段会报诊断并跳过该配置层：

- `{{event}}` → `HOOK_TERR_EVENT`
- `{{title}}` → `HOOK_TERR_TITLE`
- `{{message}}` → `HOOK_TERR_MESSAGE`
- `{{cwd}}` → `HOOK_TERR_CWD`
- `{{timestamp}}` → `HOOK_TERR_TIMESTAMP`

安全边界：

- 只配置可信命令。
- 必须使用 `HOOK_TERR_*` 环境变量传递动态值；不要把动态内容拼入 shell 字符串或 PowerShell 字符串。
- 命令 stdout/stderr 必须与 hook stdout 隔离。
- 优先使用 detached 模式，避免阻塞 hook；POSIX detached 会创建独立 session。
- attached 模式会检查退出码，并在 `timeoutMs` 到期时终止并回收进程树；Windows 使用系统目录中的 `taskkill.exe /T /F` 清理后代进程，系统 PowerShell 也始终从可信系统目录启动。
