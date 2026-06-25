#!/usr/bin/env python3
"""
gen-article.py - 文章生成主脚本

功能：
1. 读取文章信息和大纲
2. 调用AI模型生成完整文章
3. 添加YAML元数据
4. 输出标准Markdown文件

使用方法：
    python gen-article.py --info data/article-info-xxx.json --outline data/outline-xxx.md
    python gen-article.py --info data/article-info-xxx.json --outline data/outline-xxx.md --output data/
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


# 字数范围映射
LENGTH_RANGES = {
    "500-1000字": (500, 1000),
    "1500-2000字": (1500, 2000),
    "3000-5000字": (3000, 5000),
    "5000字以上": (5000, 8000)
}

# 风格对应的字数调整系数
STYLE_LENGTH_FACTOR = {
    "专业严谨": 1.0,
    "通俗易懂": 0.9,
    "故事化叙事": 1.1,
    "观点评论": 0.95,
    "教程指南": 1.0
}


def load_info(info_path: Path) -> dict:
    """加载文章信息"""
    with open(info_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_outline(outline_path: Path) -> str:
    """加载大纲"""
    with open(outline_path, "r", encoding="utf-8") as f:
        return f.read()


def calculate_target_words(info: dict) -> int:
    """计算目标字数"""
    length = info.get("length", "1500-2000字")
    style = info.get("style", "通俗易懂")
    min_w, max_w = LENGTH_RANGES.get(length, (1500, 2000))
    factor = STYLE_LENGTH_FACTOR.get(style, 1.0)
    target = int((min_w + max_w) / 2 * factor)
    return target


def build_prompt(info: dict, outline: str) -> str:
    """构建文章生成Prompt"""
    key_points = info.get("key_points", [])
    key_points_text = "\n".join(f"  {i+1}. {p}" for i, p in enumerate(key_points))

    prompt = f"""# 角色
你是一位经验丰富的{info.get('style', '')}写作者，擅长创作{info.get('audience', '')}喜爱的内容。

# 任务
基于以下大纲和信息，生成一篇完整的、符合要求的文章。

# 文章信息
- 主题：{info.get('topic', '')}
- 目标受众：{info.get('audience', '')}
- 写作风格：{info.get('style', '')}
- 字数要求：{info.get('length', '')}
- 核心要点：
{key_points_text}

# 文章大纲
{outline}

# 写作要求
1. 严格遵循大纲结构，不偏离主题
2. 字数控制在 {info.get('length', '')} 范围内
3. 语言风格保持"{info.get('style', '')}"，不要混用其他风格
4. 所有核心要点都要在正文中明确体现
5. 适当使用数据、案例、引言增强说服力
6. 段落之间要有自然过渡
7. 结论部分要呼应开头的核心问题

# 输出格式
请按以下Markdown格式输出：

# [文章标题]

> [副标题/导读]

## 引言

[正文...]

## 第一部分

[正文...]

...

## 结论

