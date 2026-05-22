# Notifications

`hook-terr` 支持四类通知器：`beep`、`windows_toast`、`popup`、`custom_command`。

## beep

Windows 下播放短提示音。默认启用。不要用于长时间循环或外部音频文件。

## windows_toast

Windows 下显示 tray balloon 通知。默认静音，由 `beep` 负责声音，避免重复打扰。

## popup

结构化弹窗，支持标题、正文和图标。默认关闭。实现必须非阻塞：hook 只启动弹窗进程，不等待用户关闭。

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
