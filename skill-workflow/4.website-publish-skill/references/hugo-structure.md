# Hugo 网站结构说明

## Hugo 基础结构

```
hugo-site/
├── archetypes/          # 内容原型模板
│   └── default.md
├── assets/              # 资源文件（SCSS、JS等）
├── content/             # 内容目录（Markdown文件）
│   ├── posts/           # 博客文章
│   ├── pages/           # 独立页面
│   └── slides/          # 幻灯片页面
├── data/                # 数据文件（JSON/TOML/YAML）
├── layouts/             # 模板文件
│   ├── _default/
│   ├── partials/
│   └── shortcodes/
├── static/              # 静态文件（直接拷贝到public）
│   ├── images/
│   ├── slides/
│   └── files/
├── themes/              # 主题
│   └── your-theme/
├── public/              # 生成的静态网站（运行hugo后）
├── hugo.toml            # 配置文件（新格式）
└── config.toml          # 配置文件（旧格式）
```

## Content 目录详解

### 单文件模式
```
content/
└── posts/
    ├── article-1.md
    └── article-2.md
```

### Page Bundle 模式（推荐）
```
content/
└── posts/
    ├── article-1/
    │   ├── index.md     # 文章正文
    │   ├── cover.jpg    # 封面图
    │   └── images/      # 文章内图片
    └── article-2/
        ├── index.md
        └── featured.png
```

## Front Matter 规范

### 基础字段
```yaml
---
title: "文章标题"
date: 2026-06-25T10:00:00+08:00
draft: false
description: "文章描述，用于SEO和摘要"
summary: "文章摘要，用于列表页"
---
```

### 分类与标签
```yaml
---
categories:
  - 技术
  - 前端
tags:
  - Hugo
  - 静态网站
  - 博客
---
```

### 图片设置
```yaml
---
featured_image: "/images/cover.jpg"
images:
  - "/images/cover.jpg"
---
```

### 作者信息
```yaml
---
author: "作者名"
avatar: "/images/avatar.jpg"
bio: "作者简介"
---
```

## 幻灯片页面规范

### Markdown 嵌入方式
```markdown
---
title: "AI在医疗健康领域的应用"
date: 2026-06-25
description: "幻灯片：探讨AI如何改变医疗健康行业"
type: "slides"
---

<iframe src="/slides/ai-health/index.html" 
        style="width:100%; height: 80vh; border: none; border-radius: 8px;">
</iframe>

[全屏查看幻灯片](/slides/ai-health/index.html)
```

### 幻灯片目录结构
```
static/
└── slides/
    ├── ai-health/
    │   └── index.html
    └── web-performance/
        └── index.html

content/
└── slides/
    ├── ai-health.md
    └── web-performance.md
```

## 常用 Shortcodes

### 图片
```markdown
{{</* figure src="/images/photo.jpg" title="图片标题" */>}}
```

### 代码高亮
```markdown
{{</* highlight python */>}}
print("Hello, World!")
{{</* /highlight */>}}
```

### 提示框
```markdown
{{</* alert info */>}}
这是一条提示信息
{{</* /alert */>}}
```

## 自动生成 Slug 规则

1. 转为小写
2. 空格替换为 `-`
3. 移除特殊字符
4. 保留中文（Hugo 支持中文 URL）

```
"AI在医疗健康领域的应用" → "ai-zai-yi-liao-jian-kang-ling-yu-de-ying-yong"
"Hello World 123" → "hello-world-123"
```

## Git 提交规范

### 约定式提交（Conventional Commits）
```
feat: 添加新功能
fix: 修复bug
docs: 文档更新
style: 样式调整
refactor: 重构
perf: 性能优化
test: 测试相关
chore: 构建/工具链
```

### 示例
```
feat(posts): 添加AI医疗健康文章

- 新增文章《AI在医疗健康领域的应用》
- 添加相关标签和分类
- 优化文章摘要
```

## 部署方式

### 方式1：GitHub Pages
```bash
hugo
cd public
git init
git add .
git commit -m "deploy: update site"
git push -f origin gh-pages
```

### 方式2：Vercel / Netlify
- 连接 Git 仓库
- 配置 Build Command: `hugo`
- 配置 Publish Directory: `public`
- 自动部署

### 方式3：自有服务器
```bash
hugo
rsync -avz public/ user@server:/var/www/site/
```
