#!/usr/bin/env python3
"""
html-templates.py - HTML模板库

功能：
1. 提供5种主题的CSS样式模板
2. 提供各种幻灯片页面的HTML模板
3. 提供JavaScript交互逻辑
4. 供 gen-slides.py 调用
"""


# ============================================================
# CSS 主题样式
# ============================================================

CSS_THEMES = {
    "modern": """
/* ===== Modern Theme - 现代简约 ===== */
:root {
  --primary: #2563eb;
  --secondary: #64748b;
  --accent: #3b82f6;
  --bg: #ffffff;
  --bg-alt: #f8fafc;
  --text: #1e293b;
  --text-light: #64748b;
  --border: #e2e8f0;
  --success: #10b981;
  --shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.1);
  --radius: 12px;
}
body { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
h1, h2, h3 { font-weight: 700; letter-spacing: -0.025em; }
.card {
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
}
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover { background: var(--accent); transform: translateY(-1px); }
""",

    "classic": """
/* ===== Classic Theme - 经典正式 ===== */
:root {
  --primary: #1e3a5f;
  --secondary: #4a5568;
  --accent: #2c5282;
  --bg: #f7fafc;
  --bg-alt: #edf2f7;
  --text: #1a202c;
  --text-light: #4a5568;
  --border: #cbd5e0;
  --success: #2f855a;
  --shadow: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  --radius: 4px;
}
body { font-family: Georgia, 'Times New Roman', serif; }
h1, h2, h3 { font-weight: 700; letter-spacing: -0.01em; }
.card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
}
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover { background: var(--accent); }
""",

    "gradient": """
/* ===== Gradient Theme - 渐变活力 ===== */
:root {
  --primary: #8b5cf6;
  --secondary: #ec4899;
  --accent: #06b6d4;
  --bg: #ffffff;
  --bg-alt: #fdf4ff;
  --text: #1f2937;
  --text-light: #6b7280;
  --border: #e5e7eb;
  --success: #10b981;
  --gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
  --gradient-secondary: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%);
  --shadow: 0 10px 40px -10px rgba(139, 92, 246, 0.3);
  --shadow-lg: 0 25px 50px -12px rgba(139, 92, 246, 0.4);
  --radius: 16px;
}
body { font-family: 'Poppins', system-ui, sans-serif; }
h1 {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
}
h2, h3 { font-weight: 700; }
.card {
  background: white;
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid rgba(139, 92, 246, 0.1);
}
.btn-primary {
  background: var(--gradient-primary);
  color: white;
  padding: 0.875rem 2rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
""",

    "minimal": """
/* ===== Minimal Theme - 极简留白 ===== */
:root {
  --primary: #000000;
  --secondary: #555555;
  --accent: #333333;
  --bg: #ffffff;
  --bg-alt: #fafafa;
  --text: #111111;
  --text-light: #888888;
  --border: #eeeeee;
  --success: #000000;
  --shadow: none;
  --shadow-lg: none;
  --radius: 0px;
}
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
h1, h2, h3 { font-weight: 300; letter-spacing: -0.05em; }
h1 { font-size: 4rem; }
.card {
  background: white;
  border-bottom: 1px solid var(--border);
  padding: 3rem 0;
}
.btn-primary {
  background: transparent;
  color: black;
  padding: 0.75rem 2rem;
  border: 1px solid black;
  border-radius: 0;
  font-weight: 400;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.btn-primary:hover { background: black; color: white; }
""",

    "dark": """
/* ===== Dark Theme - 暗色模式 ===== */
:root {
  --primary: #60a5fa;
  --secondary: #94a3b8;
  --accent: #22d3ee;
  --bg: #0f172a;
  --bg-alt: #1e293b;
  --text: #f1f5f9;
  --text-light: #94a3b8;
  --border: #334155;
  --success: #34d399;
  --shadow: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -2px rgba(0,0,0,0.3);
  --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.5);
  --radius: 12px;
}
body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); }
h1, h2, h3 { font-weight: 700; }
h1 { color: var(--primary); }
.card {
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
}
.btn-primary {
  background: var(--primary);
  color: #0f172a;
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover { background: var(--accent); transform: translateY(-1px); }
"""
,

    "ocean": """
/* ===== Ocean Theme - 海洋清新 ===== */
:root {
  --primary: #0891b2;
  --secondary: #06b6d4;
  --accent: #22d3ee;
  --bg: #f0fdfa;
  --bg-alt: #ccfbf1;
  --text: #134e4a;
  --text-light: #0f766e;
  --border: #99f6e4;
  --success: #10b981;
  --gradient-ocean: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #22d3ee 100%);
  --shadow: 0 4px 15px rgba(6, 182, 212, 0.15);
  --shadow-lg: 0 20px 40px rgba(6, 182, 212, 0.25);
  --radius: 16px;
}
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); }
h1 {
  background: var(--gradient-ocean);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
}
h2, h3 { font-weight: 700; color: var(--primary); }
.section-title::after {
  background: var(--gradient-ocean);
}
.card {
  background: white;
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.btn-primary {
  background: var(--gradient-ocean);
  color: white;
  padding: 0.75rem 2rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.summary-number {
  background: var(--gradient-ocean);
}
.toc-item:hover {
  background: var(--gradient-ocean);
  color: white;
}
""",

    "sunset": """
/* ===== Sunset Theme - 日落暖橙 ===== */
:root {
  --primary: #ea580c;
  --secondary: #f97316;
  --accent: #fb923c;
  --bg: #fffbeb;
  --bg-alt: #fef3c7;
  --text: #78350f;
  --text-light: #92400e;
  --border: #fde68a;
  --success: #65a30d;
  --gradient-sunset: linear-gradient(135deg, #ea580c 0%, #f97316 50%, #fbbf24 100%);
  --shadow: 0 4px 15px rgba(249, 115, 22, 0.15);
  --shadow-lg: 0 20px 40px rgba(249, 115, 22, 0.25);
  --radius: 20px;
}
body { font-family: 'Georgia', serif; background: var(--bg); color: var(--text); }
h1 {
  background: var(--gradient-sunset);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-style: italic;
}
h2, h3 { font-weight: 700; color: var(--primary); font-style: italic; }
.section-title::after {
  background: var(--gradient-sunset);
}
.card {
  background: white;
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  border: 2px solid var(--border);
}
.btn-primary {
  background: var(--gradient-sunset);
  color: white;
  padding: 0.875rem 2.5rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-style: italic;
}
.btn-primary:hover { transform: translateY(-2px) scale(1.02); box-shadow: var(--shadow-lg); }
.summary-number {
  background: var(--gradient-sunset);
}
.toc-item {
  border-left: 4px solid var(--primary);
}
.toc-item:hover {
  background: var(--gradient-sunset);
  color: white;
  border-left-color: transparent;
}
""",

    "forest": """
/* ===== Forest Theme - 森林自然 ===== */
:root {
  --primary: #15803d;
  --secondary: #22c55e;
  --accent: #4ade80;
  --bg: #f0fdf4;
  --bg-alt: #dcfce7;
  --text: #14532d;
  --text-light: #166534;
  --border: #bbf7d0;
  --success: #15803d;
  --gradient-forest: linear-gradient(135deg, #14532d 0%, #15803d 50%, #22c55e 100%);
  --shadow: 0 4px 12px rgba(21, 128, 61, 0.15);
  --shadow-lg: 0 20px 40px rgba(21, 128, 61, 0.25);
  --radius: 12px;
}
body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
}
h1 {
  color: var(--primary);
  font-weight: 300;
  letter-spacing: -0.02em;
}
h2 {
  color: var(--primary);
  font-weight: 400;
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.5rem;
}
h3 { font-weight: 500; color: var(--secondary); }
.section-title::after {
  display: none;
}
.card {
  background: white;
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--primary);
}
.section-body li::before {
  content: '🌿';
  color: var(--success);
  font-size: 1rem;
  left: 0;
  top: 0;
}
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.75rem 2rem;
  border-radius: var(--radius);
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 0.05em;
}
.btn-primary:hover {
  background: var(--secondary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
.summary-number {
  background: var(--gradient-forest);
  border-radius: 8px;
}
.toc-item {
  transition: all 0.3s;
}
.toc-item:hover {
  background: var(--bg-alt);
  color: var(--primary);
  padding-left: 2rem;
}
.toc-item:hover .toc-number {
  color: var(--primary);
}
"""
}


