#!/usr/bin/env python3
"""
site-utils.py - 网站工具函数库

功能：
1. Hugo 网站根目录自动检测
2. Git 操作封装
3. 文件路径处理
4. Slug 生成
5. Front Matter 解析
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def find_hugo_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    自动检测 Hugo 网站根目录
    从 start_path 开始向上查找，直到找到 hugo.toml 或 config.toml
    """
    if start_path is None:
        start_path = Path.cwd()

    current = start_path.resolve()

    while True:
        # 检查配置文件
        config_files = ["hugo.toml", "config.toml", "hugo.yaml", "config.yaml", "hugo.json", "config.json"]
        for config_file in config_files:
            if (current / config_file).exists():
                # 检查是否有 content 目录
                if (current / "content").exists():
                    return current

        # 到达根目录，停止
        if current.parent == current:
            break

        current = current.parent

    return None


def generate_slug(title: str, max_length: int = 60) -> str:
    """
    生成 URL 友好的 slug
    保留中文，转换空格和特殊字符
    """
    # 移除首尾空白
    slug = title.strip()

    # 中文和字母数字保留，其他替换为 -
    result = []
    for char in slug:
        if re.match(r'[\u4e00-\u9fa5a-zA-Z0-9]', char):
            result.append(char)
        else:
            result.append('-')

    slug = ''.join(result)

    # 多个连续 - 替换为一个
    slug = re.sub(r'-+', '-', slug)

    # 首尾的 - 去掉
    slug = slug.strip('-')

    # 长度限制
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')

    # 如果全空了，用时间戳
    if not slug:
        slug = datetime.now().strftime("%Y%m%d-%H%M%S")

    return slug


def parse_front_matter(content: str) -> Tuple[dict, str]:
    """
    解析 Markdown 文件的 YAML Front Matter
    返回 (metadata_dict, body_content)
    """
    metadata = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            body = parts[2].strip()

            # 简单 YAML 解析
            current_list_key = None
            for line in yaml_content.split("\n"):
                line = line.rstrip()
                if not line:
                    continue

                # 列表项
                if line.startswith("  - ") and current_list_key:
                    value = line.strip()[2:].strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    metadata[current_list_key].append(value)
                elif line.startswith("- ") and current_list_key:
                    value = line[2:].strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    metadata[current_list_key].append(value)
                elif ":" in line and not line.startswith(" "):
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
                        # 布尔值处理
                        if value.lower() == "true":
                            value = True
                        elif value.lower() == "false":
                            value = False
                        metadata[key] = value

    return metadata, body


def build_front_matter(metadata: dict) -> str:
    """
    构建 YAML Front Matter
    """
    lines = ["---"]

    for key, value in metadata.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            # 字符串
            str_value = str(value)
            if ":" in str_value or '"' in str_value or str_value.startswith(" "):
                lines.append(f'{key}: "{str_value}"')
            else:
                lines.append(f"{key}: {str_value}")

    lines.append("---")
    return "\n".join(lines)


def extract_summary(body: str, max_length: int = 150) -> str:
    """
    从正文中提取摘要
    """
    # 移除 Markdown 标记
    text = re.sub(r'#+\s*', '', body)  # 标题
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 粗体
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # 斜体
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 链接
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)  # 图片
    text = re.sub(r'`[^`]+`', '', text)  # 行内代码
    text = re.sub(r'```[\s\S]*?```', '', text)  # 代码块
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)  # 引用
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)  # 列表
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)  # 有序列表

    # 移除多余空白
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 截取长度
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."

    return text


def git_commit(site_path: Path, message: str, files: list = None) -> bool:
    """
    Git 提交
    """
    try:
        # 切换到网站目录
        original_dir = os.getcwd()
        os.chdir(site_path)

        try:
            # 添加文件
            if files:
                for f in files:
                    subprocess.run(["git", "add", f], check=True, capture_output=True)
            else:
                subprocess.run(["git", "add", "."], check=True, capture_output=True)

            # 提交
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Git 提交成功: {message}")
                return True
            else:
                if "nothing to commit" in result.stdout:
                    print("ℹ️  没有需要提交的变更")
                    return True
                print(f"❌ Git 提交失败: {result.stderr}")
                return False
        finally:
            os.chdir(original_dir)

    except Exception as e:
        print(f"❌ Git 操作异常: {e}")
        return False


def git_push(site_path: Path, branch: str = "main") -> bool:
    """
    Git 推送到远程
    """
    try:
        original_dir = os.getcwd()
        os.chdir(site_path)

        try:
            result = subprocess.run(
                ["git", "push", "origin", branch],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print("✅ Git 推送成功")
                return True
            else:
                print(f"❌ Git 推送失败: {result.stderr}")
                return False
        finally:
            os.chdir(original_dir)

    except Exception as e:
        print(f"❌ Git 推送异常: {e}")
        return False


def get_site_url(site_path: Path) -> Optional[str]:
    """
    从 Hugo 配置中获取网站 URL
    """
    config_files = ["hugo.toml", "config.toml", "hugo.yaml", "config.yaml"]

    for config_file in config_files:
        config_path = site_path / config_file
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # TOML 格式
                if config_file.endswith(".toml"):
                    match = re.search(r'baseURL\s*=\s*"([^"]+)"', content)
                    if match:
                        return match.group(1).rstrip("/")

                # YAML 格式
                elif config_file.endswith(".yaml"):
                    match = re.search(r'baseURL:\s*"?([^"\n]+)"?', content)
                    if match:
                        return match.group(1).rstrip("/")

            except Exception:
                pass

    return None


def check_hugo_installed() -> bool:
    """
    检查 Hugo 是否已安装
    """
    try:
        result = subprocess.run(["hugo", "version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False
