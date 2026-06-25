---
name: "design-style-skill"
description: "整合Google DESIGN.md设计系统与67个AI设计Skill，提供设计Token管理、设计风格选择、设计规范验证能力。当用户需要提升幻灯片/网页美学设计、选择设计风格、验证设计一致性时调用此Skill。"
---

# Design Style Skill - 设计风格与设计系统

## 功能描述

本Skill作为**设计能力增强层**，整合Google DESIGN.md设计系统规范与TypeUI 67个设计Skill，为工作流提供：
- 设计Token生成与管理
- 67种设计风格快速选择
- 设计一致性验证
- Tailwind CSS配置生成

## 触发条件

当以下条件满足时触发：
- 用户表达"提升设计"、"选个风格"、"更好看"、"设计系统"
- 生成幻灯片前需要选择设计风格
- 需要将DESIGN.md设计规范应用到项目
- 用户提到具体风格关键词：glassmorphism、material、gradient等

## 三层结构

```
5.design-style-skill/
├── SKILL.md                    # 本文件 - Skill说明
├── references/                 # 参考资料
│   ├── design-tokens.md        # Design Token规范
│   ├── 67-design-skills.md     # 67个设计Skill速查表
│   └── tailwind-config.md      # Tailwind配置生成指南
└── scripts/                    # 脚本工具
    ├── gen-design-tokens.py     # 生成设计Token
    ├── apply-style.py           # 应用设计风格到HTML
    └── validate-design.py       # 验证设计一致性
```

## 设计风格速查

### 流行风格（推荐优先）

| 风格 | 命令 | 适用场景 |
|-----|------|---------|
| `glassmorphism` | `typeui pull glassmorphism` | 现代感、毛玻璃效果 |
| `elegant` | `typeui pull elegant` | 高端优雅、奢侈品 |
| `gradient` | `typeui pull gradient` | 活力渐变、创意 |
| `contemporary` | `typeui pull contemporary` | 当代设计、简洁 |
| `material` | `typeui pull material` | Material Design、安卓 |
| `minimal` | `typeui pull minimal` | 极简留白、艺术 |

### 应用场景分类

**商务企业**
- `corporate` - 企业官网
- `enterprise` - 大型企业
- `application` - 办公应用

**创意艺术**
- `artistic` - 艺术感
- `creative` - 创意设计
- `fantasy` - 奇幻风格

**技术科技**
- `codex` - 技术文档
- `matrix` - 科技感
- `futuristic` - 未来感
- `cosmic` - 宇宙主题

**内容展示**
- `editorial` - 编辑出版
- `bento` - 卡片布局
- `dashboard` - 数据仪表盘

## 使用方法

### 1. 选择设计风格

```bash
# 列出所有可用风格
typeui list

# 拉取指定风格到当前目录
typeui pull glassmorphism
typeui pull elegant

# 或使用内置脚本选择
python scripts/apply-style.py --list
python scripts/apply-style.py --select elegant
```

### 2. 生成Design Token

```bash
# 根据内容自动生成设计Token
python scripts/gen-design-tokens.py --theme ocean

# 指定颜色和字体
python scripts/gen-design-tokens.py --primary "#0077cc" --font "Inter"
```

### 3. 验证设计一致性

```bash
# 验证HTML是否符合设计规范
python scripts/validate-design.py --input slides.html --standard material

# 检查对比度和可访问性
python scripts/validate-design.py --input slides.html --check-a11y
```

### 4. 应用设计风格到HTML

```bash
# 将design token应用到现有HTML
python scripts/apply-style.py --input slides.html --style glassmorphism

# 指定输出文件
python scripts/apply-style.py -i slides.html -s elegant -o styled-slides.html
```

## Design Token格式

基于Google DESIGN.md规范的Token结构：

```yaml
---
name: Custom Style
version: alpha
colors:
  primary: "#0077cc"
  secondary: "#6c7278"
  accent: "#ff6b6b"
  background: "#f8f9fa"
  surface: "#ffffff"
  text: "#1a1c1e"
typography:
  h1:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
rounded:
  sm: 4px
  md: 8px
  lg: 16px
---
```

## 67个设计Skill完整列表

| 风格 | 关键词 | 风格 | 关键词 |
|-----|-------|-----|-------|
| agentic | AI风格 | ant | 蚂蚁设计 |
| application | 应用风格 | artistic | 艺术感 |
| bento | 卡片网格 | bold | 粗体醒目 |
| brutalism | 粗野主义 | cafe | 咖啡馆 |
| claymorphism | 粘土质感 | claude | Claude风格 |
| clean | 清洁简洁 | codex | 代码文档 |
| colorful | 色彩丰富 | contemporary | 当代简洁 |
| corporate | 企业风格 | cosmic | 宇宙主题 |
| creative | 创意设计 | dashboard | 数据仪表盘 |
| dithered | 抖动效果 | doodle | 涂鸦风格 |
| dramatic | 戏剧性 | editorial | 编辑出版 |
| elegant | 优雅高端 | energetic | 活力动感 |
| enterprise | 企业级 | expressive | 表达力 |
| fantasy | 奇幻风格 | fiction | 小说风格 |
| flat | 扁平设计 | friendly | 友好亲切 |
| futuristic | 未来科技 | glassmorphism | 毛玻璃 |
| gradient | 渐变风格 | immersive | 沉浸式 |
| impeccable | 完美无瑕 | levels | 层级感 |
| lingo | 语言风格 | luxury | 奢侈豪华 |
| material | Material | matrix | 矩阵科技 |
| neo | 新概念 | neutral | 中性灰 |
| noise | 噪点纹理 | organic | 有机自然 |
| pastel | 粉彩色 | playful | 俏皮风格 |
| premium | 高端质感 | print | 打印风格 |
| raw | 原始风格 | retro | 复古风格 |
| saturated | 高饱和 | simple | 简约风格 |
| soft | 柔和风格 | solid | 纯色块 |
| sophisticated | 精致复杂 | spatial | 空间感 |
| stark | 极简对比 | street | 街头风格 |
| technical | 技术文档 | textured | 纹理质感 |
| timeless | 永恒经典 | tiny | 微小精致 |
| tropical | 热带风格 | unsaturated | 低饱和 |
| vibrant | 活泼鲜艳 | vintage | 复古怀旧 |
| vivid | 强烈色彩 | warm | 暖色调 |

## 与其他Skill的协作

- **上游Skill**：可被所有Skill调用获取设计规范
- **下游Skill**：`3.slides-html-skill`（幻灯片生成时选择风格）
- **数据流**：`design-token.json` → 注入到HTML模板 → 输出精美页面

## 最佳实践

1. **风格匹配**：根据内容主题选择风格（科技选codex/matrix，艺术选artistic）
2. **Token优先**：优先使用Token定义，确保一致性
3. **渐进增强**：从minimal/clean开始，逐步增加复杂度
4. **场景适配**：商务用corporate/enterprise，创意用glassmorphism/gradient
5. **响应式**：确保设计Token支持多设备适配

## 质量检查清单

- [ ] 设计的风格与内容主题匹配
- [ ] 颜色对比度符合WCAG AA标准
- [ ] 字体层级清晰可读
- [ ] 间距系统一致
- [ ] 圆角和阴影风格统一
- [ ] 移动端显示正常
- [ ] 符合选定设计Skill的规范