# ============================================================
# HTML 页面模板
# ============================================================

def get_cover_slide(title, subtitle, author, date):
    """封面页模板"""
    return f"""
    <section class="slide cover-slide active" data-index="0">
      <div class="slide-content">
        <h1 class="cover-title">{title}</h1>
        <p class="cover-subtitle">{subtitle}</p>
        <div class="cover-meta">
          <span class="cover-author">{author}</span>
          <span class="cover-divider">·</span>
          <span class="cover-date">{date}</span>
        </div>
      </div>
    </section>
    """


def get_toc_slide(sections):
    """目录页模板"""
    items_html = ""
    for i, section in enumerate(sections, 1):
        heading = section.get("heading", f"第{i}部分")
        items_html += f"""
        <div class="toc-item">
          <span class="toc-number">{i:02d}</span>
          <span class="toc-title">{heading}</span>
        </div>"""

    return f"""
    <section class="slide toc-slide" data-index="1">
      <div class="slide-content">
        <h2 class="section-title">目录 / Contents</h2>
        <div class="toc-list">
          {items_html}
        </div>
      </div>
    </section>
    """


def get_content_slide(section, slide_index):
    """内容页模板"""
    heading = section.get("heading", "")
    content = section.get("content", [])

    body_html = ""
    for item in content:
        item_type = item.get("type", "paragraph")
        if item_type == "paragraph":
            body_html += f'<p class="content-paragraph">{item["text"]}</p>\n'
        elif item_type == "list_item":
            body_html += f'<li class="content-list-item">{item["text"]}</li>\n'
        elif item_type == "quote":
            body_html += f'<blockquote class="content-quote">{item["text"]}</blockquote>\n'
        elif item_type == "image":
            body_html += f'<img src="{item["url"]}" alt="{item["alt"]}" class="content-image">\n'
        elif item_type == "subsection":
            sub_heading = item.get("heading", "")
            sub_content = ""
            for sub_item in item.get("content", []):
                if sub_item.get("type") == "list_item":
                    sub_content += f'<li>{sub_item["text"]}</li>\n'
                elif sub_item.get("type") == "paragraph":
                    sub_content += f'<p>{sub_item["text"]}</p>\n'
            body_html += f"""
            <div class="subsection">
              <h4>{sub_heading}</h4>
              {sub_content}
            </div>"""

    # 如果有列表项，用ul包裹
    if "<li " in body_html or "<li>" in body_html:
        # 简单处理：找到li部分包装
        pass

    return f"""
    <section class="slide content-slide" data-index="{slide_index}">
      <div class="slide-content">
        <h2 class="section-title">{heading}</h2>
        <div class="section-body">
          {body_html}
        </div>
      </div>
    </section>
    """


