"""
fix-python37-compat.py - 修复 Python 3.7 类型注解兼容性

将 Python 3.9+ 的类型注解语法（tuple[...], list[...], dict[...]）
替换为 typing 模块的写法（Tuple[...], List[...], Dict[...]）
"""

import re
from pathlib import Path


# 需要修复的文件模式
FILE_PATTERNS = [
    "**/*.py",
]

# 替换规则：先import，再替换类型注解
IMPORT_ADDITIONS = "from typing import Tuple, List, Dict, Optional, Any, Union"


def fix_file(file_path: Path) -> bool:
    """修复单个文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False

    original = content

    # 1. 检查是否已有 typing import
    has_typing_import = "from typing import" in content or "import typing" in content

    # 2. 检查是否有需要修复的类型注解
    needs_fix = False
    patterns = [
        (r'tuple\[', 'Tuple['),
        (r'list\[', 'List['),
        (r'dict\[', 'Dict['),
    ]

    for pattern, _ in patterns:
        if re.search(pattern, content):
            needs_fix = True
            break

    if not needs_fix:
        return False

    # 3. 如果没有typing import，添加一个
    if not has_typing_import:
        # 在第一个import之后添加
        lines = content.split("\n")
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_idx = i + 1
            elif insert_idx > 0 and line.strip() and not line.startswith("#"):
                break

        lines.insert(insert_idx, IMPORT_ADDITIONS)
        content = "\n".join(lines)

    # 4. 替换类型注解
    content = re.sub(r'\btuple\[', 'Tuple[', content)
    content = re.sub(r'\blist\[', 'List[', content)
    content = re.sub(r'\bdict\[', 'Dict[', content)

    # 5. 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content != original


def main():
    workflow_dir = Path(__file__).parent
    print(f"🔍 扫描目录: {workflow_dir}")

    fixed_files = []

    for py_file in workflow_dir.rglob("*.py"):
        # 跳过本脚本
        if py_file.name == "fix-python37-compat.py":
            continue

        # 跳过 .git 等目录
        if ".git" in py_file.parts or "__pycache__" in py_file.parts:
            continue

        if fix_file(py_file):
            fixed_files.append(py_file)
            print(f"  ✅ 已修复: {py_file.relative_to(workflow_dir)}")

    print(f"\n🎉 修复完成！共修复 {len(fixed_files)} 个文件")


if __name__ == "__main__":
    main()
