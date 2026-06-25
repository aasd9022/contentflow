---
name: "content-workflow"
description: "一站式内容生产工作流，整合信息收集、文章生成、HTML幻灯片和网站发布四大阶段。Invoke when user wants to create and publish complete content including articles and slides."
---

# Content Workflow Skill - 内容生产工作流

## 功能描述

本Skill是内容生产的**总入口**，整合了四大核心Skill，形成完整的端到端内容生产流水线：

```
信息收集 → 文章生成 → 幻灯片生成 → 网站发布
```

只需一个命令，即可完成从需求收集到网站发布的全流程。

## 触发条件

当用户表达以下意图时触发：
- "帮我写一篇文章并发布"
- "生成一篇关于xxx的内容"
- "创建幻灯片并发布到网站"
- "启动内容工作流"

## 工作流架构

### 五大阶段

| 阶段 | Skill | 输入 | 输出 |
|-----|-------|------|------|
| **1. 信息收集** | ask-info-skill | 用户对话 | `article-info.json` |
| **2. 文章生成** | article-gen-skill | `article-info.json` | `article.md` + `article-structured.json` |
| **3. 幻灯片** | slides-html-skill | `article-structured.json` | `slides.html` |
| **4. 网站发布** | website-publish-skill | `.md` + `.html` | 发布到 Hugo 网站 |
| **5. 设计风格** | design-style-skill | 风格选择/Design Token | 设计规范 → 注入CSS |

### 可配置选项

- **跳过幻灯片**：`--skip-slides`
- **跳过发布**：`--skip-publish`
- **指定主题**：`--theme modern/classic/gradient/minimal/dark`
- **指定网站路径**：`--site-path /path/to/hugo`
- **从中间阶段开始**：`--from-info` / `--from-article` / `--from-slides`

## 三层结构

```
skill-workflow/
├── SKILL.md                    # 本文件（总入口说明）
├── workflow.py                 # 工作流主脚本
│
├── 1.ask-info-skill/           # Skill 1: 信息收集
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── 2.article-gen-skill/        # Skill 2: 文章生成
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── 3.slides-html-skill/        # Skill 3: 幻灯片
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
├── 4.website-publish-skill/    # Skill 4: 网站发布
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
│
└── data/                       # 工作流数据目录（自动创建）
    ├── article-info-*.json
    ├── outline-*.md
    ├── article-*.md
    ├── article-structured-*.json
    └── slides-*.html
```

## 使用方法

### 快速开始

```bash
# 交互式完整流程
python workflow.py

# 快速生成（指定所有参数）
python workflow.py \
  --topic "AI在医疗健康领域的应用" \
  --audience "产品经理和技术决策者" \
  --style "专业严谨" \
  --length "1500-2000字" \
  --key-points "技术原理,应用场景,未来趋势,挑战与机遇"

# 只生成文章，不做幻灯片和发布
python workflow.py --topic "xxx" --skip-slides --skip-publish

# 指定幻灯片主题
python workflow.py --topic "xxx" --theme gradient

# 从已有信息文件开始
python workflow.py --from-info data/article-info-xxx.json
```

### 常用组合

| 场景 | 命令 |
|-----|------|
| 完整流程（交互） | `python workflow.py` |
| 完整流程（快速） | `python workflow.py --topic ... --style ...` |
| 仅文章 | `--skip-slides --skip-publish` |
| 文章+幻灯片 | `--skip-publish` |
| 仅发布 | `--publish-only --from-article xxx.md` |

## 输出文件说明

所有输出文件都保存在 `data/` 目录下：

| 文件 | 说明 | 产生阶段 |
|-----|------|---------|
| `article-info-*.json` | 文章信息JSON | 阶段1 |
| `outline-*.md` | 文章大纲 | 阶段2 |
| `article-*.md` | 完整文章 | 阶段2 |
| `article-structured-*.json` | 结构化JSON | 阶段2 |
| `slides-*.html` | HTML幻灯片 | 阶段3 |

## 与其他Skill的关系

本Skill是**总调度器**，负责：
- 协调四个子Skill的执行顺序
- 处理阶段间的数据传递
- 处理跳过/断点续跑等流程控制
- 统一的输出和错误处理

四个子Skill也可以**独立调用**，见各自的 SKILL.md。

## 最佳实践

1. **先用交互模式试一次**：了解完整流程
2. **再用参数模式批量生产**：提高效率
3. **大纲确认后再生成全文**：减少返工
4. **本地预览后再发布**：确保质量
5. **使用版本控制**：跟踪内容变更

## 常见问题

### Q: 可以只运行部分阶段吗？
A: 可以，使用 `--skip-slides`、`--skip-publish` 或 `--from-*` 参数。

### Q: 生成的文件在哪里？
A: 所有文件都在 `data/` 目录下，按时间排序，最新的在最前面。

### Q: 支持哪些幻灯片主题？
A: 5种：modern（现代）、classic（经典）、gradient（渐变）、minimal（极简）、dark（暗色）。

### Q: 支持哪些网站系统？
A: 当前主要支持 Hugo 静态网站，自动检测结构。其他系统可通过 `--site-path` 指定。