def get_summary_slide(key_points):
    """总结页模板"""
    points_html = ""
    for i, point in enumerate(key_points, 1):
        points_html += f"""
        <div class="summary-item">
          <span class="summary-number">{i}</span>
          <span class="summary-text">{point}</span>
        </div>"""

    return f"""
    <section class="slide summary-slide" data-index="-2">
      <div class="slide-content">
        <h2 class="section-title">核心要点回顾</h2>
        <div class="summary-list">
          {points_html}
        </div>
      </div>
    </section>
    """


def get_end_slide(author=""):
    """结尾Q&A页模板"""
    author_html = f'<p class="end-author">{author}</p>' if author else ''
    return f"""
    <section class="slide end-slide" data-index="-1">
      <div class="slide-content">
        <h1 class="end-title">Q & A</h1>
        <p class="end-subtitle">感谢聆听 · 欢迎提问</p>
        {author_html}
      </div>
    </section>
    """


# ============================================================
# 全局 CSS 和 JS
# ============================================================

GLOBAL_CSS = """
/* ===== 全局基础样式 ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

/* 幻灯片容器 */
.slides-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

/* 单张幻灯片 */
.slide {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateX(100%);
  padding: 60px 80px;
}

.slide.active {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.slide.prev {
  transform: translateX(-100%);
}

/* 幻灯片内容 */
.slide-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

/* 标题样式 */
.section-title {
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  color: var(--text);
  position: relative;
  padding-bottom: 1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: var(--primary);
  border-radius: 2px;
}

.section-body {
  font-size: 1.25rem;
  line-height: 2;
  color: var(--text-light);
}

.section-body p { margin-bottom: 1.25rem; }
.section-body li { margin-bottom: 0.75rem; list-style: none; padding-left: 1.5rem; position: relative; }
.section-body li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--success);
  font-weight: bold;
}

.section-body blockquote {
  border-left: 4px solid var(--primary);
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  font-style: italic;
  background: var(--bg-alt);
  border-radius: 0 8px 8px 0;
}

/* 封面页 */
.cover-slide .slide-content {
  text-align: center;
}
.cover-title {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  line-height: 1.2;
}
.cover-subtitle {
  font-size: 1.5rem;
  color: var(--text-light);
  margin-bottom: 3rem;
}
.cover-meta {
  font-size: 1.1rem;
  color: var(--text-light);
}
.cover-divider { margin: 0 1rem; }

/* 目录页 */
.toc-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.toc-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: var(--bg-alt);
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
}
.toc-item:hover {
  transform: translateX(10px);
  background: var(--primary);
  color: white;
}
.toc-number {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary);
  min-width: 50px;
}
.toc-item:hover .toc-number { color: white; }
.toc-title { font-size: 1.25rem; }

/* 总结页 */
.summary-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.summary-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: var(--bg-alt);
  border-radius: 8px;
}
.summary-number {
  width: 40px;
  height: 40px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}
.summary-text { font-size: 1.15rem; }

/* 结尾页 */
.end-slide .slide-content {
  text-align: center;
}
.end-title {
  font-size: 5rem;
  margin-bottom: 1rem;
  background: var(--primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.end-subtitle {
  font-size: 1.5rem;
  color: var(--text-light);
  margin-bottom: 2rem;
}
.end-author {
  font-size: 1.1rem;
  color: var(--text-light);
}

/* 进度条 */
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: var(--primary);
  z-index: 1000;
  transition: width 0.3s ease;
}

/* 页码 */
.page-number {
  position: fixed;
  bottom: 20px;
  right: 30px;
  font-size: 0.9rem;
  color: var(--text-light);
  z-index: 1000;
}

/* 导航提示 */
.nav-hint {
  position: fixed;
  bottom: 20px;
  left: 30px;
  font-size: 0.85rem;
  color: var(--text-light);
  z-index: 1000;
  opacity: 0.7;
}

/* 响应式 */
@media (max-width: 768px) {
  .slide { padding: 40px 30px; }
  .section-title { font-size: 1.75rem; }
  .section-body { font-size: 1rem; }
  .cover-title { font-size: 2.5rem; }
  .end-title { font-size: 3.5rem; }
}

@media print {
  .slide {
    position: relative;
    opacity: 1;
    visibility: visible;
    transform: none;
    page-break-after: always;
    height: 100vh;
  }
  .progress-bar, .page-number, .nav-hint { display: none; }
}
"""

