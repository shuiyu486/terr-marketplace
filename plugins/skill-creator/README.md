# skill-creator

Claude Code skill 全生命周期管理工具。创建、修改、修复、评估和优化 skills。

## 功能

- **从零创建 skill**：通过结构化访谈捕获意图，编写 SKILL.md
- **迭代改进**：基于用户反馈和定量评估持续优化
- **运行 evals**：创建测试用例，批量运行并查看结果
- **基准测试 (benchmark)**：方差分析，盲比评估
- **触发优化**：分析并优化 skill 的 description 以提高触发准确率
- **子代理**：内置 analyzer、comparator、grader 等子代理辅助评估

## 工作流程

```
捕获意图 → 访谈调研 → 编写 SKILL.md → 创建测试用例 → 
运行 evals → 评估结果 → 迭代改进 → 触发优化
```

## 使用方式

安装后，在 Claude Code 中表达 skill 相关需求即可触发：

- `帮我创建一个 skill` — 启动创建流程
- `修改我的 skill` — 进入改进循环
- `运行 skill evals` — 批量测试评估
- `优化 skill 触发` — 改进 description 触发准确率

## 结构

```
skill-creator/
├── .claude-plugin/plugin.json
├── skills/skill-creator/
│   ├── SKILL.md                    # Skill 定义
│   ├── agents/                     # 子代理（analyzer, comparator, grader）
│   ├── eval-viewer/                # 评估结果查看器
│   ├── assets/                     # eval 模板
│   ├── references/                 # 参考文档
│   └── scripts/                    # 自动化脚本
│       ├── aggregate_evals.py
│       ├── generate_test_cases.py
│       ├── improve_description.py
│       ├── package_skill.py
│       ├── quick_validate.py
│       ├── run_evals.py
│       └── run_eval_variance.py
└── README.md
```

## 来源

基于 Anthropic 官方 [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) 的 skill-creator。
