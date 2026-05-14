# Marketplace.json 插件条目模板

## git-subdir 格式（唯一使用格式）

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<plugin-name>"
  },
  "description": "<插件描述>",
  "version": "1.0.0",
  "author": { "name": "<作者名>" },
  "license": "MIT",
  "keywords": ["<关键词>"]
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 插件名，与 plugin.json 中的 name 一致 |
| `source.source` | 是 | 固定为 `"git-subdir"` |
| `source.url` | 是 | 固定为 `https://github.com/shuiyu486/terr-marketplace.git` |
| `source.path` | 是 | 子目录路径，`plugins/<name>` |
| `description` | 是 | 简短描述，从 SKILL.md frontmatter 提取 |
| `version` | 是 | 语义化版本号 |
| `author` | 否 | 作者信息对象 |
| `license` | 否 | 许可证标识符 |
| `keywords` | 否 | 关键词数组，用于搜索 |
| `repository` | 否 | 关联的源码仓库 URL |
| `homepage` | 否 | 项目主页 URL |
| `category` | 否 | 分类：development / productivity / security / learning |

## marketplace.json 完整结构

```json
{
  "name": "terr-marketplace",
  "owner": { "name": "terrapin" },
  "description": "Terr 的 Claude Code 插件集合",
  "version": "1.0.0",
  "plugins": [
    // ... 插件条目按此模板逐个添加
  ]
}
```
