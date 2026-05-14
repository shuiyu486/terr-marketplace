---
name: skills2ccPlugin
description: >-
  将 skill 转换为 terr-marketplace 可安装插件。当用户想把 skill 发布到 marketplace，
  将 skill-creator 的输出打包为插件，或提到"发布 skill"、"打包插件"、"注册到 marketplace"、
  "让 skill 能通过 /plugin install 安装"时使用。即使措辞不同（"上线"、"分享"、"分发"），
  只要意图是将 skill 变成 marketplace 中的可安装单元，就应该触发。
---

# skills2ccPlugin

将一个 skill 目录转换为 terr-marketplace 插件。读取 SKILL.md 元数据，
生成 plugin.json，组织目录结构，注册 marketplace.json（git-subdir），验证。

## 重要前提

- marketplace 仓库路径：先用 `$env:USERPROFILE\.claude\plugins\marketplaces\terr-marketplace`，若不存在再尝试 `C:\AI\m_projects\m_agents\terr-marketplace`
- 所有插件使用 **git-subdir** source 格式，否则用户安装时需 `--sparse` 参数
- 插件目录固定为 `plugins/<name>/`，skill 内容放在 `plugins/<name>/skills/<name>/`

## 目标目录结构

源 skill（由 skill-creator 生成，可能包含多种资源目录）：
```
skills/<name>/
├── SKILL.md            ← 必须
├── references/         ← 可选：参考文档
├── scripts/            ← 可选：可执行脚本
├── agents/             ← 可选：子代理指令（grader、comparator 等）
├── assets/             ← 可选：模板、静态资源（HTML 模板等）
├── eval-viewer/        ← 可选：评估查看器（generate_review.py 等）
└── ...                 ← 可选：其他自定义资源目录
```

转换为 marketplace 插件后：
```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json           ← 新建
└── skills/
    └── <name>/
        ├── SKILL.md           ← 从源 skill 复制
        ├── references/        ← 若存在则复制
        ├── scripts/           ← 若存在则复制
        ├── agents/            ← 若存在则复制
        ├── assets/            ← 若存在则复制
        ├── eval-viewer/       ← 若存在则复制
        └── ...                ← 其他任何子目录均复制
```

**关键原则**：源 skill 的所有文件和子目录都要复制到 `skills/<name>/` 下，不仅限于 `references/` 和 `scripts/`。skill 内部引用哪个目录，哪个目录就必须带上。漏掉一个目录，skill 运行时引用它就会失败。

## 操作流程

### 1. 提取元数据

读取源 skill 的 `SKILL.md` YAML frontmatter，提取 `name` 和 `description`。
向用户确认 version（默认 1.0.0）、author、license（默认 MIT）、keywords。

### 2. 创建 plugin.json

```json
{
  "name": "<name>",
  "version": "1.0.0",
  "description": "<description>",
  "author": { "name": "<author>" },
  "license": "MIT",
  "keywords": ["<kw1>", "<kw2>"]
}
```

### 3. 组织文件

**第一步：确定 marketplace 路径并创建目标目录**

```powershell
$marketplace = if (Test-Path "$env:USERPROFILE\.claude\plugins\marketplaces\terr-marketplace") {
    "$env:USERPROFILE\.claude\plugins\marketplaces\terr-marketplace"
} else {
    "C:\AI\m_projects\m_agents\terr-marketplace"
}
$target = "$marketplace\plugins\<name>"
New-Item -ItemType Directory -Force "$target\.claude-plugin" | Out-Null
```

**第二步：复制所有源 skill 文件和子目录**

关键规则：**复制源 skill 目录下的每一个子目录，不管它叫什么名字。** 不同 skill 有不同的资源目录组合——`agents/`、`assets/`、`eval-viewer/` 和任何自定义目录都是合法的。只要目录存在就复制，不要按名称筛选。

```powershell
# 复制目标 skill 子目录
$targetSkill = "$target\skills\<name>"
New-Item -ItemType Directory -Force $targetSkill | Out-Null

# 复制 SKILL.md（必须存在）
Copy-Item "<源-skill-路径>\SKILL.md" $targetSkill -Force

# 复制所有子目录（存在则复制，不存在则跳过）
$subdirs = @("references", "scripts", "agents", "assets", "eval-viewer")
foreach ($d in $subdirs) {
    $src = "<源-skill-路径>\$d"
    if (Test-Path $src) {
        Copy-Item $src "$targetSkill\$d" -Recurse -Force
    }
}

# 兜底：复制任何上面未列出的其他子目录（如 LICENSE.txt 等根级文件）
Get-ChildItem "<源-skill-路径>" -Directory | ForEach-Object {
    if ($_.Name -notin $subdirs -and -not (Test-Path "$targetSkill\$($_.Name)")) {
        Copy-Item $_.FullName "$targetSkill\$($_.Name)" -Recurse -Force
    }
}
```

**第三步：验证复制结果**

```powershell
Get-ChildItem $targetSkill -Recurse -File | ForEach-Object { $_.FullName }
```

确认所有预期的文件和目录都在 `skills/<name>/` 下。`<name>` 必须与 plugin name 完全一致。

### 4. 注册 marketplace.json

在 `.claude-plugin/marketplace.json` 的 `plugins` 数组末尾追加。
**必须用 git-subdir 格式**——它让每个插件独立从 GitHub 稀疏克隆子目录，
用户添加 marketplace 时无需 `--sparse` 参数：

```json
{
  "name": "<name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<name>"
  },
  "description": "<description>",
  "version": "1.0.0",
  "author": { "name": "<author>" },
  "license": "MIT",
  "keywords": ["<kw1>", "<kw2>"]
}
```

**关键**：不要修改已有条目。确保插入后的 JSON 仍合法（逗号位置、括号闭合）。

### 5. 验证

```powershell
claude plugin validate $marketplace
```

验证失败则修复后重试，不要跳过。

### 6. 提交推送

```powershell
cd $marketplace
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Add <name> plugin v<version>"
git push
```

## 边界情况

- 若 `plugins/<name>/` 已存在，询问用户是覆盖还是跳过
- 若源 skill 缺少某个子目录（references/、scripts/、agents/ 等），跳过该目录即可，不影响其他目录的复制
- 源 skill 可能有任意子目录组合，全都复制——不按目录名筛选
- plugin name 在整个 marketplace 中必须唯一
- 不要修改 marketplace.json 中已有的其他 `plugins` 条目
