#!/usr/bin/env python3
"""
gen-slides.py - HTML幻灯片生成主脚本

功能：
1. 读取结构化文章JSON
2. 自动拆分内容为幻灯片
3. 选择主题样式
4. 生成完整的单文件HTML幻灯片

使用方法：
    python gen-slides.py --input data/article-structured-xxx.json
    python gen-slides.py -i data.json --theme gradient
    python gen-slides.py -i data.json -o output/slides.html
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Optional, Any, Union

# 添加脚本目录到路径，以便导入模板
import importlib.util
_script_dir = Path(__file__).resolve().parent
_template_path = _script_dir / "html-templates.py"
_spec = importlib.util.spec_from_file_location("html_templates", _template_path)
html_templates = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(html_templates)

build_html_document = html_templates.build_html_document
get_cover_slide = html_templates.get_cover_slide
get_toc_slide = html_templates.get_toc_slide
get_content_slide = html_templates.get_content_slide
get_summary_slide = html_templates.get_summary_slide
get_end_slide = html_templates.get_end_slide


# 可用主题
AVAILABLE_THEMES = ["modern", "classic", "gradient", "minimal", "dark", "ocean", "sunset", "forest"]


def load_structured_article(input_path: Path) -> dict:
    """加载结构化文章JSON"""
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def estimate_content_length(content_items: list) -> int:
    """估算内容长度（字符数）"""
    total = 0
    for item in content_items:
        if "text" in item:
            total += len(item["text"])
        if item.get("type") == "subsection":
            total += estimate_content_length(item.get("content", []))
    return total


def split_section_to_slides(section: dict, start_index: int, max_chars_per_slide: int = 800) -> list:
    """将章节内容拆分为多个幻灯片"""
    heading = section.get("heading", "")
    content = section.get("content", [])

    # 估算总长度
    total_length = estimate_content_length(content)

    # 如果内容很少，一页搞定
    if total_length <= max_chars_per_slide:
        return [{"heading": heading, "content": content, "slide_index": start_index}]

    # 内容较多，需要拆分
    slides = []
    current_slide_content = []
    current_length = 0

    for item in content:
        item_length = len(item.get("text", ""))

        # 如果是子章节，作为一个整体
        if item.get("type") == "subsection":
            sub_length = estimate_content_length(item.get("content", []))
            if current_length + sub_length > max_chars_per_slide and current_slide_content:
                slides.append({
                    "heading": heading,
                    "content": current_slide_content,
                    "slide_index": start_index + len(slides)
                })
                current_slide_content = []
                current_length = 0
            current_slide_content.append(item)
            current_length += sub_length

        # 如果是列表项，逐行添加
        elif item.get("type") == "list_item":
            if current_length + item_length > max_chars_per_slide and current_slide_content:
                slides.append({
                    "heading": heading,
                    "content": current_slide_content,
                    "slide_index": start_index + len(slides)
                })
                current_slide_content = []
                current_length = 0
            current_slide_content.append(item)
            current_length += item_length

        # 其他类型直接添加
        else:
            if current_length + item_length > max_chars_per_slide and current_slide_content:
                slides.append({
                    "heading": heading,
                    "content": current_slide_content,
                    "slide_index": start_index + len(slides)
                })
                current_slide_content = []
                current_length = 0
            current_slide_content.append(item)
            current_length += item_length

    # 添加最后一页
    if current_slide_content:
        slides.append({
            "heading": heading,
            "content": current_slide_content,
            "slide_index": start_index + len(slides)
        })

    return slides


def build_all_slides(data: dict) -> Tuple[str, int]:
    """构建所有幻灯片"""
    metadata = data.get("metadata", {})
    content = data.get("content", {})
    sections = content.get("sections", [])
    key_points = content.get("key_points", [])

    title = metadata.get("title", content.get("title", "幻灯片"))
    subtitle = content.get("subtitle", "")
    author = metadata.get("author", "")
    date = metadata.get("date", datetime.now().strftime("%Y-%m-%d"))

    slides_html_parts = []
    current_slide_index = 0

    # 1. 封面页
    slides_html_parts.append(get_cover_slide(title, subtitle, author, date))
    current_slide_index += 1

    # 2. 目录页（如果章节>2）
    has_toc = len(sections) > 2
    if has_toc:
        slides_html_parts.append(get_toc_slide(sections))
        current_slide_index += 1

    # 3. 内容页（每个章节拆分为1-N页）
    max_chars = 600  # 每页最大字符数
    for section in sections:
        section_slides = split_section_to_slides(section, current_slide_index, max_chars)
        for slide in section_slides:
            slides_html_parts.append(get_content_slide(slide, slide["slide_index"]))
            current_slide_index += 1

    # 4. 总结页（如果有关键要点）
    has_summary = len(key_points) > 0
    if has_summary:
        slides_html_parts.append(get_summary_slide(key_points))
        current_slide_index += 1

    # 5. 结尾Q&A页
    slides_html_parts.append(get_end_slide(author))
    current_slide_index += 1

    slides_html = "\n".join(slides_html_parts)
    total_slides = len(slides_html_parts)

    return slides_html, total_slides


def save_slides(html: str, data: dict, output_dir: Path) -> Path:
    """保存幻灯片HTML"""
    output_dir.mkdir(parents=True, exist_ok=True)

    session_id = data.get("metadata", {}).get("session_id", "default")
    safe_title = re.sub(r'[^\w]', '_', data.get("metadata", {}).get("title", "slides"))[:20]
    filename = f"slides-{safe_title}-{session_id}.html"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def print_summary(output_path: Path, total_slides: int, theme: str):
    """打印摘要"""
    print("\n" + "=" * 60)
    print("✅ HTML幻灯片已生成！")
    print("=" * 60)
    print(f"📄 文件路径: {output_path}")
    print(f"🎨 使用主题: {theme}")
    print(f"📊 幻灯片数量: {total_slides} 页")
    print(f"📏 文件大小: {output_path.stat().st_size / 1024:.1f} KB")
    print("=" * 60)
    print("\n💡 使用提示:")
    print("   • 在浏览器中打开 HTML 文件即可查看")
    print("   • 使用 ← → 键翻页")
    print("   • 按 F 键进入全屏模式")
    print("   • 点击屏幕左右边缘也可翻页")
    print("   • 按 Esc 退出全屏")
    print("   • 支持触控滑动（移动端）")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="HTML幻灯片生成工具")
    parser.add_argument("--input", "-i", required=True, help="结构化文章JSON文件路径")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--theme", "-t",
                        choices=AVAILABLE_THEMES,
                        default="modern",
                        help=f"主题风格（默认: modern）可选: {', '.join(AVAILABLE_THEMES)}")
    parser.add_argument("--max-chars", type=int, default=600,
                        help="每页最大字符数（默认: 600）")
    parser.add_argument("--list-themes", action="store_true",
                        help="列出所有可用主题")

    args = parser.parse_args()

    # 列出主题
    if args.list_themes:
        print("\n🎨 可用主题:")
        for theme in AVAILABLE_THEMES:
            print(f"   • {theme}")
        print()
        return 0

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        return 1

    # 加载数据
    data = load_structured_article(input_path)
    title = data.get("metadata", {}).get("title",
              data.get("content", {}).get("title", "未命名文章"))
    print(f"\n📖 已加载文章: {title}")
    print(f"🎨 选择主题: {args.theme}")

    # 构建幻灯片
    slides_html, total_slides = build_all_slides(data)

    # 生成完整HTML
    author = data.get("metadata", {}).get("author", "")
    full_html = build_html_document(title, slides_html, args.theme, author)

    # 保存
    output_dir = Path(args.output) if args.output else input_path.parent
    output_path = save_slides(full_html, data, output_dir)

    # 输出摘要
    print_summary(output_path, total_slides, args.theme)

    return 0


if __name__ == "__main__":
    exit(main())
