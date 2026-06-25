---
name: "website-publish-skill"
description: "将生成的HTML幻灯片和文章内容发布到个人Hugo网站，支持自动创建页面、资源拷贝、Git提交部署。Invoke when slides/article generation is complete and user wants to publish content to their personal website."
---

# Website Publish Skill - 网站发布

## 功能描述

本Skill作为工作流的**第四阶段**，负责将 Skill 3 生成的 HTML 幻灯片和 Skill 2 生成的文章内容，自动发布到基于 Hugo 的个人网站。支持页面创建、资源拷贝、Git 提交与部署。

## 触发条件

当以下条件满足时触发：
- Skill 3 (slides-html-skill) 已生成 `slides-*.html` 文件
- 用户明确表达"发布到网站"、"上传到博客"、"部署"
- 文章内容和幻灯片都已完成并确认无误

## 三层结构

```
4.website-publish-skill/
├── SKILL.md                  # 本文件 - Skill说明
├── references/               # 参考资料
│   ├── hugo-structure.md     # Hugo网站结构说明
│   └── deploy-guide.md       # 发布部署指南
└── scripts/                  # 脚本工具
    ├── publish-slides.py     # 幻灯片发布脚本
    ├── publish-article.py    # 文章发布脚本
    └── site-utils.py         # 网站工具函数
```

## 使用方法

### 1. 发布幻灯片

```bash
python scripts/publish-slides.py --input ../data/slides-xxx.html
```

**自动操作**：
1. 检测 Hugo 网站根目录
2. 将 HTML 文件拷贝到 `static/slides/` 目录
3. 在 `content/slides/` 创建对应 Markdown 页面
4. 更新 slides 列表页面
5. 可选：Git 提交并推送

### 2. 发布文章

```bash
python scripts/publish-article.py --input ../data/article-xxx.md
```

**自动操作**：
1. 检测 Hugo 网站根目录
2. 将文章拷贝到 `content/posts/` 或 `content/articles/`
3. 解析 YAML Front Matter
4. 提取首图（如有）
5. 生成文章摘要
6. 可选：Git 提交并推送

### 3. 一键全量发布

```bash
python scripts/publish-slides.py --all --auto-deploy
```

## Hugo 网站结构适配

### 支持的目录结构

```
site/                          # Hugo 网站根目录
├── content/
│   ├── posts/                 # 博客文章
│   ├── articles/              # 长文章
│   ├── slides/                # 幻灯片页面
│   └── page/                  # 独立页面
├── static/
│   ├── slides/                # 幻灯片HTML文件
│   ├── images/                # 图片资源
│   └── files/                 # 文件下载
├── layouts/                   # 模板
├── themes/                    # 主题
└── public/                    # 生成的静态文件
```

### 自动检测逻辑

1. 从当前目录向上查找 `hugo.toml` 或 `config.toml`
2. 检查 `content/` 目录是否存在
3. 识别使用的主题
4. 确定文章存放的 section（posts/articles）

## 发布流程

### 幻灯片发布流程
```
输入: slides-xxx.html
  ↓
1. 解析文件名，提取标题和ID
  ↓
2. 拷贝 HTML 到 static/slides/{id}/index.html
  ↓
3. 创建 content/slides/{id}.md
   - 标题、日期、描述
   - iframe 嵌入幻灯片
   - 分类标签
  ↓
4. 更新 slides 列表页（可选）
  ↓
5. Git add + commit + push（可选）
  ↓
输出: 发布成功信息 + 访问URL
```

### 文章发布流程
```
输入: article-xxx.md
  ↓
1. 解析 YAML Front Matter
  ↓
2. 生成 slug（URL友好的标题）
  ↓
3. 拷贝到 content/posts/{slug}/index.md
   （或 content/posts/{slug}.md）
  ↓
4. 提取图片资源到对应目录
  ↓
5. 自动添加文章摘要
  ↓
6. Git add + commit + push（可选）
  ↓
输出: 发布成功信息 + 访问URL
```

## 配置选项

| 选项 | 说明 | 默认值 |
|-----|------|-------|
| `--site-path` | Hugo 网站根目录 | 自动检测 |
| `--section` | 文章所属 section | `posts` |
| `--auto-deploy` | 是否自动Git提交 | `false` |
| `--draft` | 是否作为草稿发布 | `false` |
| `--open` | 发布后自动打开 | `false` |

## 与其他Skill的协作

- **上游Skill**：
  - `2.article-gen-skill`（文章生成）→ 发布文章
  - `3.slides-html-skill`（幻灯片生成）→ 发布幻灯片
- **数据流**：
  - `article.md` → `content/posts/`
  - `slides.html` → `static/slides/` + `content/slides/`

## 最佳实践

1. **先预览再发布**：本地 `hugo server` 预览效果
2. **Git 提交规范**：使用约定式提交（Conventional Commits）
3. **SEO 优化**：确保标题、描述、关键词完整
4. **图片优化**：发布前压缩图片，添加 alt 文本
5. **分类标签**：正确归类，添加相关标签
6. **内部链接**：添加相关文章推荐链接

## 发布后检查清单

- [ ] 页面能正常访问
- [ ] 图片加载正常
- [ ] 样式显示正确
- [ ] 幻灯片可正常翻页
- [ ] 移动端适配正常
- [ ] 标题/描述/关键词完整
- [ ] 分类标签正确
- [ ] 列表页已更新
- [ ] 站点地图已更新
- [ ] 加载速度正常
