#!/usr/bin/env python3
"""
workflow.py - 内容生产工作流主入口

一站式内容生产流水线：
  信息收集 → 文章生成 → 幻灯片生成 → 网站发布

使用方法：
    # 交互式完整流程
    python workflow.py

    # 直接提供主题快速生成
    python workflow.py --topic "AI在医疗领域的应用"
                      --audience "产品经理"
                      --style "专业严谨"
                      --length "1500-2000字"
                      --key-points "技术原理,应用场景,未来趋势"

    # 只执行部分阶段
    python workflow.py --skip-publish       # 不发布到网站
    python workflow.py --skip-slides        # 不生成幻灯片
    python workflow.py --publish-only       # 只执行发布阶段
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List


# ============================================================
# 路径配置
# ============================================================

WORKFLOW_DIR = Path(__file__).parent.resolve()
DATA_DIR = WORKFLOW_DIR / "data"

SKILL_PATHS = {
    "ask_info": WORKFLOW_DIR / "1.ask-info-skill",
    "article_gen": WORKFLOW_DIR / "2.article-gen-skill",
    "slides": WORKFLOW_DIR / "3.slides-html-skill",
    "publish": WORKFLOW_DIR / "4.website-publish-skill",
}

SCRIPT_PATHS = {
    "save_info": SKILL_PATHS["ask_info"] / "scripts" / "save-info.py",
    "gen_outline": SKILL_PATHS["article_gen"] / "scripts" / "gen-outline.py",
    "gen_article": SKILL_PATHS["article_gen"] / "scripts" / "gen-article.py",
    "md_to_json": SKILL_PATHS["article_gen"] / "scripts" / "md-to-json.py",
    "gen_slides": SKILL_PATHS["slides"] / "scripts" / "gen-slides.py",
    "publish_slides": SKILL_PATHS["publish"] / "scripts" / "publish-slides.py",
    "publish_article": SKILL_PATHS["publish"] / "scripts" / "publish-article.py",
}


# ============================================================
# 工具函数
# ============================================================

def print_banner():
    """打印欢迎横幅"""
    print("\n" + "=" * 60)
    print("🎯 内容生产工作流 Content Workflow")
    print("=" * 60)
    print("  信息收集 → 文章生成 → 幻灯片 → 网站发布")
    print("=" * 60)


def print_stage(stage_num: int, total_stages: int, title: str):
    """打印阶段标题"""
    print(f"\n{'='*60}")
    print(f"📌 阶段 {stage_num}/{total_stages}: {title}")
    print(f"{'='*60}")


def print_success(message: str):
    """打印成功消息"""
    print(f"\n✅ {message}")


def print_error(message: str):
    """打印错误消息"""
    print(f"\n❌ {message}")


def run_script(script_path: Path, args: list) -> bool:
    """
    运行 Python 脚本
    返回是否成功
    """
    cmd = [sys.executable, str(script_path)] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print_error(f"脚本执行失败: {e}")
        return False


def ensure_data_dir():
    """确保 data 目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


# ============================================================
# 阶段 1: 信息收集
# ============================================================

