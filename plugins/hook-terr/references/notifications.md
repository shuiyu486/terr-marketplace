# Notifications

`hook-terr` 支持四类通知器：`sound`、`windows_toast`、`popup`、`custom_command`。

默认 Stop 通道是 `sound + popup`。通知失败 fail open，不会阻断 Claude Code 主流程，但简要诊断会追加到 hook `systemMessage`。

## sound

Windows 下播放 `.wav` 提示音。默认使用 `C:\\Windows\\Media\\tada.wav`。

`/hook-terr:sound` 支持两种路径：

- `Use default`：跳过试听，直接保存默认 `tada.wav`。
- `Open picker`：打开外部 PowerShell 试听菜单，用户试听后把 id、alias 或 wavPath 回填给 Claude Code，再写入全局 settings。

外部 picker 只负责试听和输出选择，不直接修改 settings。

## windows_toast

Windows 下显示 tray balloon 通知。默认可用，但不再作为 Stop 默认通道。可通过 `/hook-terr:configure` 或 settings 覆盖启用到 Stop 通道。

## popup

结构化弹窗，支持标题、正文和图标。默认作为 Stop 通道启用。实现必须非阻塞：hook 只启动弹窗进程，不等待用户关闭。

## custom_command

高级自定义命令，默认关闭。启用后等价于执行本机命令。

允许模板变量：

- `{{event}}`
- `{{title}}`
- `{{message}}`
- `{{cwd}}`
- `{{timestamp}}`

安全边界：

- 只配置可信命令。
- 不要拼接未信任输入。
- 命令 stdout/stderr 必须与 hook stdout 隔离。
- 优先使用 detached 模式，避免阻塞 hook。
