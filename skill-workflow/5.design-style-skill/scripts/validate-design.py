#!/usr/bin/env python3
"""
设计一致性验证脚本
检查HTML中的设计规范遵循情况
"""

import re
import argparse
import json
import math
from collections import defaultdict

def hex_to_rgb(hex_color):
    """将hex颜色转换为RGB"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(rgb):
    """计算相对亮度"""
    r, g, b = [x/255.0 for x in rgb]
    r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055) ** 2.4
    g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055) ** 2.4
    b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055) ** 2.4
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast_ratio(color1, color2):
    """计算对比度"""
    l1 = get_luminance(hex_to_rgb(color1))
    l2 = get_luminance(hex_to_rgb(color2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def extract_colors(html):
    """从HTML中提取颜色"""
    colors = set()

    # 提取hex颜色
    hex_pattern = r'#[0-9a-fA-F]{3,8}'
    colors.update(re.findall(hex_pattern, html))

    # 提取rgb/rgba颜色
    rgb_pattern = r'rgb\((\d+),\s*(\d+),\s*(\d+)\)'
    for match in re.finditer(rgb_pattern, html):
        r, g, b = match.groups()
        colors.add(f"#{int(r):02x}{int(g):02x}{int(b):02x}")

    rgba_pattern = r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)'
    for match in re.finditer(rgba_pattern, html):
        r, g, b = match.groups()
        colors.add(f"#{int(r):02x}{int(g):02x}{int(b):02x}")

    # 移除无效颜色
    valid_colors = set()
    for c in colors:
        if len(c) >= 7:  # 至少6位hex + #
            valid_colors.add(c)

    return valid_colors

def extract_font_families(html):
    """提取字体家族"""
    font_pattern = r'font-family:\s*([^;]+)'
    fonts = re.findall(font_pattern, html, re.IGNORECASE)

    # 清理字体名称
    clean_fonts = set()
    for font in fonts:
        # 提取第一个字体名称（忽略备选字体）
        font_name = font.split(',')[0].strip().strip("'\"")
        clean_fonts.add(font_name)

    return clean_fonts

def extract_font_sizes(html):
    """提取字体大小"""
    size_pattern = r'font-size:\s*(\d+(?:\.\d+)?)(px|rem|em)'
    sizes = re.findall(size_pattern, html, re.IGNORECASE)

    # 转换为px
    px_sizes = []
    for size, unit in sizes:
        size = float(size)
        if unit == 'rem':
            size *= 16
        elif unit == 'em':
            size *= 16
        px_sizes.append(size)

    return px_sizes

def extract_spacing(html):
    """提取间距值"""
    spacing_patterns = [
        r'margin:\s*(\d+(?:\.\d+)?)(px|rem)',
        r'padding:\s*(\d+(?:\.\d+)?)(px|rem)',
        r'gap:\s*(\d+(?:\.\d+)?)(px|rem)',
    ]

    spacing = set()
    for pattern in spacing_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for size, unit in matches:
            size = float(size)
            if unit == 'rem':
                size *= 16
            spacing.add(round(size))

    return sorted(spacing)

def extract_border_radius(html):
    """提取圆角值"""
    radius_pattern = r'border-radius:\s*(\d+(?:\.\d+)?)(px|rem|%)'
    radii = re.findall(radius_pattern, html, re.IGNORECASE)

    px_radii = []
    for size, unit in radii:
        size = float(size)
        if unit == 'rem':
            size *= 16
        elif unit == '%':
            size = min(size, 50)  # 百分比最大50%
        px_radii.append(round(size))

    return sorted(set(px_radii))

def validate_contrast(fg_color, bg_color):
    """验证对比度是否满足WCAG标准"""
    ratio = contrast_ratio(fg_color, bg_color)

    result = {
        "ratio": round(ratio, 2),
        "AA_large": ratio >= 3.0,  # 大文本(>18px)
        "AA_normal": ratio >= 4.5,  # 正常文本
        "AAA_large": ratio >= 4.5,
        "AAA_normal": ratio >= 7.0,
    }
    return result

def analyze_html(html_content):
    """分析HTML的设计特征"""
    analysis = {
        "colors": sorted(list(extract_colors(html_content))),
        "fonts": sorted(list(extract_font_families(html_content))),
        "font_sizes": {
            "min": min(extract_font_sizes(html_content)) if extract_font_sizes(html_content) else 0,
            "max": max(extract_font_sizes(html_content)) if extract_font_sizes(html_content) else 0,
            "count": len(extract_font_sizes(html_content)),
        },
        "spacing": extract_spacing(html_content),
        "border_radius": extract_border_radius(html_content),
    }

    # 计算唯一颜色数量（过多样式可能不一致）
    analysis["color_count"] = len(analysis["colors"])

    return analysis

def validate_design(html_path, check_a11y=False):
    """验证设计一致性"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    analysis = analyze_html(html)

    findings = []
    errors = 0
    warnings = 0
    info = 0

    # 检查1: 颜色数量
    if analysis["color_count"] > 15:
        warnings.append({
            "severity": "warning",
            "message": f"使用了 {analysis['color_count']} 种颜色，可能导致视觉不统一。建议控制在10种以内。"
        })
        warnings += 1
    else:
        info += 1

    # 检查2: 字体数量
    if len(analysis["fonts"]) > 4:
        findings.append({
            "severity": "warning",
            "message": f"使用了 {len(analysis['fonts'])} 种字体: {', '.join(analysis['fonts'])}。建议控制在3种以内保持一致。"
        })
        warnings += 1
    else:
        info += 1

    # 检查3: 字体大小
    min_size = analysis["font_sizes"]["min"]
    if min_size < 12:
        findings.append({
            "severity": "error",
            "message": f"最小字体大小 {min_size}px 低于可访问性最低标准(12px)"
        })
        errors += 1

    # 检查4: 间距一致性
    spacing = analysis["spacing"]
    if spacing:
        # 检查是否存在4px基准的间距系统
        non_base = [s for s in spacing if s % 4 != 0]
        if non_base:
            findings.append({
                "severity": "info",
                "message": f"间距值 {non_base} 不是4的倍数，建议使用4px基准系统(4,8,12,16,24,32...)"
            })
            warnings += 1

    # 检查5: 圆角一致性
    radius = analysis["border_radius"]
    if radius:
        unique_radius = set(radius)
        if len(unique_radius) > 5:
            findings.append({
                "severity": "warning",
                "message": f"使用了 {len(unique_radius)} 种圆角值，建议控制在3-4种以内保持视觉一致"
            })
            warnings += 1

    # 可访问性检查
    if check_a11y:
        # 尝试提取背景色和文本色进行对比度检查
        bg_colors = [c for c in analysis["colors"] if is_light_color(c)]
        text_colors = [c for c in analysis["colors"] if not is_light_color(c)]

        for bg in bg_colors[:3]:  # 检查前3个背景色
            for text in text_colors[:3]:  # 检查前3个文本色
                result = validate_contrast(text, bg)
                if result["AA_normal"]:
                    findings.append({
                        "severity": "info",
                        "message": f"文本对比度: {text} on {bg} = {result['ratio']}:1 (通过AA标准)"
                    })
                else:
                    findings.append({
                        "severity": "error",
                        "message": f"文本对比度不足: {text} on {bg} = {result['ratio']}:1 (需要4.5:1)"
                    })
                    errors += 1

    return {
        "analysis": analysis,
        "findings": findings,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "info": info
        }
    }

