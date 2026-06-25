# Tailwind CSS 配置指南

基于 Google DESIGN.md 的 Tailwind v4 配置生成

## 基础配置模板

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.html'],
  theme: {
    extend: {
      // 颜色系统
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        accent: 'var(--color-accent)',
        background: 'var(--color-background)',
        surface: 'var(--color-surface)',
        text: 'var(--color-text)',
        'text-secondary': 'var(--color-text-secondary)',
      },
      // 字体系统
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      // 间距系统
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
        '3xl': '64px',
      },
      // 圆角系统
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '16px',
        'xl': '24px',
      },
      // 阴影系统
      boxShadow: {
        'sm': '0 1px 2px rgba(0,0,0,0.05)',
        'md': '0 4px 6px rgba(0,0,0,0.1)',
        'lg': '0 10px 15px rgba(0,0,0,0.1)',
        'xl': '0 20px 25px rgba(0,0,0,0.15)',
      },
      // 动画
      transitionDuration: {
        'fast': '120ms',
        'normal': '250ms',
        'slow': '400ms',
      },
    },
  },
  plugins: [],
}
```

## CSS变量模式

### 定义CSS变量

```css
/* 在HTML的<style>中定义 */
:root {
  /* 颜色 */
  --color-primary: #0077cc;
  --color-secondary: #6c7278;
  --color-accent: #ff6b6b;
  --color-background: #f8f9fa;
  --color-surface: #ffffff;
  --color-text: #1a1c1e;
  --color-text-secondary: #6c7278;

  /* 字体 */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-serif: 'Georgia', serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

### 在Tailwind中使用

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
      },
    },
  },
}
```

## 暗色模式配置

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0077cc',
          dark: '#66b3ff',
        },
      },
    },
  },
}
```

```css
/* 暗色模式变量覆盖 */
.dark {
  --color-primary: #66b3ff;
  --color-background: #0b1326;
  --color-surface: #171f33;
  --color-text: #ffffff;
}
```

## 组件级设计Token

### 按钮

```css
.btn {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-weight: 500;
  transition: all var(--transition-normal);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  filter: brightness(1.1);
}
```

### 卡片

```css
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
}
```

### 输入框

```css
.input {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-secondary);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 119, 204, 0.2);
}
```

## Design Token → Tailwind CLI

Google DESIGN.md仓库提供的CLI工具：

```bash
# 安装
npm install @google/design.md

# 导出Design Token为Tailwind配置
npx @google/design.md export DESIGN.md --format tailwind

# 验证设计一致性
npx @google/design.md lint DESIGN.md

# 对比两个版本
npx @google/design.md diff DESIGN.md DESIGN-v2.md
```
