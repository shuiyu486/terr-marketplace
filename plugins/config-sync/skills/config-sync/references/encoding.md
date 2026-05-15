# 编码安全参考

## 编码要求（关键！）

**所有配置文件的读写必须使用 UTF-8 编码，读取和写入都要显式指定。** 在中文 Windows 上，PowerShell 5.1 的 `Get-Content` 和 `Set-Content` 默认使用 GBK 编码。用 GBK 读取 UTF-8 文件会将 Nerd Font PUA 字符（3 字节 UTF-8）错误解释为 CJK 字符，之后再写入时永久损坏。

`starship.toml` 包含 Nerd Font 私有区（PUA）Unicode 字符（如 `` U+E0B6、`` U+E0B0、`󰈙` U+F0219 等）。这些字符在 GBK 编码下无对应映射，会被拆成 2-3 个 CJK 字符（`顐` `禲` `癩` 等）。

**必须使用以下 API（避开 PowerShell 默认编码陷阱）：**

读取文件：
```powershell
# 方法 1（推荐）— .NET UTF8，无 BOM 问题
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# 方法 2 — PowerShell，但必须显式指定 UTF8
$content = Get-Content $path -Raw -Encoding UTF8
```

写入文件：
```powershell
# 唯一推荐方法 — .NET UTF8Encoding($false)，不写 BOM（关键！）
# 注意：[System.Text.Encoding]::UTF8 在 .NET Framework 中默认写入 BOM！
# 必须使用 New-Object System.Text.UTF8Encoding $false
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $content, $utf8NoBom)

# 定义 helper 以便复用：
function Write-FileUtf8NoBom([string]$Path, [string]$Content) {
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}
```

**绝对禁止 `Set-Content -Encoding UTF8`** —— PS5.1 会在文件头添加 BOM（字节 EF BB BF）。`config.nu` 开头的 BOM 字符 `﻿` 会被拼接到第一个语句前，导致 Nushell 静默跳过整个文件的 alias 解析（`scope aliases` 返回空列表，`cc` 别名失效）。`starship.toml` 的 BOM 虽不致命但也不规范。

**禁止使用**：任何不带 `-Encoding UTF8` 的 `Get-Content` / `Set-Content`（默认 GBK）、`Out-File`、`>` 重定向（默认 UTF-16 LE 或 GBK）、`Set-Content -Encoding UTF8`（BOM 隐患）。

## 远程获取编码安全

`Invoke-WebRequest` 返回的 `.Content` 属性已经过 PowerShell 的文本解码，可能引入编码问题。用 `.RawContentStream` 或直接使用 `[System.Net.WebClient]` 获取原始字节更安全：

```powershell
$wc = New-Object System.Net.WebClient
$bytes = $wc.DownloadData($url)
[System.IO.File]::WriteAllBytes("$cacheDir\$f", $bytes)
```

## Starship.toml 特殊保护

同步前后用以下方法快速检查编码是否损坏：

```powershell
$t = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($path))
if ($t.Contains('顐') -or $t.Contains('禲') -or $t.Contains('癩')) {
    # 编码已损坏！从备份恢复并用 .NET UTF8 重写
}
```
