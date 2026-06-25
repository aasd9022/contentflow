#!/usr/bin/env python3
"""
gen-outline.py - 文章大纲生成脚本

功能：
1. 读取 Skill 1 生成的 article-info JSON
2. 基于风格和要点生成结构化大纲
3. 支持模板生成和AI生成两种模式
4. 输出 Markdown 格式大纲

使用方法：
    python gen-outline.py --info data/article-info-xxx.json
    python gen-outline.py --info data/article-info-xxx.json --output custom-outline.md
    python gen-outline.py --info data/article-info-xxx.json --ai  # 调用AI生成
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


# 风格对应的大纲模板
OUTLINE_TEMPLATES = {
    "专业严谨": {
        "sections": ["引言", "研究背景", "方法论", "实验分析", "讨论", "结论"],
        "subsections": 2,
        "intro_words": 200,
        "conclusion_words": 200
    },
    "通俗易懂": {
        "sections": ["引言", "什么是{topic}", "为什么重要", "具体例子", "如何应用", "总结"],
        "subsections": 1,
        "intro_words": 200,
        "conclusion_words": 150
    },
    "故事化叙事": {
        "sections": ["引子", "开端", "发展", "转折", "高潮", "结局", "启示"],
        "subsections": 1,
        "intro_words": 250,
        "conclusion_words": 200
    },
    "观点评论": {
        "sections": ["引言", "现象描述", "核心观点", "论据1", "论据2", "反驳与回应", "总结"],
        "subsections": 1,
        "intro_words": 200,
        "conclusion_words": 200
    },
    "教程指南": {
        "sections": ["目标说明", "前置准备", "步骤详解", "常见问题", "进阶技巧", "总结"],
        "subsections": 3,
        "intro_words": 150,
        "conclusion_words": 150
    }
}


def load_info(info_path: Path) -> dict:
    """加载文章信息JSON"""
    with open(info_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_outline_template(info: dict) -> str:
    """基于模板生成大纲"""
    style = info.get("style", "通俗易懂")
    topic = info.get("topic", "")
    key_points = info.get("key_points", [])

    template = OUTLINE_TEMPLATES.get(style, OUTLINE_TEMPLATES["通俗易懂"])

    # 生成标题
    title = f"{topic}：深度解析与实践指南"
    subtitle = f"面向{info.get('audience', '广大读者')}的{style}内容"

    # 构建大纲
    outline = f"# {title}\n\n"
    outline += f"> {subtitle}\n\n"
    outline += f"**字数目标**: {info.get('length', '1500-2000字')} | "
    outline += f"**目标受众**: {info.get('audience', '')} | "
    outline += f"**写作风格**: {style}\n\n"
    outline += "---\n\n"

    # 引言部分
    outline += f"## 引言 (约{template['intro_words']}字)\n\n"
    outline += f"- **背景引入**：从{topic}的现实意义出发\n"
    outline += f"- **核心问题**：提出本文要解决的关键问题\n"
    outline += f"- **文章结构**：简要说明文章的组织逻辑\n\n"

    # 主体部分
    for i, section_name in enumerate(template["sections"][1:-1], 1):
        outline += f"## 第{i}部分：{section_name}\n\n"

        # 根据key_points分配到各个section
        if i <= len(key_points):
            outline += f"### 核心要点：{key_points[i-1]}\n\n"
            outline += f"- 论据1：相关数据或案例\n"
            outline += f"- 论据2：具体分析\n"
            outline += f"- 小结：本节核心观点\n\n"
        else:
            for j in range(1, template["subsections"] + 1):
                outline += f"### {j}.{i} 子主题{j}\n\n"
                outline += f"- 内容要点1\n"
                outline += f"- 内容要点2\n\n"

    # 结论部分
    outline += f"## 结论 (约{template['conclusion_words']}字)\n\n"
    outline += f"- **核心观点总结**：回顾本文核心论点\n"
    outline += f"- **实践建议**：给{info.get('audience', '读者')}的actionable建议\n"
    outline += f"- **未来展望**：{topic}的发展方向\n\n"

    # 核心要点检查清单
    outline += "---\n\n"
    outline += "## 📋 核心要点覆盖检查\n\n"
    for i, point in enumerate(key_points, 1):
        outline += f"- [ ] 要点{i}：{point}\n"

    return outline


def add_metadata(outline: str, info: dict) -> str:
    """添加YAML元数据"""
    metadata = "---\n"
    metadata += f"title: \"{info.get('topic', '')}\"\n"
    metadata += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    metadata += f"style: {info.get('style', '')}\n"
    metadata += f"length: {info.get('length', '')}\n"
    metadata += f"audience: {info.get('audience', '')}\n"
    metadata += f"key_points:\n"
    for p in info.get("key_points", []):
        metadata += f"  - {p}\n"
    metadata += f"session_id: {info.get('session_id', '')}\n"
    metadata += "---\n\n"
    return metadata + outline


def save_outline(outline: str, info: dict, output_dir: Path) -> Path:
    """保存大纲"""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_topic = re.sub(r'[^\w]', '_', info.get("topic", "article"))[:20]
    session_id = info.get("session_id", "default")
    filename = f"outline-{safe_topic}-{session_id}.md"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(outline)

    return output_path


def print_summary(outline: str, output_path: Path):
    """打印摘要"""
    print("\n" + "=" * 60)
    print("✅ 文章大纲已生成！")
    print("=" * 60)
    print(f"📄 文件路径: {output_path}")
    print(f"📊 字数估算: ~{len(outline) * 4}字（中文1字符≈2-3字）")
    print("=" * 60)
    print("\n📑 大纲预览（前30行）：\n")
    print("\n".join(outline.split("\n")[:30]))
    print("\n...")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="文章大纲生成工具")
    parser.add_argument("--info", "-i", required=True, help="文章信息JSON文件路径")
    parser.add_argument("--output", "-o", help="输出目录（默认: data/）")
    parser.add_argument("--no-metadata", action="store_true", help="不添加YAML元数据")
    parser.add_argument("--ai", action="store_true", help="使用AI生成（需要API）")

    args = parser.parse_args()

    info_path = Path(args.info)
    if not info_path.exists():
        print(f"❌ 文件不存在: {info_path}")
        return 1

    # 加载信息
    info = load_info(info_path)
    print(f"\n📖 已加载文章信息:")
    print(f"   主题: {info.get('topic', '')}")
    print(f"   风格: {info.get('style', '')}")
    print(f"   要点数: {len(info.get('key_points', []))}")

    # 生成大纲
    if args.ai:
        print("\n⚠️  AI模式需要配置API key，请参考prompt-templates.md手动调用AI")
        print("   临时使用模板模式生成基础大纲...")

    outline = generate_outline_template(info)

    # 添加元数据
    if not args.no_metadata:
        outline = add_metadata(outline, info)

    # 保存
    output_dir = Path(args.output) if args.output else info_path.parent
    output_path = save_outline(outline, info, output_dir)

    # 输出摘要
    print_summary(outline, output_path)

    return 0


if __name__ == "__main__":
    exit(main())
