<div align="center">

# ContentFlow

<h3>
  一站式 AI 内容生产工作流
</h3>

<p>
  从灵感到发布，只需一条命令
</p>

<p>
  <a href="#-特性"><strong>特性</strong></a> ·
  <a href="#-快速开始"><strong>快速开始</strong></a> ·
  <a href="#-架构"><strong>架构</strong></a> ·
  <a href="#-使用指南"><strong>使用指南</strong></a>
</p>

</div>

## ✨ 特性

- **🎯 五阶流水线**：信息收集 → 大纲生成 → 文章撰写 → 幻灯片制作 → 网站发布
- **🧩 模块化设计**：每个阶段都是独立 Skill，可单独调用或自由组合
- **🎨 8+ 幻灯片主题**：modern / classic / gradient / minimal / dark / ocean / sunset / forest
- **🖌️ 67 种设计风格**：内置完整设计系统，一键切换视觉风格
- **📝 智能大纲**：先生成大纲确认，再生成全文，减少返工
- **🔄 断点续跑**：支持从任意阶段开始，跳过不需要的步骤
- **🌐 Hugo 集成**：自动发布到 Hugo 静态网站
- **⌨️ 双模式**：交互式引导上手，命令行参数批量生产
- **📦 零依赖**：纯 Python 标准库实现，开箱即用

## 📦 包含的 Skill

| # | Skill | 功能 | 输出 |
|---|-------|------|------|
| 1 | `ask-info-skill` | 结构化对话收集创作需求 | `article-info.json` |
| 2 | `article-gen-skill` | AI 生成大纲与完整文章 | `article.md` + 结构化 JSON |
| 3 | `slides-html-skill` | 文章转精美 HTML 幻灯片 | `slides.html` |
| 4 | `website-publish-skill` | 一键发布到 Hugo 网站 | 部署到网站 |
| 5 | `design-style-skill` | 设计 Token 与风格管理 | 设计规范 + CSS |

## 🚀 快速开始

### 环境要求

- Python 3.7+
- （可选）Hugo 网站用于发布

### 安装

```bash
git clone https://github.com/yourusername/contentflow.git
cd contentflow
```

### 交互式完整流程

```bash
python workflow.py
```

### 快速生成（指定所有参数）

```bash
python workflow.py \
  --topic "AI在医疗健康领域的应用" \
  --audience "产品经理和技术决策者" \
  --style "专业严谨" \
  --length "1500-2000字" \
  --key-points "技术原理,应用场景,未来趋势,挑战与机遇"
```

### 常用组合

| 场景 | 命令 |
|------|------|
| 完整流程（交互） | `python workflow.py` |
| 完整流程（快速） | `python workflow.py --topic ... --style ...` |
| 仅生成文章 | `--skip-slides --skip-publish` |
| 文章 + 幻灯片 | `--skip-publish` |
| 指定幻灯片主题 | `--theme gradient` |
| 从中间阶段开始 | `--from-info xxx.json` / `--from-article xxx.md` |

## 🏗️ 架构

### 工作流管线

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  信息收集   │ →  │  文章生成   │ →  │  幻灯片生成 │ →  │  网站发布   │
│ ask-info    │    │ article-gen │    │ slides-html │    │  publish    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                 ↑
                          ┌─────────────┐                        │
                          │ 设计风格    │ ───────────────────────┘
                          │ design-style│
                          └─────────────┘
```

### 目录结构

```
contentflow/
├── SKILL.md                    # 总入口 Skill 说明
├── workflow.py                 # 工作流主脚本
├── 1.ask-info-skill/           # Skill 1: 信息收集
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── 2.article-gen-skill/        # Skill 2: 文章生成
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── 3.slides-html-skill/        # Skill 3: 幻灯片
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── 4.website-publish-skill/    # Skill 4: 网站发布
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── 5.design-style-skill/       # Skill 5: 设计风格
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── data/                       # 生成的内容（自动创建）
```

## 📖 使用指南

### 阶段 1: 信息收集

通过 5 个维度收集文章创作需求：

| 维度 | 说明 | 示例 |
|------|------|------|
| 主题 | 文章核心主题 | "AI在医疗健康领域的应用" |
| 受众 | 目标读者群体 | "医疗从业者、产品经理" |
| 风格 | 写作风格 | 专业严谨 / 通俗易懂 / 故事化叙事 |
| 长度 | 字数范围 | 500-1000 / 1500-2000 / 3000-5000 |
| 核心要点 | 必须涵盖的内容 | "技术原理,应用场景,未来趋势" |

### 阶段 2: 文章生成

- 先生成大纲，确认后再生成全文
- 支持 5 种写作风格，每种对应不同的 Prompt 策略
- 自动生成 YAML Front Matter、字数统计、SEO 信息
- 输出 Markdown 文章 + 结构化 JSON（供幻灯片使用）

### 阶段 3: 幻灯片生成

**8 种主题可选：**

| 主题 | 风格 | 适用场景 |
|------|------|---------|
| `modern` | 现代简约 | 科技产品、商务演示 |
| `classic` | 经典正式 | 学术报告、会议演讲 |
| `gradient` | 渐变活力 | 创意设计、营销推广 |
| `minimal` | 极简留白 | 艺术摄影、个人展示 |
| `dark` | 暗色模式 | 技术分享、夜间演示 |
| `ocean` | 海洋蓝 | 科技、环保主题 |
| `sunset` | 日落橙 | 创意、生活方式 |
| `forest` | 森林绿 | 自然、健康主题 |

**幻灯片特性：**
- 键盘导航（← → 翻页，F 全屏）
- 响应式布局（桌面/平板/手机）
- 代码高亮
- 打印友好（可导出 PDF）

### 阶段 4: 网站发布

自动检测 Hugo 网站结构，支持：

- 文章发布到 `content/posts/` 或 `content/articles/`
- 幻灯片发布到 `static/slides/` + `content/slides/`
- 自动解析 Front Matter，生成 Slug
- 可选 Git 自动提交与部署

### 阶段 5: 设计风格（可选增强）

集成 67 种设计风格，支持：

- Design Token 生成与管理
- 一键应用设计风格到 HTML
- 设计一致性验证（对比度、可访问性）

## 🎯 命令行参数

```
内容生产工作流 - 信息收集→文章生成→幻灯片→网站发布

options:
  -h, --help            show this help message and exit

文章信息:
  --topic TOPIC         文章主题
  --audience AUDIENCE   目标受众
  --style STYLE         写作风格
  --length LENGTH       文章长度
  --key-points KEY_POINTS  核心要点（逗号分隔）

流程控制:
  --skip-slides         跳过幻灯片生成
  --skip-publish        跳过网站发布
  --publish-only        只执行发布阶段

发布配置:
  --site-path SITE_PATH  Hugo网站根目录
  --theme THEME         幻灯片主题（默认: modern）

断点续跑:
  --from-info FROM_INFO    从已有 article-info.json 开始
  --from-article FROM_ARTICLE  从已有 article.md 开始
  --from-slides FROM_SLIDES    从已有 slides.html 开始
```

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">
  <p>如果这个项目对你有帮助，欢迎给个 ⭐ Star</p>
</div>
