#!/usr/bin/env python3
"""
md-to-json.py - Markdown转JSON脚本

功能：
1. 解析Markdown文章文件
2. 提取YAML元数据
3. 分割文章结构（标题、段落、图片等）
4. 输出结构化JSON供Skill 3使用

使用方法：
    python md-to-json.py --input data/article-xxx.md
    python md-to-json.py --input data/article-xxx.md --output data/article-xxx.json
"""

import argparse
import json
import re
from pathlib import Path
from typing import Optional, Tuple


def parse_yaml_front_matter(content: str) -> Tuple[dict, str]:
    """解析YAML前置元数据"""
    metadata = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            body = parts[2].strip()

            # 简单YAML解析
            current_list_key = None
            for line in yaml_content.split("\n"):
                line = line.rstrip()
                if not line:
                    continue

                if line.startswith("  - ") and current_list_key:
                    value = line.strip()[2:].strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    metadata[current_list_key].append(value)
                elif ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if value == "":
                        metadata[key] = []
                        current_list_key = key
                    else:
                        current_list_key = None
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        metadata[key] = value

    return metadata, body


def parse_markdown_structure(body: str) -> dict:
    """解析Markdown结构"""
    lines = body.split("\n")
    structure = {
        "title": "",
        "subtitle": "",
        "sections": [],
        "stats": {
            "total_chars": 0,
            "h1_count": 0,
            "h2_count": 0,
            "h3_count": 0,
            "paragraph_count": 0,
            "image_count": 0
        }
    }

    current_section: Optional[dict] = None
    current_subsection: Optional[dict] = None
    current_paragraph: list = []

    def flush_paragraph():
        if current_paragraph and current_section:
            text = " ".join(current_paragraph).strip()
            if text:
                if current_subsection:
                    current_subsection["content"].append({"type": "paragraph", "text": text})
                else:
                    current_section["content"].append({"type": "paragraph", "text": text})
                structure["stats"]["paragraph_count"] += 1
            current_paragraph.clear()

    for line in lines:
        line_stripped = line.rstrip()

        if not line_stripped:
            flush_paragraph()
            continue

        # H1 标题
        if line_stripped.startswith("# ") and not line_stripped.startswith("## "):
            flush_paragraph()
            structure["title"] = line_stripped[2:].strip()
            structure["stats"]["h1_count"] += 1

        # H2 标题
        elif line_stripped.startswith("## ") and not line_stripped.startswith("### "):
            flush_paragraph()
            current_section = {
                "type": "section",
                "heading": line_stripped[3:].strip(),
                "level": 2,
                "content": []
            }
            structure["sections"].append(current_section)
            current_subsection = None
            structure["stats"]["h2_count"] += 1

        # H3 标题
        elif line_stripped.startswith("### "):
            flush_paragraph()
            if current_section is None:
                current_section = {
                    "type": "section",
                    "heading": "引言",
                    "level": 2,
                    "content": []
                }
                structure["sections"].append(current_section)

            current_subsection = {
                "type": "subsection",
                "heading": line_stripped[4:].strip(),
                "level": 3,
                "content": []
            }
            current_section["content"].append(current_subsection)
            structure["stats"]["h3_count"] += 1

        # 引用
        elif line_stripped.startswith(">"):
            flush_paragraph()
            quote_text = line_stripped[1:].strip()
            if current_subsection:
                current_subsection["content"].append({"type": "quote", "text": quote_text})
            elif current_section:
                current_section["content"].append({"type": "quote", "text": quote_text})
            else:
                if not structure["subtitle"]:
                    structure["subtitle"] = quote_text

        # 列表
        elif re.match(r'^\s*[-*+]\s+', line_stripped):
            flush_paragraph()
            item_text = re.sub(r'^\s*[-*+]\s+', '', line_stripped)
            list_item = {"type": "list_item", "text": item_text}
            if current_subsection:
                current_subsection["content"].append(list_item)
            elif current_section:
                current_section["content"].append(list_item)

        # 图片
        elif line_stripped.startswith("!["):
            flush_paragraph()
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line_stripped)
            if match:
                structure["stats"]["image_count"] += 1
                image = {"type": "image", "alt": match.group(1), "url": match.group(2)}
                if current_subsection:
                    current_subsection["content"].append(image)
                elif current_section:
                    current_section["content"].append(image)

        # 普通段落
        else:
            current_paragraph.append(line_stripped)
            structure["stats"]["total_chars"] += len(line_stripped)

    flush_paragraph()

    # 提取核心要点
    structure["key_points"] = []
    for section in structure["sections"]:
        if "要点" in section.get("heading", "") or "核心" in section.get("heading", ""):
            for item in section.get("content", []):
                if item.get("type") == "list_item":
                    structure["key_points"].append(item["text"])

    return structure


def merge_metadata_and_structure(metadata: dict, structure: dict) -> dict:
    """合并元数据和结构"""
    result = {
        "metadata": {
            "title": metadata.get("title", structure["title"]),
            "date": metadata.get("date", ""),
            "author": metadata.get("author", ""),
            "style": metadata.get("style", ""),
            "audience": metadata.get("audience", ""),
            "length": metadata.get("length", ""),
            "description": metadata.get("description", ""),
            "keywords": metadata.get("keywords", []),
            "tags": metadata.get("tags", []),
            "session_id": metadata.get("session_id", "")
        },
        "content": structure,
        "slides_hint": {
            "recommended_slide_count": len(structure["sections"]) + 2,  # 标题页+章节页+结尾页
            "title_slide": True,
            "toc_slide": len(structure["sections"]) > 3,
            "summary_slide": True
        }
    }
    return result


def save_json(data: dict, input_path: Path, output_dir: Optional[Path] = None) -> Path:
    """保存JSON"""
    if output_dir is None:
        output_dir = input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    session_id = data["metadata"].get("session_id", "default")
    filename = f"article-structured-{session_id}.json"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def print_summary(data: dict, output_path: Path):
    """打印摘要"""
    print("\n" + "=" * 60)
    print("✅ Markdown已转为JSON结构！")
    print("=" * 60)
    print(f"📄 文件路径: {output_path}")
    print(f"📖 标题: {data['content']['title']}")
    print(f"📊 章节数: {len(data['content']['sections'])}")
    print(f"📊 段落数: {data['content']['stats']['paragraph_count']}")
    print(f"📊 字符数: {data['content']['stats']['total_chars']}")
    print(f"🎯 建议幻灯片数: {data['slides_hint']['recommended_slide_count']}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Markdown转JSON结构化工具")
    parser.add_argument("--input", "-i", required=True, help="输入Markdown文件")
    parser.add_argument("--output", "-o", help="输出目录")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        return 1

    # 读取文件
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析YAML和正文
    metadata, body = parse_yaml_front_matter(content)
    print(f"\n📋 元数据解析: {len(metadata)} 个字段")

    # 解析结构
    structure = parse_markdown_structure(body)
    print(f"📑 结构解析: {len(structure['sections'])} 个章节")

    # 合并数据
    result = merge_metadata_and_structure(metadata, structure)

    # 保存
    output_dir = Path(args.output) if args.output else None
    output_path = save_json(result, input_path, output_dir)

    # 输出摘要
    print_summary(result, output_path)

    return 0


if __name__ == "__main__":
    exit(main())
