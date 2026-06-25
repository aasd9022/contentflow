---
name: "article-gen-skill"
description: "基于已收集的文章信息（主题、受众、风格、长度、要点），利用AI模型生成完整的高质量文章内容，并支持大纲预览与全文生成。Invoke when user has completed info collection and is ready to generate the article body."
---

# Article Gen Skill - 文章生成

## 功能描述

本Skill作为工作流的**第二阶段**，负责基于 Skill 1 收集的文章信息，调用AI模型生成符合要求的完整文章。支持**大纲预览 → 内容迭代 → 全文输出**的工作模式。

## 触发条件

当以下条件满足时触发：
- Skill 1 (ask-info-skill) 已生成 `article-info-*.json` 文件
- 用户明确表达"开始生成文章"或"写文章"
- 提供了文章信息参数

## 三层结构

```
2.article-gen-skill/
├── SKILL.md              # 本文件 - Skill说明
├── references/           # 参考资料
│   ├── style-guide.md    # 风格指南
│   └── prompt-templates.md  # Prompt模板
└── scripts/              # 脚本工具
    ├── gen-outline.py    # 大纲生成脚本
    ├── gen-article.py    # 文章生成脚本
    └── md-to-json.py     # 格式转换脚本
```

## 使用方法

### 1. 读取文章信息

```bash
python scripts/gen-outline.py --input ../data/article-info-xxx.json
```

**输入**：Skill 1 生成的 JSON 文件
**输出**：结构化大纲（Markdown 格式）

### 2. 大纲预览与确认

```markdown
# 📑 文章大纲

## 标题
[主标题 + 副标题]

## 引言 (约200字)
- 背景引入
- 核心问题提出

## 第一部分：xxx
### 1.1 子主题
- 要点1
- 要点2

## 第二部分：xxx
...

## 结论 (约200字)
- 核心观点总结
- 行动建议
```

**确认方式**：
```
✅ 确认大纲 → 进入全文生成
🔄 修改大纲 → 提供修改意见
❌ 重新开始 → 回到Skill 1
```

### 3. 全文生成

```bash
python scripts/gen-article.py --info data/article-info.json --outline data/outline.md --output data/article.md
```

**输出**：
```
skill-workflow/
└── data/
    ├── article-info-xxx.json     # 输入
    ├── outline-xxx.md            # 中间产物
    └── article-xxx.md            # 最终文章
```

## 核心参数

| 参数 | 说明 | 来源 |
|-----|------|------|
| topic | 文章主题 | info |
| audience | 目标受众 | info |
| style | 写作风格 | info |
| length | 字数范围 | info |
| key_points | 核心要点 | info |
| outline | 文章大纲 | 自动生成 |
| tone | 语气强度 | 自动推断 |

## 风格映射

不同风格对应不同的Prompt策略：

| 风格 | 关键词 | 句式特点 | 段落结构 |
|-----|-------|---------|---------|
| 专业严谨 | 学术、技术 | 复合句、专业术语 | 总分总、层层递进 |
| 通俗易懂 | 科普、生活 | 短句、比喻 | 故事引入 → 解释 → 举例 |
| 故事化叙事 | 案例、人物 | 场景描写 | 时间线、冲突-解决 |
| 观点评论 | 时评、分析 | 反问、对比 | 观点 → 论据 → 论证 |
| 教程指南 | 步骤、操作 | 祈使句、列表 | 准备 → 步骤 → 总结 |

## 调用方式

```bash
# 方式1：通过Skill工具
Skill: article-gen-skill

# 方式2：直接传参
"使用 article-gen-skill，基于 data/article-info-xxx.json 生成文章"
```

## 输出格式

生成的Markdown文件包含：
- **YAML Front Matter**：元数据（标题、日期、标签、摘要）
- **正文**：完整的Markdown内容
- **字数统计**：自动统计实际字数
- **SEO 信息**：关键词、描述

### 示例输出
```markdown
---
title: "AI在医疗健康领域的应用与未来"
date: 2026-06-25
tags: [AI, 医疗, 健康]
description: "探讨人工智能如何改变传统医疗健康行业..."
keywords: ["人工智能", "医疗", "数字化"]
---

# AI在医疗健康领域的应用与未来

> 本文约 1850 字，阅读时间约 6 分钟

## 引言

在数字化浪潮的推动下，...

## 第一部分：技术原理

...
```

## 与其他Skill的协作

- **上游Skill**：`1.ask-info-skill`（信息收集）
- **下游Skill**：`3.slides-html-skill`（HTML幻灯片）
- **数据流**：`article-info.json` → `outline.md` → `article.md` → `slides.html`

## 最佳实践

1. **先生成大纲**：避免直接生成全文导致内容偏离
2. **允许迭代修改**：用户可以对大纲和文章提出修改意见
3. **控制字数**：根据 `length` 参数严格控制输出长度
4. **保留要点**：确保 `key_points` 中的每个要点都有体现
5. **风格一致**：整篇文章保持统一的语气和风格
6. **生成摘要**：自动生成150字以内的文章摘要

## 错误处理

| 错误场景 | 应对策略 |
|---------|---------|
| 找不到 info 文件 | 提示用户先运行 Skill 1 |
| 字数严重不足 | 提示用户扩展 `key_points` 或调整 `length` |
| 风格不符合 | 重新生成或提供风格参考样例 |
| 关键要点缺失 | 检查大纲是否覆盖所有 `key_points` |
