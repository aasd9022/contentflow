#!/usr/bin/env python3
"""
publish-article.py - 文章发布脚本

功能：
1. 将 Markdown 文章发布到 Hugo 网站
2. 自动解析 Front Matter
3. 支持 Page Bundle 模式
4. 支持 Git 提交和推送
5. 生成访问 URL

使用方法：
    python publish-article.py --input data/article-xxx.md
    python publish-article.py -i data/article-xxx.md --section posts
    python publish-article.py -i data/article-xxx.md --auto-deploy
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
parse_front_matter = site_utils.parse_front_matter
build_front_matter = site_utils.build_front_matter
extract_summary = site_utils.extract_summary
git_commit = site_utils.git_commit
git_push = site_utils.git_push
get_site_url = site_utils.get_site_url


def detect_section(site_path: Path) -> str:
    """
    检测网站使用的文章 section
    优先 posts，其次 articles，都没有就用 posts
    """
    content_dir = site_path / "content"

    # 常见的 section 名称
    candidates = ["posts", "articles", "blog", "post"]

    for candidate in candidates:
        if (content_dir / candidate).exists():
            return candidate

    return "posts"


def publish_article(article_path: Path, site_path: Path, options: dict) -> dict:
    """
    发布单篇文章
    返回发布结果信息
    """
    result = {
        "success": False,
        "title": "",
        "slug": "",
        "url": "",
        "files_added": []
    }

    # 1. 读取文章
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. 解析 Front Matter
    metadata, body = parse_front_matter(content)

    # 3. 提取标题
    title = metadata.get("title", "")
    if not title:
        # 从正文提取第一个 H1
        match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        if match:
            title = match.group(1).strip()
        else:
            title = article_path.stem

    result["title"] = title

    # 4. 生成 slug
    slug = metadata.get("slug", "")
    if not slug:
        slug = generate_slug(title)
    result["slug"] = slug

    # 5. 确定 section
    section = options.get("section", detect_section(site_path))

    # 6. 确保有摘要
    if not metadata.get("summary") and not metadata.get("description"):
        summary = extract_summary(body, 150)
        if summary:
            metadata["summary"] = summary
            if not metadata.get("description"):
                metadata["description"] = summary

    # 7. 补充日期
    if not metadata.get("date"):
        metadata["date"] = datetime.now().strftime("%Y-%m-%d")

    # 8. 确保 draft 字段
    if "draft" not in metadata:
        metadata["draft"] = options.get("draft", False)

    # 9. 使用 Page Bundle 模式发布
    post_dir = site_path / "content" / section / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    # 构建完整文章
    full_front_matter = build_front_matter(metadata)
    full_content = f"{full_front_matter}\n\n{body}\n"

    # 写入 index.md
    index_md_path = post_dir / "index.md"
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    result["files_added"].append(str(index_md_path.relative_to(site_path)))

    # 10. 处理图片（如果文章同目录有 images 文件夹）
    images_src_dir = article_path.parent / "images"
    if images_src_dir.exists() and images_src_dir.is_dir():
        images_dst_dir = post_dir / "images"
        if not images_dst_dir.exists():
            shutil.copytree(images_src_dir, images_dst_dir)
            for img_file in images_dst_dir.rglob("*"):
                if img_file.is_file():
                    result["files_added"].append(
                        str(img_file.relative_to(site_path))
                    )

    # 11. 获取 URL
    site_url = get_site_url(site_path)
    if site_url:
        result["url"] = f"{site_url}/{section}/{slug}/"
    else:
        result["url"] = f"/{section}/{slug}/"

    result["success"] = True
    result["section"] = section
    result["metadata"] = metadata

    return result


def print_summary(results: list, site_path: Path, options: dict):
    """打印发布摘要"""
    print("\n" + "=" * 60)
    print("🎉 文章发布完成！")
    print("=" * 60)
    print(f"📁 网站路径: {site_path}")
    print(f"📝 文章数量: {len(results)} 篇")
    print(f"📂 分类目录: {options.get('section', 'posts')}")
    print(f"📝 草稿模式: {'是' if options.get('draft') else '否'}")
    print(f"🔄 Git提交: {'启用' if options.get('auto_deploy') else '未启用'}")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"\n{i}. ✅ {result['title']}")
            print(f"   Slug: {result['slug']}")
            print(f"   URL: {result['url']}")
            print(f"   分类: {result.get('section', 'posts')}")
            print(f"   文件: {len(result['files_added'])} 个")
        else:
            print(f"\n{i}. ❌ 发布失败")

    print("\n" + "=" * 60)

    if not options.get("auto_deploy"):
        print("\n💡 下一步:")
        print("   1. 本地预览: cd 到网站目录, 运行 hugo server -D")
        print("   2. 构建发布: hugo --minify")
        print("   3. Git 提交: git add . && git commit -m 'feat(posts): 添加新文章'")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="文章发布到Hugo网站工具")
    parser.add_argument("--input", "-i", required=True,
                        help="文章Markdown文件路径（支持单个文件或目录）")
    parser.add_argument("--site-path", "-s",
                        help="Hugo网站根目录（默认自动检测）")
    parser.add_argument("--section",
                        help="文章分类目录（默认自动检测: posts/articles）")
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

    # 收集所有文章文件
    article_files = []
    if input_path.is_file():
        if input_path.suffix.lower() in (".md", ".markdown"):
            article_files.append(input_path)
    else:
        article_files = list(input_path.glob("*.md")) + list(input_path.glob("*.markdown"))

    if not article_files:
        print("❌ 没有找到 Markdown 文章文件")
        return 1

    print(f"\n📁 找到 {len(article_files)} 篇文章")

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

    # 3. 确定 section
    section = args.section or detect_section(site_path)
    print(f"📂 分类目录: {section}")

    # 4. 发布选项
    options = {
        "draft": args.draft,
        "auto_deploy": args.auto_deploy,
        "section": section,
    }

    # 5. 逐个发布
    results = []
    for article_file in article_files:
        print(f"\n📤 发布: {article_file.name}")
        result = publish_article(article_file, site_path, options)
        results.append(result)
        if result["success"]:
            print(f"   ✅ 成功: {result['title']}")
        else:
            print("   ❌ 失败")

    # 6. 自动部署
    if args.auto_deploy:
        all_files = []
        for r in results:
            all_files.extend(r["files_added"])

        if all_files:
            message = f"feat({section}): 添加 {len(results)} 篇文章"
            if len(results) == 1 and results[0].get("title"):
                message = f"feat({section}): 添加文章《{results[0]['title']}》"

            git_commit(site_path, message, all_files)

            if args.push:
                git_push(site_path, args.branch)

    # 7. 输出摘要
    print_summary(results, site_path, options)

    # 返回成功的数量
    success_count = sum(1 for r in results if r["success"])
    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    exit(main())
