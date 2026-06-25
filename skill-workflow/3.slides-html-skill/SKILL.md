---
name: "slides-html-skill"
description: "将结构化文章内容转换为精美的HTML幻灯片，支持多种主题、响应式布局和键盘导航。Invoke when article generation is complete and user wants to create presentation slides from the content."
---

# Slides HTML Skill - HTML幻灯片生成

## 功能描述

本Skill作为工作流的**第三阶段**，负责将 Skill 2 生成的结构化文章 JSON 转换为美观、可交互的 HTML 幻灯片。支持多种主题风格、响应式布局、键盘导航、全屏演示等功能。

## 触发条件

当以下条件满足时触发：
- Skill 2 (article-gen-skill) 已生成 `article-structured-*.json` 文件
- 用户明确表达"生成幻灯片"、"做PPT"、"转演示文稿"
- 文章内容已完成并确认无误

## 三层结构

```
3.slides-html-skill/
├── SKILL.md              # 本文件 - Skill说明
├── references/           # 参考资料
│   ├── slide-templates.md    # 幻灯片模板
│   └── css-themes.md         # 主题样式说明
└── scripts/              # 脚本工具
    ├── gen-slides.py         # 幻灯片生成主脚本
    └── html-templates.py     # HTML模板库
```

## 使用方法

### 1. 读取结构化文章

```bash
python scripts/gen-slides.py --input ../data/article-structured-xxx.json
```

**输入**：Skill 2 生成的结构化 JSON
**输出**：单文件 HTML 幻灯片

### 2. 主题选择

| 主题 | 风格 | 适用场景 |
|-----|------|---------|
| `modern` | 现代简约 | 科技产品、商务演示 |
| `classic` | 经典正式 | 学术报告、会议演讲 |
| `gradient` | 渐变活力 | 创意设计、营销推广 |
| `minimal` | 极简留白 | 艺术摄影、个人展示 |
| `dark` | 暗色模式 | 技术分享、夜间演示 |

```bash
python scripts/gen-slides.py --input data.json --theme gradient
```

### 3. 幻灯片结构

每篇文章自动生成以下幻灯片页：

```
Slide 1: 封面页（标题+副标题+作者+日期）
Slide 2: 目录页（章节导航）
Slide 3+: 每个章节1-2页（根据内容自动拆分）
Last Slide: 总结页 + Q&A页
```

### 4. 输出文件

```
skill-workflow/
└── data/
    ├── article-structured-xxx.json     # 输入
    └── slides-xxx.html                 # 输出：单文件HTML
```

## 幻灯片特性

### 交互功能
- **键盘导航**：← → 键翻页，F 全屏，ESC 退出
- **进度条**：顶部显示当前进度
- **页码显示**：当前页 / 总页数
- **目录跳转**：点击目录快速跳转

### 视觉效果
- **平滑过渡**：幻灯片切换动画
- **渐变背景**：根据主题自动配色
- **响应式**：适配桌面、平板、手机
- **打印友好**：支持打印为PDF

### 代码高亮
- 内置代码高亮支持
- 自动识别编程语言
- 行号显示

## 调用方式

```bash
# 基本使用
python scripts/gen-slides.py -i data/article-structured-xxx.json

# 指定主题
python scripts/gen-slides.py -i data.json --theme dark

# 自定义输出路径
python scripts/gen-slides.py -i data.json -o output/slides.html

# 查看所有选项
python scripts/gen-slides.py --help
```

## 幻灯片内容布局规则

| 内容类型 | 布局方式 | 字号比例 |
|---------|---------|---------|
| 章节标题 | 居中大字 | 100% |
| 要点列表 | 左对齐列表 | 60% |
| 段落文字 | 分栏展示 | 50% |
| 引用文字 | 居中斜体 | 70% |
| 图片 | 全屏/半屏图 | - |
| 代码块 | 等宽字体 | 45% |

## 与其他Skill的协作

- **上游Skill**：`2.article-gen-skill`（文章生成）
- **下游Skill**：`4.website-publish-skill`（网站发布）
- **数据流**：`article-structured.json` → `slides.html` → 发布到网站

## 最佳实践

1. **内容精简**：每页幻灯片不超过6行文字，避免大段文字
2. **视觉优先**：多用图表、图片，少用纯文字
3. **节奏控制**：每章1-2页，总页数控制在10-20页
4. **配色协调**：统一主题色，避免颜色过多
5. **字体层级**：标题>副标题>正文>注释，层级清晰
6. **可读性**：保证最小字号，远距离可读

## 质量检查清单

- [ ] 封面信息完整（标题、副标题、作者、日期）
- [ ] 目录页与实际章节一致
- [ ] 每页内容不超过屏幕高度
- [ ] 文字颜色与背景对比度足够
- [ ] 图片清晰且加载正常
- [ ] 键盘导航正常工作
- [ ] 响应式布局正常
- [ ] 总页数合理（10-20页）
- [ ] 主题与内容风格匹配
- [ ] 打印为PDF效果良好