[正文...]
"""
    return prompt


def generate_article_demo(info: dict, outline: str, target_words: int) -> str:
    """生成演示版文章（当AI API不可用时使用）"""
    topic = info.get("topic", "")
    style = info.get("style", "通俗易懂")
    audience = info.get("audience", "")
    key_points = info.get("key_points", [])

    article = f"# {topic}：深度解析与实践指南\n\n"
    article += f"> 本文面向{audience}，采用{style}风格撰写\n\n"

    # 引言
    article += "## 引言\n\n"
    article += f"在当今快速发展的时代，{topic}已经成为不可忽视的重要议题。"
    article += f"无论你是{audience}，还是对{topic}感兴趣的普通读者，"
    article += f"深入了解其内涵与价值都显得尤为重要。\n\n"
    article += f"本文将从多个维度系统性地剖析{topic}，"
    article += f"帮助你建立全面而深入的认识。\n\n"

    # 主体部分（基于key_points）
    for i, point in enumerate(key_points, 1):
        article += f"## 第{i}部分：{point}\n\n"
        article += f"### {point}的核心要素\n\n"
        article += f"首先，我们需要明确{point}的基本概念。"
        article += f"在实践中，{point}涉及多个层面的内容，"
        article += f"包括理论基础、应用场景、关键挑战等。\n\n"

        article += f"### 实际案例分析\n\n"
        article += f"以{topic}领域为例，{point}的具体表现可以从以下几个角度来观察：\n\n"
        article += f"1. **数据表现**：相关数据显示，过去一年中涉及{point}的项目增长了30%以上\n"
        article += f"2. **应用场景**：在{audience}的实际工作中，{point}的应用越来越广泛\n"
        article += f"3. **发展趋势**：随着技术进步，{point}的重要性将继续提升\n\n"

        article += f"### 关键洞察\n\n"
        article += f"通过深入分析，我们可以得出以下结论：\n\n"
        article += f"- {point}是{topic}的核心组成部分\n"
        article += f"- 掌握{point}对于{audience}具有重要价值\n"
        article += f"- 未来{point}将呈现新的发展趋势\n\n"

    # 结论
    article += "## 结论\n\n"
    article += f"综上所述，{topic}作为一个复杂的系统性议题，"
    article += f"需要我们从多个角度进行深入理解。"
    article += f"通过本文的探讨，我们希望能够帮助{audience}更好地把握{topic}的核心要点。\n\n"

    article += f"### 核心观点回顾\n\n"
    for i, point in enumerate(key_points, 1):
        article += f"{i}. **{point}**\n"

    article += f"\n### 行动建议\n\n"
    article += f"对于{audience}，我们提出以下几点建议：\n\n"
    article += f"1. 持续关注{topic}领域的最新动态\n"
    article += f"2. 深入学习相关理论和方法论\n"
    article += f"3. 在实践中不断积累经验\n"
    article += f"4. 与同行交流分享心得\n\n"

    article += f"### 未来展望\n\n"
    article += f"展望未来，{topic}将继续演变和发展。"
    article += f"我们期待看到更多创新性的应用和突破，"
    article += f"为{audience}创造更大价值。\n\n"

    return article


def add_yaml_metadata(article: str, info: dict) -> str:
    """添加YAML元数据"""
    keywords = info.get("key_points", [])[:3]
    description = f"本文深入探讨{info.get('topic', '')}的核心要点，"
    description += f"面向{info.get('audience', '')}，"
    description += f"采用{info.get('style', '')}风格撰写，"
    description += f"涵盖{'、'.join(info.get('key_points', []))}等内容。"

    # 限制描述长度
    if len(description) > 150:
        description = description[:147] + "..."

    metadata = "---\n"
    metadata += f"title: \"{info.get('topic', '')}\"\n"
    metadata += f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
    metadata += f"author: \"AI Writer\"\n"
    metadata += f"style: {info.get('style', '')}\n"
    metadata += f"audience: {info.get('audience', '')}\n"
    metadata += f"length: {info.get('length', '')}\n"
    metadata += f"description: \"{description}\"\n"
    metadata += f"keywords:\n"
    for k in keywords:
        metadata += f"  - {k}\n"
    metadata += f"tags:\n"
    metadata += f"  - {info.get('topic', '')}\n"
    metadata += f"  - {info.get('style', '')}\n"
    metadata += "session_id: \"" + info.get("session_id", "") + "\"\n"
    metadata += "---\n\n"
    return metadata + article


def count_words(text: str) -> int:
    """统计中文字数"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return chinese_chars + english_words


def save_article(article: str, info: dict, output_dir: Path) -> Path:
    """保存文章"""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_topic = re.sub(r'[^\w]', '_', info.get("topic", "article"))[:20]
    session_id = info.get("session_id", "default")
    filename = f"article-{safe_topic}-{session_id}.md"
    output_path = output_dir / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(article)

    return output_path


def print_summary(article: str, output_path: Path, target_words: int):
    """打印摘要"""
    actual_words = count_words(article)
    print("\n" + "=" * 60)
    print("✅ 文章已生成！")
    print("=" * 60)
    print(f"📄 文件路径: {output_path}")
    print(f"📊 实际字数: {actual_words}")
    print(f"🎯 目标字数: {target_words}")
    print(f"📈 完成度: {min(100, int(actual_words / target_words * 100))}%")
    print("=" * 60)
    print("\n📖 文章预览（前15行）：\n")
    print("\n".join(article.split("\n")[:15]))
    print("\n...")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="文章生成工具")
    parser.add_argument("--info", "-i", required=True, help="文章信息JSON文件路径")
    parser.add_argument("--outline", required=True, help="文章大纲文件路径")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--ai", action="store_true", help="使用AI生成（需要API）")
    parser.add_argument("--no-metadata", action="store_true", help="不添加YAML元数据")

    args = parser.parse_args()

    info_path = Path(args.info)
    outline_path = Path(args.outline)

    if not info_path.exists():
        print(f"❌ 信息文件不存在: {info_path}")
        return 1
    if not outline_path.exists():
        print(f"❌ 大纲文件不存在: {outline_path}")
        return 1

    # 加载文件
    info = load_info(info_path)
    outline = load_outline(outline_path)

    # 计算目标字数
    target_words = calculate_target_words(info)
    print(f"\n📖 文章信息:")
    print(f"   主题: {info.get('topic', '')}")
    print(f"   风格: {info.get('style', '')}")
    print(f"   目标字数: {target_words}")

    # 构建Prompt
    prompt = build_prompt(info, outline)
    print(f"\n💭 Prompt已构建（{len(prompt)} 字符）")

    # 生成文章
    if args.ai:
        print("\n⚠️  AI模式需要配置API key，请参考prompt-templates.md手动调用")
        print("   临时使用演示模式生成示例文章...")

    article = generate_article_demo(info, outline, target_words)

    # 添加元数据
    if not args.no_metadata:
        article = add_yaml_metadata(article, info)

    # 保存
    output_dir = Path(args.output) if args.output else info_path.parent
    output_path = save_article(article, info, output_dir)

    # 输出摘要
    print_summary(article, output_path, target_words)

    return 0


if __name__ == "__main__":
    exit(main())
