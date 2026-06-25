#!/usr/bin/env python3
"""
publish-slides.py - 幻灯片发布脚本

功能：
1. 将 HTML 幻灯片发布到 Hugo 网站
2. 自动创建页面和静态资源
3. 支持 Git 提交和推送
4. 生成访问 URL

使用方法：
    python publish-slides.py --input data/slides-xxx.html
    python publish-slides.py -i data/slides-xxx.html --site-path ../my-hugo-site
    python publish-slides.py -i data/slides-xxx.html --auto-deploy
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# 动态导入 site_utils
import importlib.util
_site_utils_path = Path(__file__).resolve().parent / "site-utils.py"
_spec = importlib.util.spec_from_file_location("site_utils", _site_utils_path)
site_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_utils)

find_hugo_root = site_utils.find_hugo_root
generate_slug = site_utils.generate_slug
build_front_matter = site_utils.build_front_matter
git_commit = site_utils.git_commit
git_push = site_utils.git_push
get_site_url = site_utils.get_site_url


def detect_slide_title(html_content: str, fallback: str = "幻灯片") -> str:
    """从 HTML 中提取标题"""
    # 尝试 <title> 标签
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        if title:
            return title

    # 尝试 <h1> 标签
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if title:
            return title

    return fallback


def publish_slide(slide_path: Path, site_path: Path, options: dict) -> dict:
    """
    发布单个幻灯片
    返回发布结果信息
    """
    result = {
        "success": False,
        "title": "",
        "slug": "",
        "slide_url": "",
        "page_url": "",
        "files_added": []
    }

    # 读取 HTML 文件
    with open(slide_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 提取标题
    title = detect_slide_title(html_content, slide_path.stem)
    result["title"] = title

    # 生成 slug
    slug = generate_slug(title)
    result["slug"] = slug

    # 1. 拷贝 HTML 到 static/slides/
    static_slides_dir = site_path / "static" / "slides" / slug
    static_slides_dir.mkdir(parents=True, exist_ok=True)

    slide_html_path = static_slides_dir / "index.html"
    shutil.copy2(slide_path, slide_html_path)
    result["files_added"].append(str(slide_html_path.relative_to(site_path)))

    # 2. 创建 content/slides/ 页面
    content_slides_dir = site_path / "content" / "slides"
    content_slides_dir.mkdir(parents=True, exist_ok=True)

    page_md_path = content_slides_dir / f"{slug}.md"

    # 构建 Front Matter
    metadata = {
        "title": f"{title} - 幻灯片",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "draft": options.get("draft", False),
        "description": f"关于{title}的演示文稿",
        "type": "slides",
        "categories": ["幻灯片"],
        "tags": ["幻灯片", "演示文稿"],
        "slide_url": f"/slides/{slug}/",
    }

    # 构建页面内容
    front_matter = build_front_matter(metadata)

    page_content = f"""{front_matter}

## 幻灯片简介

这是关于 **{title}** 的演示文稿。

## 在线查看

<iframe src="/slides/{slug}/index.html"
        style="width: 100%;
               height: 70vh;
               border: none;
               border-radius: 8px;
               box-shadow: 0 4px 20px rgba(0,0,0,0.1);
               margin: 1.5rem 0;">
</iframe>

<div style="text-align: center; margin: 1rem 0;">
  <a href="/slides/{slug}/index.html" target="_blank"
     style="display: inline-block;
            padding: 0.75rem 2rem;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;">
    🖥️ 全屏查看幻灯片
  </a>
</div>

## 使用说明

