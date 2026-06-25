#!/usr/bin/env python3
"""
save-info.py - 文章信息保存脚本

功能：
1. 接收用户输入的文章信息
2. 验证必填字段
3. 生成时间戳和唯一ID
4. 保存为JSON格式文件
5. 输出文件路径供下一阶段使用

使用方法：
    python save-info.py --topic "..." --audience "..." --style "..." --length "..." --key-points "p1,p2,p3"
    python save-info.py --interactive  # 交互式输入模式
    python save-info.py --from-json input.json  # 从已有JSON导入
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import uuid


# 默认存储目录
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent / "data"

# 必填字段
REQUIRED_FIELDS = ["topic", "audience", "style", "length", "key_points"]

# 风格选项
STYLE_OPTIONS = ["专业严谨", "通俗易懂", "故事化叙事", "观点评论", "教程指南"]

# 长度选项
LENGTH_OPTIONS = ["500-1000字", "1500-2000字", "3000-5000字", "5000字以上"]


def validate_info(info: dict) -> tuple[bool, str]:
    """验证信息完整性"""
    for field in REQUIRED_FIELDS:
        if field not in info or not info[field]:
            return False, f"缺少必填字段: {field}"

    if info.get("style") and info["style"] not in STYLE_OPTIONS:
        return False, f"风格必须是以下之一: {', '.join(STYLE_OPTIONS)}"

    if info.get("length") and info["length"] not in LENGTH_OPTIONS:
        return False, f"长度必须是以下之一: {', '.join(LENGTH_OPTIONS)}"

    if isinstance(info.get("key_points"), str):
        info["key_points"] = [p.strip() for p in info["key_points"].split(",") if p.strip()]

    if not isinstance(info.get("key_points"), list) or len(info["key_points"]) < 1:
        return False, "核心要点至少需要1个"

    return True, ""


def interactive_mode() -> dict:
    """交互式输入模式"""
    print("=" * 50)
    print("📝 文章信息收集 - 交互式输入模式")
    print("=" * 50)

    info = {}

    info["topic"] = input("\n📌 请输入文章主题: ").strip()
    info["audience"] = input("👥 请输入目标受众: ").strip()

    print("\n✍️  请选择写作风格:")
    for i, style in enumerate(STYLE_OPTIONS, 1):
        print(f"   {i}) {style}")
    style_idx = int(input("请输入选项编号 (1-5): ")) - 1
    info["style"] = STYLE_OPTIONS[style_idx]

    print("\n📏 请选择文章长度:")
    for i, length in enumerate(LENGTH_OPTIONS, 1):
        print(f"   {i}) {length}")
    length_idx = int(input("请输入选项编号 (1-4): ")) - 1
    info["length"] = LENGTH_OPTIONS[length_idx]

    print("\n🎯 请输入核心要点 (用逗号分隔，至少1个):")
    key_points_input = input("   ").strip()
    info["key_points"] = [p.strip() for p in key_points_input.split(",") if p.strip()]

    return info


def save_info(info: dict, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    """保存信息到JSON文件"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 添加元数据
    info["timestamp"] = datetime.now().isoformat()
    info["session_id"] = str(uuid.uuid4())[:8]
    info["version"] = "1.0"

    # 生成文件名
    safe_topic = "".join(c for c in info["topic"] if c.isalnum() or c in ("-", "_"))[:20]
    filename = f"article-info-{safe_topic}-{info['session_id']}.json"
    output_path = output_dir / filename

    # 保存文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    return output_path


def print_summary(info: dict, output_path: Path):
    """打印信息摘要"""
    print("\n" + "=" * 50)
    print("✅ 信息收集完成！")
    print("=" * 50)
    print(f"📌 主题: {info['topic']}")
    print(f"👥 受众: {info['audience']}")
    print(f"✍️  风格: {info['style']}")
    print(f"📏 长度: {info['length']}")
    print(f"🎯 要点:")
    for i, point in enumerate(info['key_points'], 1):
        print(f"   {i}. {point}")
    print(f"\n📄 文件已保存至: {output_path}")
    print(f"🔑 会话ID: {info['session_id']}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="文章信息收集与保存工具")
    parser.add_argument("--topic", help="文章主题")
    parser.add_argument("--audience", help="目标受众")
    parser.add_argument("--style", choices=STYLE_OPTIONS, help="写作风格")
    parser.add_argument("--length", choices=LENGTH_OPTIONS, help="文章长度")
    parser.add_argument("--key-points", help="核心要点（逗号分隔）")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式输入模式")
    parser.add_argument("--from-json", help="从已有JSON文件导入")
    parser.add_argument("--output", "-o", help="自定义输出目录")

    args = parser.parse_args()

    # 模式选择
    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as f:
            info = json.load(f)
    elif args.interactive:
        info = interactive_mode()
    elif all([args.topic, args.audience, args.style, args.length, args.key_points]):
        info = {
            "topic": args.topic,
            "audience": args.audience,
            "style": args.style,
            "length": args.length,
            "key_points": args.key_points.split(",")
        }
    else:
        print("❌ 参数不完整，请使用 --interactive 进入交互模式，或提供所有必填参数")
        print("\n示例:")
        print('  python save-info.py -i')
        print('  python save-info.py --topic "AI应用" --audience "开发者" --style "专业严谨" --length "1500-2000字" --key-points "原理,场景,趋势"')
        sys.exit(1)

    # 验证
    valid, msg = validate_info(info)
    if not valid:
        print(f"❌ 验证失败: {msg}")
        sys.exit(1)

    # 保存
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    output_path = save_info(info, output_dir)

    # 输出摘要
    print_summary(info, output_path)


if __name__ == "__main__":
    main()
