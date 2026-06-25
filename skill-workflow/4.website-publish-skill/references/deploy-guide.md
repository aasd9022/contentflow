# 发布部署指南

## 发布前检查清单

### 内容检查
- [ ] 文章标题准确且吸引人
- [ ] 描述/摘要完整（150字以内）
- [ ] 关键词合理（3-5个）
- [ ] 分类标签正确
- [ ] 正文无错别字
- [ ] 图片都有 alt 文本
- [ ] 链接都有效
- [ ] 代码格式正确

### 技术检查
- [ ] Hugo 本地构建无错误
- [ ] 页面在各浏览器正常显示
- [ ] 移动端适配正常
- [ ] 幻灯片可正常翻页
- [ ] 图片加载正常
- [ ] 加载速度可接受
- [ ] SEO 元信息完整

---

## 发布流程

### 第一步：本地预览
```bash
# 启动 Hugo 开发服务器
hugo server -D

# 访问
open http://localhost:1313
```

检查项：
- 页面布局是否正常
- 样式是否正确
- 图片是否加载
- 幻灯片是否可交互

### 第二步：构建生产版本
```bash
# 清理旧的 public 目录
hugo --cleanDestinationDir

# 生产构建
hugo --minify

# 检查构建结果
ls -la public/
```

### 第三步：Git 提交
```bash
# 查看变更
git status

# 添加变更
git add content/posts/xxx/
git add static/slides/xxx/

# 提交（约定式提交
git commit -m "feat(posts): 添加 xxx 文章"

# 推送到远程
git push origin main
```

### 第四步：部署
根据你的部署方式选择：

#### GitHub Pages:
```bash
# 方式A: 使用 gh-pages 分支
git subtree push --prefix public origin gh-pages
```

#### Vercel/Netlify:
- 自动部署（推送触发）
- 检查部署日志
- 验证生产环境

#### 自有服务器:
```bash
rsync -avz --delete public/ user@server:/var/www/site/
```

---

## 幻灯片发布专用流程

### 幻灯片结构
```
源文件:
  slides-ai-health.html

发布后结构:
  static/slides/ai-health/index.html  (HTML文件)
  content/slides/ai-health.md       (页面入口)
```

### 幻灯片页面模板
```markdown
---
title: "AI在医疗健康领域的应用 - 幻灯片"
date: 2026-06-25
description: "探讨AI如何改变医疗健康行业的演示文稿"
type: slides
categories:
  - 幻灯片
tags:
  - AI
  - 医疗
  - 幻灯片
---

## 幻灯片简介

这是关于 AI 在医疗健康领域应用的演示文稿。

## 在线查看

<iframe src="/slides/ai-health/index.html" 
        style="width: 100%;
               height: 80vh;
               border: none;
               border-radius: 8px;
               box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
</iframe>

[点击全屏查看幻灯片](/slides/ai-health/index.html){.btn .btn-primary}

## 使用说明

- 使用 **← →** 键翻页
- 按 **F** 键进入全屏
- 点击屏幕左右边缘也可翻页
- 支持移动端触控滑动
```

---

## 文章发布专用流程

### 文章结构（Page Bundle）
```
源文件:
  article-ai-health.md

发布后结构:
  content/posts/ai-health/index.md
  content/posts/ai-health/images/
```

### 文章 Front Matter 模板
```yaml
---
title: "AI在医疗健康领域的应用与未来"
date: 2026-06-25T10:00:00+08:00
draft: false

description: "深入探讨人工智能如何改变传统医疗健康行业，包括疾病诊断、药物研发、健康管理等应用场景。"
summary: "人工智能正在深刻改变医疗健康行业，从疾病诊断到药物研发，从健康管理到医疗影像，AI技术正在重塑医疗健康的未来。"

author: "作者名"
avatar: "/images/avatar.jpg"

categories:
  - 技术
  - 人工智能

tags:
  - AI
  - 医疗
  - 健康管理
  - 数字化

featured_image: "/images/ai-health-cover.jpg"
images:
  - "/images/ai-health-cover.jpg"

keywords:
  - 人工智能
  - 医疗健康
  - AI应用
  - 数字化转型
---
```

---

## SEO 优化指南

### 标题优化
- 长度：50-60字符
- 包含核心关键词
- 吸引点击

### 描述优化
- 长度：120-150字符
- 概括文章核心价值
- 包含关键词

### 关键词优化
- 3-5个核心关键词
- 自然融入正文
- 标题、描述、正文都要出现

### 图片优化
- 添加 alt 文本
- 压缩图片大小
- 使用 WebP 格式
- 添加 lazy loading

### 内部链接
- 相关文章推荐
- 锚点链接
- 面包屑导航

---

## 常见问题

### Q: 发布后页面不显示？
A: 检查以下几点：
1. draft 是否设置为 false
2. 日期是否在当前时间之前
3. 文件是否在正确的 content 目录下
4. Hugo 构建是否有错误

### Q: 幻灯片无法访问？
A: 检查：
1. HTML 文件是否在 static/slides/ 目录
2. 文件路径是否正确
3. 文件名是否一致
4. 浏览器控制台是否有报错

### Q: 图片加载失败？
A: 检查：
1. 图片路径是否正确
2. 图片是否在 static 目录或 page bundle 内
3. 文件名大小写是否匹配
4. 图片格式是否支持

### Q: 样式不对？
A: 检查：
1. 主题是否正确配置
2. type 是否设置正确
3. 自定义CSS是否加载
4. 浏览器缓存是否清除

---

## 发布后验证

### 功能验证
- [ ] 页面可正常访问
- [ ] 标题显示正确
- [ ] 正文格式正确
- [ ] 图片都加载成功
- [ ] 链接可点击
- [ ] 分类标签正确

### 性能验证
- [ ] 首屏加载 < 3s
- [ ] Lighthouse 分数 > 80
- [ ] 移动端适配正常
- [ ] 无控制台错误

### SEO验证
- [ ] 标题正确
- [ ] 描述完整
- [ ] 关键词合理
- [ ] Open Graph 正常
- [ ] 结构化数据正常