GLOBAL_JS = """
// ===== 幻灯片控制逻辑 =====
(function() {
  const slides = document.querySelectorAll('.slide');
  let currentIndex = 0;
  const totalSlides = slides.length;

  const progressBar = document.querySelector('.progress-bar');
  const pageNumber = document.querySelector('.page-number');

  function updateSlide(newIndex) {
    if (newIndex < 0 || newIndex >= totalSlides) return;

    slides.forEach((slide, i) => {
      slide.classList.remove('active', 'prev', 'next');
      if (i < newIndex) slide.classList.add('prev');
      else if (i === newIndex) slide.classList.add('active');
      else slide.classList.add('next');
    });

    currentIndex = newIndex;
    updateProgress();
    updatePageNumber();
  }

  function updateProgress() {
    const progress = ((currentIndex + 1) / totalSlides) * 100;
    progressBar.style.width = progress + '%';
  }

  function updatePageNumber() {
    pageNumber.textContent = (currentIndex + 1) + ' / ' + totalSlides;
  }

  function nextSlide() { updateSlide(currentIndex + 1); }
  function prevSlide() { updateSlide(currentIndex - 1); }
  function goToSlide(index) { updateSlide(index); }

  // 键盘导航
  document.addEventListener('keydown', (e) => {
    switch(e.key) {
      case 'ArrowRight':
      case ' ':
      case 'PageDown':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'Home':
        e.preventDefault();
        goToSlide(0);
        break;
      case 'End':
        e.preventDefault();
        goToSlide(totalSlides - 1);
        break;
      case 'f':
      case 'F':
        toggleFullscreen();
        break;
      case 'Escape':
        if (document.fullscreenElement) document.exitFullscreen();
        break;
    }
  });

  // 点击导航
  document.addEventListener('click', (e) => {
    const x = e.clientX;
    const width = window.innerWidth;
    if (x < width * 0.2) prevSlide();
    else if (x > width * 0.8) nextSlide();
  });

  // 触控滑动
  let touchStartX = 0;
  let touchEndX = 0;
  document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });
  document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) nextSlide();
      else prevSlide();
    }
  });

  // 全屏切换
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  // 目录点击跳转
  document.querySelectorAll('.toc-item').forEach((item, index) => {
    item.addEventListener('click', () => {
      goToSlide(index + 2); // 跳过封面和目录页
    });
  });

  // 初始化
  updateProgress();
  updatePageNumber();
})();
"""


def build_html_document(title, slides_html, theme="modern", author=""):
    """构建完整的HTML文档"""
    theme_css = CSS_THEMES.get(theme, CSS_THEMES["modern"])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    {theme_css}
    {GLOBAL_CSS}
  </style>
</head>
<body>
  <div class="progress-bar"></div>
  <div class="nav-hint">← → 翻页 · F 全屏 · 点击左右边缘导航</div>
  <div class="page-number">1 / 1</div>

  <div class="slides-container">
    {slides_html}
  </div>

  <script>
    {GLOBAL_JS}
  </script>
</body>
</html>
"""