def is_light_color(hex_color):
    """判断是否为浅色"""
    try:
        rgb = hex_to_rgb(hex_color)
        luminance = get_luminance(rgb)
        return luminance > 0.5
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description='验证设计一致性')
    parser.add_argument('--input', '-i', required=True,
                        help='输入HTML文件路径')
    parser.add_argument('--check-a11y', '-a', action='store_true',
                        help='检查可访问性(对比度)')
    parser.add_argument('--output', '-o',
                        help='输出JSON结果文件')

    args = parser.parse_args()

    result = validate_design(args.input, args.check_a11y)

    # 输出结果
    print("\n" + "="*50)
    print("设计一致性验证报告")
    print("="*50)

    print(f"\n分析统计:")
    print(f"  颜色数量: {result['analysis']['color_count']}")
    print(f"  字体: {', '.join(result['analysis']['fonts'])}")
    print(f"  字号范围: {result['analysis']['font_sizes']['min']:.0f}px - {result['analysis']['font_sizes']['max']:.0f}px")
    print(f"  间距值: {result['analysis']['spacing']}")
    print(f"  圆角值: {result['analysis']['border_radius']}")

    print(f"\n验证结果:")
    print(f"  错误: {result['summary']['errors']}")
    print(f"  警告: {result['summary']['warnings']}")
    print(f"  提示: {result['summary']['info']}")

    if result['findings']:
        print("\n详细发现:")
        for f in result['findings']:
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[f['severity']]
            print(f"  {icon} {f['message']}")

    # 保存JSON
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存: {args.output}")

if __name__ == '__main__':
    main()
