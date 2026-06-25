#!/usr/bin/env python3
"""
gen-preview-index.py - 生成幻灯片预览索引页

列出 data/ 目录下的所有 slides-*.html 文件
生成一个可视化的预览导航页面
"""

import re
import sys
from pathlib import Path
from datetime import datetime


def extract_slide_info(html_file: Path) -> dict:
    """从HTML文件提取幻灯片信息"""
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取标题
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else html_file.stem

        # 提取主题
        theme_match = re.search(r'/\* ===== (\w+) Theme', content)
        theme = theme_match.group(1) if theme_match else "未知"

        # 统计幻灯片页数
        slide_count = content.count('class="slide')

        # 文件大小
        size_kb = html_file.stat().st_size / 1024

        return {
            "title": title,
            "theme": theme,
            "slide_count": slide_count,
            "size_kb": round(size_kb, 1),
            "file": html_file.name,
            "modified": datetime.fromtimestamp(html_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "title": html_file.stem,
            "theme": "错误",
            "slide_count": 0,
            "size_kb": 0,
            "file": html_file.name,
            "modified": "",
            "error": str(e)
        }


def generate_index_html(slides: list) -> str:
    """生成索引页HTML"""
    cards_html = ""
    for i, slide in enumerate(slides, 1):
        theme_color = {
            "Modern": "#2563eb",
            "Classic": "#1e3a5f",
            "Gradient": "#8b5cf6",
            "Minimal": "#000000",
            "Dark": "#60a5fa",
            "Ocean": "#0891b2",
            "Sunset": "#ea580c",
            "Forest": "#15803d"
        }.get(slide["theme"], "#64748b")

        cards_html += f"""
        <div class="card" style="--theme-color: {theme_color};">
          <div class="card-header">
            <span class="card-number">#{i:02d}</span>
            <span class="card-theme">{slide['theme']} 主题</span>
          </div>
          <h3 class="card-title">{slide['title']}</h3>
          <div class="card-meta">
            <div class="meta-item">
              <span class="meta-icon">📄</span>
              <span>{slide['slide_count']} 页幻灯片</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">💾</span>
              <span>{slide['size_kb']} KB</span>
            </div>
            <div class="meta-item">
              <span class="meta-icon">🕒</span>
              <span>{slide['modified']}</span>
            </div>
          </div>
          <a href="{slide['file']}" target="_blank" class="card-btn">
            🚀 打开预览
          </a>
        </div>"""
        if i < len(slides):
            cards_html += "\n"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎨 幻灯片预览索引</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 40px 20px;
      color: #1e293b;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    .header {{
      text-align: center;
      color: white;
      margin-bottom: 50px;
    }}
    .header h1 {{
      font-size: 3rem;
      margin-bottom: 10px;
      font-weight: 800;
    }}
    .header p {{
      font-size: 1.2rem;
      opacity: 0.9;
    }}
    .stats {{
      display: flex;
      justify-content: center;
      gap: 30px;
      margin-bottom: 40px;
      flex-wrap: wrap;
    }}
    .stat {{
      background: rgba(255,255,255,0.2);
      backdrop-filter: blur(10px);
      padding: 15px 30px;
      border-radius: 12px;
      color: white;
      text-align: center;
    }}
    .stat-num {{
      font-size: 2rem;
      font-weight: bold;
      display: block;
    }}
    .stat-label {{
      font-size: 0.9rem;
      opacity: 0.9;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 25px;
    }}
    .card {{
      background: white;
      border-radius: 16px;
      padding: 25px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.2);
      transition: all 0.3s ease;
      border-top: 4px solid var(--theme-color, #2563eb);
    }}
    .card:hover {{
      transform: translateY(-8px);
      box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }}
    .card-number {{
      font-size: 1.5rem;
      font-weight: 800;
      color: #94a3b8;
    }}
    .card-theme {{
      font-size: 0.85rem;
      background: var(--theme-color);
      color: white;
      padding: 4px 12px;
      border-radius: 12px;
      font-weight: 600;
    }}
    .card-title {{
      font-size: 1.3rem;
      color: #1e293b;
      margin-bottom: 20px;
      line-height: 1.4;
    }}
    .card-meta {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding: 15px 0;
      border-top: 1px solid #e2e8f0;
      border-bottom: 1px solid #e2e8f0;
      margin-bottom: 20px;
    }}
    .meta-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.9rem;
      color: #64748b;
    }}
    .meta-icon {{
      font-size: 1rem;
    }}
    .card-btn {{
      display: block;
      text-align: center;
      background: var(--theme-color);
      color: white;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 10px;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .card-btn:hover {{
      transform: scale(1.05);
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    .footer {{
      text-align: center;
      color: white;
      margin-top: 50px;
      opacity: 0.8;
    }}
    .footer a {{
      color: white;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎨 幻灯片预览索引</h1>
      <p>内容生产工作流 · Skill 3 输出</p>
    </div>

    <div class="stats">
      <div class="stat">
        <span class="stat-num">{len(slides)}</span>
        <span class="stat-label">幻灯片文件</span>
      </div>
      <div class="stat">
        <span class="stat-num">{sum(s['slide_count'] for s in slides)}</span>
        <span class="stat-label">总页数</span>
      </div>
      <div class="stat">
        <span class="stat-num">{len(set(s['theme'] for s in slides))}</span>
        <span class="stat-label">不同主题</span>
      </div>
    </div>

    <div class="grid">
      {cards_html}
    </div>

    <div class="footer">
      <p>💡 点击任意卡片打开对应幻灯片 | 使用 ← → 键翻页 | F 键全屏</p>
      <p style="margin-top: 10px;">
        📅 生成于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
        由 content-workflow 自动化生成
      </p>
    </div>
  </div>
</body>
</html>
"""
    return html


def main():
    data_dir = Path(__file__).parent / "data"

    if not data_dir.exists():
        print(f"❌ 目录不存在: {data_dir}")
        return 1

    # 查找所有 slides HTML
    slide_files = sorted(data_dir.glob("slides-*.html"))

    if not slide_files:
        print("❌ 没有找到 slides HTML 文件")
        return 1

    print(f"📁 找到 {len(slide_files)} 个幻灯片文件")

    # 提取信息
    slides = [extract_slide_info(f) for f in slide_files]

    # 生成索引页
    index_html = generate_index_html(slides)

    # 保存
    index_path = data_dir / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"✅ 索引页已生成: {index_path}")
    print(f"🌐 访问地址: http://localhost:8000/ (启动 start-server.py 后)")

    return 0


if __name__ == "__main__":
    exit(main())
