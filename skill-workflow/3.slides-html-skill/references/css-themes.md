# CSS 主题样式指南

## 主题概览

| 主题名称 | 风格描述 | 主色调 | 适用场景 |
|---------|---------|-------|---------|
| `modern` | 现代简约 | 蓝色系 | 科技、商务 |
| `classic` | 经典正式 | 深灰系 | 学术、报告 |
| `gradient` | 渐变活力 | 紫粉渐变 | 创意、营销 |
| `minimal` | 极简留白 | 黑白灰 | 艺术、个人 |
| `dark` | 暗色模式 | 深色系 | 技术、夜间 |
| `ocean` | 海洋清新 | 青蓝渐变 | 自然、健康 |
| `sunset` | 日落暖橙 | 橙黄渐变 | 生活、美食 |
| `forest` | 森林自然 | 绿色系 | 环保、教育 |

---

## 1. Modern 主题（现代简约）

### 配色方案
```css
:root {
  --primary: #2563eb;      /* 主色：蓝色 */
  --secondary: #64748b;    /* 次色：灰蓝 */
  --accent: #3b82f6;       /* 强调：亮蓝 */
  --bg: #ffffff;           /* 背景：白色 */
  --bg-alt: #f8fafc;       /* 次背景：浅灰 */
  --text: #1e293b;         /* 文字：深灰 */
  --text-light: #64748b;   /* 次要文字：中灰 */
  --border: #e2e8f0;       /* 边框：浅灰 */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}
```

### 字体
```
标题: Inter, system-ui, sans-serif
正文: Inter, system-ui, sans-serif
代码: JetBrains Mono, Fira Code, monospace
```

### 视觉特征
- 大量留白，呼吸感强
- 圆角卡片（12px）
- 柔和阴影
- 蓝色点缀，专业感

---

## 2. Classic 主题（经典正式）

### 配色方案
```css
:root {
  --primary: #1e3a5f;      /* 主色：深蓝灰 */
  --secondary: #4a5568;    /* 次色：暗灰 */
  --accent: #2c5282;       /* 强调：深蓝 */
  --bg: #f7fafc;           /* 背景：米白 */
  --bg-alt: #edf2f7;       /* 次背景：浅灰蓝 */
  --text: #1a202c;         /* 文字：近黑 */
  --text-light: #4a5568;   /* 次要文字：深灰 */
  --border: #cbd5e0;       /* 边框：灰 */
  --success: #2f855a;
  --warning: #d69e2e;
  --error: #c53030;
}
```

### 字体
```
标题: Georgia, "Times New Roman", serif
正文: Georgia, "Times New Roman", serif
代码: Consolas, "Courier New", monospace
```

### 视觉特征
- 衬线字体，正式感
- 边框清晰，直角
- 低饱和度，稳重
- 适合学术报告

---

## 3. Gradient 主题（渐变活力）

### 配色方案
```css
:root {
  --primary: #8b5cf6;      /* 主色：紫色 */
  --secondary: #ec4899;    /* 次色：粉红 */
  --accent: #06b6d4;       /* 强调：青色 */
  --bg: #ffffff;           /* 背景：白 */
  --bg-alt: #fdf4ff;       /* 次背景：浅紫 */
  --text: #1f2937;         /* 文字：深灰 */
  --text-light: #6b7280;   /* 次要文字：灰 */
  --border: #e5e7eb;       /* 边框：浅灰 */
  --gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
  --gradient-secondary: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
}
```

### 字体
```
标题: "Poppins", system-ui, sans-serif
正文: "Inter", system-ui, sans-serif
代码: "Fira Code", monospace
```

### 视觉特征
- 紫粉渐变，活力四射
- 圆角大（16px）
- 强对比色
- 适合创意营销

---

## 4. Minimal 主题（极简留白）

### 配色方案
```css
:root {
  --primary: #000000;      /* 主色：纯黑 */
  --secondary: #555555;    /* 次色：中灰 */
  --accent: #333333;       /* 强调：深灰 */
  --bg: #ffffff;           /* 背景：纯白 */
  --bg-alt: #fafafa;       /* 次背景：极浅灰 */
  --text: #111111;         /* 文字：近黑 */
  --text-light: #888888;   /* 次要文字：浅灰 */
  --border: #eeeeee;       /* 边框：极浅灰 */
  --success: #000000;
  --warning: #000000;
  --error: #000000;
}
```

### 字体
```
标题: "Helvetica Neue", Helvetica, Arial, sans-serif
正文: "Helvetica Neue", Helvetica, Arial, sans-serif
代码: "SF Mono", Monaco, monospace
```

### 视觉特征
- 黑白灰三色
- 极致留白
- 细线条
- 高级简约感

---

## 5. Dark 主题（暗色模式）

### 配色方案
```css
:root {
  --primary: #60a5fa;      /* 主色：亮蓝 */
  --secondary: #94a3b8;    /* 次色：浅灰蓝 */
  --accent: #22d3ee;       /* 强调：青蓝 */
  --bg: #0f172a;           /* 背景：深蓝黑 */
  --bg-alt: #1e293b;       /* 次背景：深蓝灰 */
  --text: #f1f5f9;         /* 文字：近白 */
  --text-light: #94a3b8;   /* 次要文字：浅灰 */
  --border: #334155;       /* 边框：深灰蓝 */
  --success: #34d399;
  --warning: #fbbf24;
  --error: #f87171;
}
```

### 字体
```
标题: Inter, system-ui, sans-serif
正文: Inter, system-ui, sans-serif
代码: JetBrains Mono, monospace
```

### 视觉特征
- 深色背景，护眼
- 高对比度文字
- 科技感十足
- 适合夜间演示

---

## 通用布局规范

### 容器尺寸
```css
.slide-container {
  width: 100%;
  height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
```

### 字号规范
```css
h1 { font-size: 3.5rem; font-weight: 700; }  /* 主标题 */
h2 { font-size: 2.5rem; font-weight: 600; }  /* 章节标题 */
h3 { font-size: 1.75rem; font-weight: 600; } /* 子标题 */
p  { font-size: 1.25rem; line-height: 1.8; } /* 正文 */
li { font-size: 1.25rem; line-height: 2; }   /* 列表 */
```

### 间距规范
```css
.section-padding: 80px 0;
element-margin: 1.5rem 0;
list-item-gap: 0.75rem;
```

### 动画时间
```css
fade-duration: 0.5s;
slide-duration: 0.6s;
easing: cubic-bezier(0.4, 0, 0.2, 1);
```
