# 方向 1：本地 → 项目（local → ccNovaTerm）

用户说"同步到项目"、"push"、"更新模板"时触发。将本地配置变更推送到 ccNovaTerm 仓库。

**完全无需用户手动克隆项目。** 如果本地没有 clone，自动在临时目录 clone、提交、推送后清理。

## 第一步：准备模板化的本地配置

1. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
2. **读取本地文件** — 用 UTF-8 编码读取配置文件。**跳过文件级排除的文件**（`Test-FileExcluded` 返回 `$true` 的文件不参与后续步骤）
3. **检测系统特定值** — 自动识别：
   - nu.exe 路径（`Get-Command nu.exe` → `~\AppData\Local\Programs\nu\bin\nu.exe` → `${env:ProgramFiles}\nu\bin\nu.exe`）
   - Git usr/bin 路径（从 `git.exe` 推断 → `C:\Program Files\Git\usr\bin`）
   - 用户名（`$env:USERNAME`）
4. **生成模板** — 将系统值替换为占位符：
   - nu.exe 完整路径 → `__NU_PATH__`
   - Git usr/bin 路径 → `__GIT_USR_BIN__`
   - 用户名 → `__USERNAME__`
   - `load-env { http_proxy: ... }` → 注释掉（如 `# load-env { http_proxy: "http://127.0.0.1:7890", https_proxy: "http://127.0.0.1:7890" }`）
   - `settings.json`：只取 `statusLine` 字段，不包含 API key 等敏感信息
   - `.wezterm.lua`：`config.default_prog` 用操作系统检测包裹（如模板已有则保持）

## 第二步：展示差异并确认

1. **获取远程基准** — 如第零步 0b 无本地项目，执行 0c 远程获取模板到缓存
2. **对比差异** — 将模板化后的本地内容与远程基准逐文件对比（settings.json 只比较 statusLine 字段）。**不包含文件级排除的文件**
3. **无变更则终止** — 如果所有文件与远程一致，告知用户"本地配置与项目模板完全一致，无需推送"，不执行任何写入操作
4. **展示变更清单** — 列出哪些文件有变更、变更内容概要。**单独列出被排除规则跳过的文件**
5. **请求确认** — 向用户展示变更摘要并询问是否继续推送。**必须获得用户明确同意才能执行推送**（涉及远程仓库写入）

## 第三步：推送变更

推送前检查 git 是否可用：

```powershell
$gitOk = $true
try { $null = Get-Command git.exe -ErrorAction Stop } catch {
    Write-Output "未检测到 git。请安装 Git for Windows 后再执行同步到项目。"
    $gitOk = $false
}
```

根据第零步结果选择路径：

### 路径 A：本地项目存在（0b 成功）

直接在本地项目上操作：

```powershell
# 1. 写入模板化后的文件到 $configDir（UTF-8 无 BOM）
foreach ($f in $changedFiles) {
    [System.IO.File]::WriteAllText("$configDir\$f", $templatedContent, [System.Text.Encoding]::UTF8)
}

# 2. 提交并推送
git -C $repoRoot add config/
git -C $repoRoot commit -m "<生成的提交信息>"
git -C $repoRoot push
```

### 路径 B：无本地项目（通过临时 clone）

```powershell
$tmpDir = "$env:TEMP\ccNovaTerm-push-$((Get-Date -Format 'yyyyMMddHHmmss'))"

# 1. 浅克隆（节省时间，只取最新提交）
git clone --depth 1 $repoUrl $tmpDir

# 2. 写入模板化后的文件（UTF-8 无 BOM）
foreach ($f in $changedFiles) {
    [System.IO.File]::WriteAllText("$tmpDir\config\$f", $templatedContent, [System.Text.Encoding]::UTF8)
}

# 3. 提交
git -C $tmpDir add config/
git -C $tmpDir commit -m "<生成的提交信息>"

# 4. 推送（需用户已配置 git 凭据）
git -C $tmpDir push

# 5. 清理临时目录
Remove-Item -Recurse -Force $tmpDir
```

**提交信息格式** — 简洁描述变更内容：
```
sync: update <文件1>, <文件2> from local environment

- .wezterm.lua: update default_prog path
- starship.toml: adjust <具体变更>
```

**git push 失败处理** — 如果 push 失败（凭据未配置、无权限等）：
- 临时目录保留不删除，告知用户路径
- 提示用户可以手动进入目录执行 `git push`
- 或提供 `gh auth login` / SSH key 配置指引

## 第四步：报告结果

- 列出成功推送的文件
- 列出被排除规则跳过的文件
- 临时 clone 是否已清理（路径 B）
- 如果是本地项目，提醒可能需要更新 README 等文档