- 使用 **← →** 键翻页
- 按 **F** 键进入全屏模式
- 点击屏幕左右边缘也可翻页
- 支持移动端触控滑动
- 按 **Esc** 退出全屏
"""

    with open(page_md_path, "w", encoding="utf-8") as f:
        f.write(page_content)

    result["files_added"].append(str(page_md_path.relative_to(site_path)))

    # 获取网站 URL
    site_url = get_site_url(site_path)
    if site_url:
        result["slide_url"] = f"{site_url}/slides/{slug}/"
        result["page_url"] = f"{site_url}/slides/{slug}/"
    else:
        result["slide_url"] = f"/slides/{slug}/"
        result["page_url"] = f"/slides/{slug}/"

    result["success"] = True
    return result


def print_summary(results: list, site_path: Path, options: dict):
    """打印发布摘要"""
    print("\n" + "=" * 60)
    print("🎉 幻灯片发布完成！")
    print("=" * 60)
    print(f"📁 网站路径: {site_path}")
    print(f"📊 发布数量: {len(results)} 个幻灯片")
    print(f"📝 草稿模式: {'是' if options.get('draft') else '否'}")
    print(f"🔄 Git提交: {'启用' if options.get('auto_deploy') else '未启用'}")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"\n{i}. ✅ {result['title']}")
            print(f"   Slug: {result['slug']}")
            print(f"   幻灯片: {result['slide_url']}")
            print(f"   页面: {result['page_url']}")
            print(f"   文件: {len(result['files_added'])} 个")
        else:
            print(f"\n{i}. ❌ 发布失败")

    print("\n" + "=" * 60)

    if not options.get("auto_deploy"):
        print("\n💡 下一步:")
        print("   1. 本地预览: cd 到网站目录, 运行 hugo server")
        print("   2. 构建发布: hugo --minify")
        print("   3. Git 提交: git add . && git commit -m 'feat(slides): 添加幻灯片'")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="幻灯片发布到Hugo网站工具")
    parser.add_argument("--input", "-i", required=True,
                        help="幻灯片HTML文件路径（支持单个文件或目录）")
    parser.add_argument("--site-path", "-s",
                        help="Hugo网站根目录（默认自动检测）")
    parser.add_argument("--draft", action="store_true",
                        help="作为草稿发布（不公开）")
    parser.add_argument("--auto-deploy", action="store_true",
                        help="自动Git提交并推送")
    parser.add_argument("--push", action="store_true",
                        help="Git推送到远程（需配合--auto-deploy）")
    parser.add_argument("--branch", default="main",
                        help="Git分支（默认: main）")

    args = parser.parse_args()

    input_path = Path(args.input)

    # 1. 验证输入
    if not input_path.exists():
        print(f"❌ 输入路径不存在: {input_path}")
        return 1

    # 收集所有幻灯片文件
    slide_files = []
    if input_path.is_file():
        if input_path.suffix.lower() == ".html":
            slide_files.append(input_path)
    else:
        slide_files = list(input_path.glob("*.html"))

    if not slide_files:
        print("❌ 没有找到 HTML 幻灯片文件")
        return 1

    print(f"\n📁 找到 {len(slide_files)} 个幻灯片文件")

    # 2. 检测 Hugo 网站根目录
    site_path = None
    if args.site_path:
        site_path = Path(args.site_path).resolve()
        if not (site_path / "content").exists():
            print(f"❌ 网站路径无效（缺少 content 目录）: {site_path}")
            return 1
    else:
        site_path = find_hugo_root(input_path.parent)
        if not site_path:
            site_path = find_hugo_root(Path.cwd())

    if not site_path:
        print("❌ 未找到 Hugo 网站根目录，请使用 --site-path 指定")
        return 1

    print(f"🌐 网站根目录: {site_path}")

    # 3. 发布选项
    options = {
        "draft": args.draft,
        "auto_deploy": args.auto_deploy,
    }

    # 4. 逐个发布
    results = []
    for slide_file in slide_files:
        print(f"\n📤 发布: {slide_file.name}")
        result = publish_slide(slide_file, site_path, options)
        results.append(result)
        if result["success"]:
            print(f"   ✅ 成功: {result['title']}")
        else:
            print("   ❌ 失败")

    # 5. 自动部署
    if args.auto_deploy:
        all_files = []
        for r in results:
            all_files.extend(r["files_added"])

        if all_files:
            message = f"feat(slides): 添加 {len(results)} 个幻灯片"
            if len(results) == 1 and results[0].get("title"):
                message = f"feat(slides): 添加幻灯片《{results[0]['title']}》"

            git_commit(site_path, message, all_files)

            if args.push:
                git_push(site_path, args.branch)

    # 6. 输出摘要
    print_summary(results, site_path, options)

    # 返回成功的数量
    success_count = sum(1 for r in results if r["success"])
    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    exit(main())
