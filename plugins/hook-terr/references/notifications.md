# Notifications

`hook-terr` 支持四类通知器：`sound`、`windows_toast`、`popup`、`custom_command`。

默认 Stop 自检规则不执行外部通知；只有启用 `notify` 的规则才会调用通知器。通知失败 fail open，不会阻断 Claude Code 主流程，但简要诊断会追加到 hook `systemMessage`。

## sound

Windows 下播放 `.wav` 提示音。默认使用 `C:\\Windows\\Media\\tada.wav`。

`/hook-terr:sound` 支持两种路径：

- `Use default`：跳过试听，直接保存默认 `tada.wav`。
- `Open picker`：打开外部 PowerShell 试听菜单，用户试听后把 id、alias 或 wavPath 回填给 Claude Code，再写入全局 settings。

外部 picker 只负责试听和输出选择，不直接修改 settings。

## windows_toast

Windows 下显示 tray balloon 通知。默认可用，但不会由默认 Stop 自检规则触发。启用 notify 的规则可通过 `/hook-terr:configure` 或 settings 覆盖选择该通道。

实现要求：hook 将通知脚本写入临时 `.ps1`，再通过 `cmd.exe /c start powershell.exe -STA -File ...` 启动独立通知进程并立即返回，避免 Claude Code 清理 Stop hook 子进程时中断通知。通知进程会同时投递 WinRT `ToastNotificationManager` 和 `System.Windows.Forms.NotifyIcon` tray balloon；后者使用 `ApplicationContext` message loop 保活。`timeoutMs` 会限制在 5–30 秒之间。设置 `HOOK_TERR_WINDOWS_TOAST_LOG` 时会把 WinRT/NotifyIcon 投递路径写入该日志。

## popup

结构化弹窗，支持标题、正文和图标。默认通道配置中可用，但不会由默认 Stop 自检规则触发。实现必须非阻塞：hook 只启动弹窗进程，不等待用户关闭。

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
- 优先使用 detached 模式，避免阻塞 hook。