def stage_ask_info(args) -> Optional[Path]:
    """
    阶段1：收集文章信息
    返回 article-info.json 的路径
    """
    print_stage(1, 4, "信息收集")

    ensure_data_dir()

    # 如果提供了完整参数，直接生成
    if args.topic and args.audience and args.style and args.length and args.key_points:
        print("📝 使用命令行参数生成信息...")

        cmd_args = [
            "--topic", args.topic,
            "--audience", args.audience,
            "--style", args.style,
            "--length", args.length,
            "--key-points", args.key_points,
            "--output", str(DATA_DIR),
        ]

        success = run_script(SCRIPT_PATHS["save_info"], cmd_args)
        if not success:
            print_error("信息收集失败")
            return None

        # 找到最新的 info 文件
        info_files = sorted(DATA_DIR.glob("article-info-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if info_files:
            print_success(f"信息已保存: {info_files[0].name}")
            return info_files[0]
        return None

    # 交互式模式
    else:
        print("💬 进入交互式信息收集模式...")
        print("   （提示：使用 --topic 等参数可以跳过交互）")

        success = run_script(SCRIPT_PATHS["save_info"], [
            "--interactive",
            "--output", str(DATA_DIR),
        ])

        if success:
            info_files = sorted(DATA_DIR.glob("article-info-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            if info_files:
                print_success(f"信息已保存: {info_files[0].name}")
                return info_files[0]

        return None


# ============================================================
# 阶段 2: 文章生成
# ============================================================

def stage_gen_article(info_path: Path) -> Tuple[Optional[Path], Optional[Path]]:
    """
    阶段2：生成文章
    返回 (article_md_path, article_json_path)
    """
    print_stage(2, 4, "文章生成")

    if not info_path or not info_path.exists():
        print_error("信息文件不存在")
        return None, None

    print(f"📖 使用信息文件: {info_path.name}")

    # 2.1 生成大纲
    print("\n📑 生成大纲...")
    outline_success = run_script(SCRIPT_PATHS["gen_outline"], [
        "--info", str(info_path),
        "--output", str(DATA_DIR),
    ])

    if not outline_success:
        print_error("大纲生成失败")
        return None, None

    # 找到大纲文件
    outline_files = sorted(DATA_DIR.glob("outline-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not outline_files:
        print_error("未找到生成的大纲文件")
        return None, None

    outline_path = outline_files[0]
    print_success(f"大纲已生成: {outline_path.name}")

    # 2.2 生成文章
    print("\n✍️  生成文章...")
    article_success = run_script(SCRIPT_PATHS["gen_article"], [
        "--info", str(info_path),
        "--outline", str(outline_path),
        "--output", str(DATA_DIR),
    ])

    if not article_success:
        print_error("文章生成失败")
        return None, None

    # 找到文章文件
    article_files = sorted(DATA_DIR.glob("article-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not article_files:
        print_error("未找到生成的文章文件")
        return None, None

    article_path = article_files[0]
    print_success(f"文章已生成: {article_path.name}")

    # 2.3 转换为结构化 JSON
    print("\n🔄 转换为结构化格式...")
    json_success = run_script(SCRIPT_PATHS["md_to_json"], [
        "--input", str(article_path),
        "--output", str(DATA_DIR),
    ])

    if not json_success:
        print_error("结构化转换失败")
        return article_path, None

    json_files = sorted(DATA_DIR.glob("article-structured-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not json_files:
        print_error("未找到结构化JSON文件")
        return article_path, None

    json_path = json_files[0]
    print_success(f"结构化JSON已生成: {json_path.name}")

    return article_path, json_path


# ============================================================
# 阶段 3: 幻灯片生成
# ============================================================

def stage_gen_slides(json_path: Path, theme: str = "modern") -> Optional[Path]:
    """
    阶段3：生成HTML幻灯片
    返回 slides.html 的路径
    """
    print_stage(3, 4, "HTML幻灯片生成")

    if not json_path or not json_path.exists():
        print_error("结构化JSON文件不存在")
        return None

    print(f"🎨 使用主题: {theme}")
    print(f"📁 输入文件: {json_path.name}")

    success = run_script(SCRIPT_PATHS["gen_slides"], [
        "--input", str(json_path),
        "--theme", theme,
        "--output", str(DATA_DIR),
    ])

    if not success:
        print_error("幻灯片生成失败")
        return None

    # 找到幻灯片文件
    slides_files = sorted(DATA_DIR.glob("slides-*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not slides_files:
        print_error("未找到生成的幻灯片文件")
        return None

    slides_path = slides_files[0]
    print_success(f"幻灯片已生成: {slides_path.name}")
    return slides_path


# ============================================================
# 阶段 4: 网站发布
# ============================================================

def stage_publish(article_path: Optional[Path], slides_path: Optional[Path], site_path: Optional[str] = None) -> bool:
    """
    阶段4：发布到网站
    """
    print_stage(4, 4, "网站发布")

    if not article_path and not slides_path:
        print_error("没有可发布的内容")
        return False

    all_success = True

    # 发布文章
    if article_path and article_path.exists():
        print(f"\n📝 发布文章: {article_path.name}")

        publish_args = ["--input", str(article_path)]
        if site_path:
            publish_args.extend(["--site-path", site_path])

        success = run_script(SCRIPT_PATHS["publish_article"], publish_args)
        if success:
            print_success("文章发布成功")
        else:
            print_error("文章发布失败")
            all_success = False
    else:
        print("\n⏭️  跳过文章发布（无文章内容）")

    # 发布幻灯片
    if slides_path and slides_path.exists():
        print(f"\n🖼️  发布幻灯片: {slides_path.name}")

        publish_args = ["--input", str(slides_path)]
        if site_path:
            publish_args.extend(["--site-path", site_path])

        success = run_script(SCRIPT_PATHS["publish_slides"], publish_args)
        if success:
            print_success("幻灯片发布成功")
        else:
            print_error("幻灯片发布失败")
            all_success = False
    else:
        print("\n⏭️  跳过幻灯片发布（无幻灯片内容）")

    return all_success


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="内容生产工作流 - 信息收集→文章生成→幻灯片→网站发布",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式完整流程
  python workflow.py

  # 快速生成（指定主题）
  python workflow.py --topic "AI与医疗" --audience "产品经理" --style "专业严谨" --length "1500-2000字" --key-points "原理,应用,趋势"

  # 只生成文章，不发布
  python workflow.py --skip-publish

  # 指定幻灯片主题
  python workflow.py --theme gradient
        """
    )

    # 文章信息参数
    parser.add_argument("--topic", help="文章主题")
    parser.add_argument("--audience", help="目标受众")
    parser.add_argument("--style",
                        choices=["专业严谨", "通俗易懂", "故事化叙事", "观点评论", "教程指南"],
                        help="写作风格")
    parser.add_argument("--length",
                        choices=["500-1000字", "1500-2000字", "3000-5000字", "5000字以上"],
                        help="文章长度")
    parser.add_argument("--key-points", help="核心要点（逗号分隔）")

    # 流程控制
    parser.add_argument("--skip-slides", action="store_true",
                        help="跳过幻灯片生成")
    parser.add_argument("--skip-publish", action="store_true",
                        help="跳过网站发布")
    parser.add_argument("--publish-only", action="store_true",
                        help="只执行发布阶段（需指定输入文件）")

    # 发布配置
    parser.add_argument("--site-path", help="Hugo网站根目录")
    parser.add_argument("--theme", default="modern",
                        choices=["modern", "classic", "gradient", "minimal", "dark", "ocean", "sunset", "forest"],
                        help="幻灯片主题（默认: modern）")

    # 从已有文件开始
    parser.add_argument("--from-info", help="从已有 article-info.json 开始")
    parser.add_argument("--from-article", help="从已有 article.md 开始")
    parser.add_argument("--from-slides", help="从已有 slides.html 开始（仅发布）")

    args = parser.parse_args()

    # 打印横幅
    print_banner()

    # 确保 data 目录
    ensure_data_dir()

    # ==========================================
    # 只发布模式
    # ==========================================
    if args.publish_only:
        print("\n📤 仅发布模式")

        article_path = Path(args.from_article) if args.from_article else None
        slides_path = Path(args.from_slides) if args.from_slides else None

        success = stage_publish(article_path, slides_path, args.site_path)
        print("\n" + "=" * 60)
        if success:
            print("🎉 发布完成！")
        else:
            print("⚠️  发布部分完成（有错误）")
        print("=" * 60)
        return 0 if success else 1

    # ==========================================
    # 完整工作流
    # ==========================================

    info_path = None
    article_path = None
    article_json_path = None
    slides_path = None

    # 确定从哪个阶段开始
    start_stage = 1

    if args.from_slides:
        start_stage = 4  # 直接发布
        slides_path = Path(args.from_slides)
    elif args.from_article:
        start_stage = 3  # 从幻灯片开始
        article_path = Path(args.from_article)
        # 需要先转成结构化JSON
        print("\n🔄 转换文章为结构化格式...")
        run_script(SCRIPT_PATHS["md_to_json"], [
            "--input", str(article_path),
            "--output", str(DATA_DIR),
        ])
        json_files = sorted(DATA_DIR.glob("article-structured-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if json_files:
            article_json_path = json_files[0]
    elif args.from_info:
        start_stage = 2  # 从文章生成开始
        info_path = Path(args.from_info)

    # 阶段 1: 信息收集
    if start_stage <= 1:
        info_path = stage_ask_info(args)
        if not info_path:
            print_error("信息收集失败，工作流终止")
            return 1

    # 阶段 2: 文章生成
    if start_stage <= 2:
        article_path, article_json_path = stage_gen_article(info_path)
        if not article_path:
            print_error("文章生成失败，工作流终止")
            return 1

    # 阶段 3: 幻灯片生成
    if start_stage <= 3 and not args.skip_slides and article_json_path:
        slides_path = stage_gen_slides(article_json_path, args.theme)
        if not slides_path:
            print_error("幻灯片生成失败，但继续后续步骤...")

    # 阶段 4: 网站发布
    if not args.skip_publish:
        success = stage_publish(article_path, slides_path, args.site_path)
    else:
        success = True
        print("\n⏭️  跳过网站发布阶段")

    # ==========================================
    # 最终总结
    # ==========================================
    print("\n" + "=" * 60)
    print("🎊 工作流执行完成！")
    print("=" * 60)

    if info_path:
        print(f"   📋 信息文件: {info_path.name}")
    if article_path:
        print(f"   📝 文章文件: {article_path.name}")
    if article_json_path:
        print(f"   🔣 结构化JSON: {article_json_path.name}")
    if slides_path:
        print(f"   🖼️  幻灯片文件: {slides_path.name}")

    print(f"\n📁 所有输出文件位于: {DATA_DIR}")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
