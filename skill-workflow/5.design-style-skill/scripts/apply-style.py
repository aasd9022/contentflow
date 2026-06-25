#!/usr/bin/env python3
"""
设计风格应用脚本
将Design Token或预设风格应用到HTML文件
"""

import json
import argparse
import re
import os

STYLE_TEMPLATES = {
    "glassmorphism": {
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "surface": "rgba(255, 255, 255, 0.15)",
        "surface-hover": "rgba(255, 255, 255, 0.25)",
        "text": "#ffffff",
        "border": "1px solid rgba(255, 255, 255, 0.2)",
        "shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
        "backdrop-filter": "blur(10px)",
        "font": "Inter, system-ui, sans-serif"
    },
    "minimal": {
        "background": "#fafafa",
        "surface": "#ffffff",
        "surface-hover": "#f5f5f5",
        "text": "#1a1a1a",
        "text-secondary": "#666666",
        "border": "1px solid #e0e0e0",
        "shadow": "0 1px 3px rgba(0, 0, 0, 0.04)",
        "font": "Inter, system-ui, sans-serif"
    },
    "elegant": {
        "background": "#faf9f7",
        "surface": "#ffffff",
        "surface-hover": "#f8f7f5",
        "text": "#1a1c1e",
        "text-secondary": "#6c7278",
        "accent": "#8b7355",
        "border": "1px solid #e8e6e3",
        "shadow": "0 2px 8px rgba(0, 0, 0, 0.06)",
        "font": "Georgia, serif"
    },
    "dark": {
        "background": "#0b1326",
        "surface": "#171f33",
        "surface-hover": "#222a3d",
        "text": "#dae2fd",
        "text-secondary": "#c4c7c8",
        "accent": "#00a8e8",
        "border": "1px solid #2d3449",
        "shadow": "0 4px 16px rgba(0, 0, 0, 0.4)",
        "font": "Inter, system-ui, sans-serif"
    },
    "gradient": {
        "background": "linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)",
        "surface": "#ffffff",
        "surface-hover": "#f0f7ff",
        "text": "#1a1c1e",
        "text-secondary": "#6c7278",
        "accent": "#0077cc",
        "border": "1px solid rgba(0, 119, 204, 0.2)",
        "shadow": "0 4px 20px rgba(0, 119, 204, 0.15)",
        "font": "Inter, system-ui, sans-serif"
    },
    "corporate": {
        "background": "#f5f7fa",
        "surface": "#ffffff",
        "surface-hover": "#f8fafc",
        "text": "#1a1c1e",
        "text-secondary": "#6c7278",
        "accent": "#2563eb",
        "border": "1px solid #e2e8f0",
        "shadow": "0 1px 3px rgba(0, 0, 0, 0.05)",
        "font": "Inter, system-ui, sans-serif"
    }
}

def list_styles():
    """列出所有可用风格"""
    print("\n可用设计风格:")
    print("-" * 40)
    for name in STYLE_TEMPLATES.keys():
        print(f"  {name}")
    print()

def generate_css(style_name, custom_overrides=None):
    """生成CSS样式"""
    if style_name and style_name in STYLE_TEMPLATES:
        style = STYLE_TEMPLATES[style_name]
    else:
        style = STYLE_TEMPLATES["minimal"]

    if custom_overrides:
        style = {**style, **custom_overrides}

    css = f"""
    /* Design Style: {style_name} */
    :root {{
        --bg-primary: {style['background']};
        --bg-surface: {style['surface']};
        --bg-surface-hover: {style.get('surface-hover', style['surface'])};
        --color-text: {style['text']};
        --color-text-secondary: {style.get('text-secondary', style['text'])};
        --color-accent: {style.get('accent', '#0077cc')};
        --border-default: {style['border']};
        --shadow-default: {style['shadow']};
        --backdrop-filter: {style.get('backdrop-filter', 'none')};
        --font-primary: {style['font']};
    }}

    body {{
        background: var(--bg-primary);
        color: var(--color-text);
        font-family: var(--font-primary);
        transition: background var(--transition-normal, 0.25s);
    }}

    .slide {{
        background: var(--bg-surface);
        border: var(--border-default);
        box-shadow: var(--shadow-default);
        {f"backdrop-filter: var(--backdrop-filter);" if 'backdrop-filter' in style else ""}
    }}

    .slide:hover {{
        background: var(--bg-surface-hover);
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: var(--color-text);
    }}

    p, li {{
        color: var(--color-text-secondary);
    }}

    .accent {{ color: var(--color-accent); }}

    .btn-primary {{
        background: var(--color-accent);
        color: white;
        border-radius: 8px;
        transition: all 0.25s;
    }}

    .btn-primary:hover {{
        opacity: 0.9;
        transform: translateY(-1px);
    }}
    """
    return css

def inject_into_html(html_content, css, inject_mode='replace'):
    """将CSS注入HTML"""
    style_tag = f"<style>\n{css}\n</style>"

    if inject_mode == 'replace':
        # 替换已有的<style>标签
        pattern = r'<style[^>]*>.*?</style>'
        if re.search(pattern, html_content, re.DOTALL | re.IGNORECASE):
            html_content = re.sub(pattern, style_tag, html_content, count=1, flags=re.DOTALL | re.IGNORECASE)
        else:
            # 在</head>前插入
            html_content = html_content.replace('</head>', f'{style_tag}\n</head>')
    elif inject_mode == 'append':
        html_content = html_content.replace('</head>', f'{style_tag}\n</head>')

    return html_content

def load_html(input_path):
    """加载HTML文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_html(html_content, output_path):
    """保存HTML文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"已应用设计风格: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='应用设计风格到HTML')
    parser.add_argument('--input', '-i', required=True,
                        help='输入HTML文件路径')
    parser.add_argument('--output', '-o',
                        help='输出HTML文件路径')
    parser.add_argument('--style', '-s', choices=list(STYLE_TEMPLATES.keys()),
                        help='选择预设风格')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有可用风格')
    parser.add_argument('--inject-mode', default='replace',
                        choices=['replace', 'append'],
                        help='CSS注入模式')

    args = parser.parse_args()

    if args.list:
        list_styles()
        return

    if not args.style:
        print("错误: 请指定 --style 参数")
        list_styles()
        return

    # 生成CSS
    css = generate_css(args.style)

    # 加载HTML
    html = load_html(args.input)

    # 注入CSS
    html = inject_into_html(html, css, args.inject_mode)

    # 保存
    output_path = args.output or args.input
    save_html(html, output_path)

if __name__ == '__main__':
    main()
