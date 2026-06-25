# Design Token 规范参考

基于 Google DESIGN.md 设计系统规范

## Token 类型

### 颜色 (Colors)

```yaml
colors:
  primary: "#0077cc"        # 主色：品牌核心色
  secondary: "#6c7278"      # 次要色：辅助表达
  tertiary: "#ff6b6b"        # 强调色：CTA、警示
  neutral: "#f8f9fa"         # 中性色：背景、边框
  background: "#ffffff"      # 页面背景
  surface: "#ffffff"         # 卡片/容器背景
  text: "#1a1c1e"            # 主文本
  text-secondary: "#6c7278"  # 次要文本
```

### 字体 (Typography)

```yaml
typography:
  display-lg:               # 展示标题
    fontFamily: Inter
    fontSize: 84px
    fontWeight: 700
    lineHeight: 90px
    letterSpacing: -0.04em
  headline-lg:              # 大标题
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 40px
  headline-md:              # 中标题
    fontFamily: Inter
    fontSize: 24px
    fontWeight: 500
    lineHeight: 32px
  body-lg:                  # 正文大
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 28px
  body-md:                  # 正文中
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
  label-sm:                 # 标签/注释
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 16px
```

### 间距 (Spacing)

```yaml
spacing:
  xs: 4px                   # 紧凑间距
  sm: 8px                   # 小间距
  md: 16px                  # 标准间距
  lg: 24px                  # 大间距
  xl: 32px                  # 特大间距
  2xl: 48px                 # 区域间距
  3xl: 64px                 # 页面边距
```

### 圆角 (Rounded)

```yaml
rounded:
  none: 0px                  # 无圆角
  sm: 4px                   # 小圆角
  md: 8px                   # 中圆角
  lg: 16px                  # 大圆角
  xl: 24px                  # 超大圆角
  full: 9999px              # 药丸形/圆形
```

### 阴影 (Shadow)

```yaml
shadow:
  sm: "0 1px 2px rgba(0,0,0,0.05)"
  md: "0 4px 6px rgba(0,0,0,0.1)"
  lg: "0 10px 15px rgba(0,0,0,0.1)"
  xl: "0 20px 25px rgba(0,0,0,0.15)"
```

### 过渡 (Motion)

```yaml
motion:
  fast: 120ms               # 微交互
  normal: 250ms             # 标准过渡
  slow: 400ms              # 大动画
  easing: "cubic-bezier(0.2, 0, 0, 1)"
```

## 常用配色方案

### Ocean (海洋) - 默认主题
```yaml
primary: "#0077cc"
secondary: "#6c7278"
accent: "#00a8e8"
background: "#f8fafc"
surface: "#ffffff"
text: "#1a1c1e"
```

### Forest (森林)
```yaml
primary: "#2d5a27"
secondary: "#6c7278"
accent: "#8bc34a"
background: "#f5f7f2"
surface: "#ffffff"
text: "#1a1c1e"
```

### Sunset (日落)
```yaml
primary: "#ff6b6b"
secondary: "#6c7278"
accent: "#feca57"
background: "#fff9f5"
surface: "#ffffff"
text: "#1a1c1e"
```

### Dark (暗色)
```yaml
primary: "#ffffff"
secondary: "#8e9192"
accent: "#00a8e8"
background: "#0b1326"
surface: "#171f33"
text: "#ffffff"
```

## Tailwind CSS 转换

Design Token 可直接转换为 Tailwind 主题配置：

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#0077cc',
        secondary: '#6c7278',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '16px',
      },
    },
  },
}
```

## WCAG 对比度要求

| 文本类型 | 最小对比度 | 适用标准 |
|---------|-----------|---------|
| 大文本 (>18px) | 3:1 | AA |
| 正常文本 (<18px) | 4.5:1 | AA |
| UI组件/图形 | 3:1 | AA |
| 关键操作按钮 | 4.5:1 | AAA推荐 |

## 可访问性检查

- 前景/背景颜色对比度
- 字体大小 ≥ 12px（标签）/ ≥ 14px（正文）
- 行高 ≥ 1.2（标题）/ ≥ 1.5（正文）
- 字母间距适中
