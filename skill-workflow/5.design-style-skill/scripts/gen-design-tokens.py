#!/usr/bin/env python3
"""
设计Token生成器
根据主题或自定义参数生成Design Token JSON
"""

import json
import argparse
import os
from datetime import datetime

THEMES = {
    "ocean": {
        "name": "Ocean",
        "primary": "#0077cc",
        "secondary": "#6c7278",
        "accent": "#00a8e8",
        "background": "#f8fafc",
        "surface": "#ffffff",
        "text": "#1a1c1e",
        "font": "Inter"
    },
    "forest": {
        "name": "Forest",
        "primary": "#2d5a27",
        "secondary": "#6c7278",
        "accent": "#8bc34a",
        "background": "#f5f7f2",
        "surface": "#ffffff",
        "text": "#1a1c1e",
        "font": "Inter"
    },
    "sunset": {
        "name": "Sunset",
        "primary": "#ff6b6b",
        "secondary": "#6c7278",
        "accent": "#feca57",
        "background": "#fff9f5",
        "surface": "#ffffff",
        "text": "#1a1c1e",
        "font": "Inter"
    },
    "dark": {
        "name": "Dark",
        "primary": "#ffffff",
        "secondary": "#8e9192",
        "accent": "#00a8e8",
        "background": "#0b1326",
        "surface": "#171f33",
        "text": "#ffffff",
        "font": "Inter"
    },
    "glassmorphism": {
        "name": "Glassmorphism",
        "primary": "#6366f1",
        "secondary": "#8e9192",
        "accent": "#22d3ee",
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "surface": "rgba(255, 255, 255, 0.1)",
        "text": "#ffffff",
        "font": "Inter"
    },
    "elegant": {
        "name": "Elegant",
        "primary": "#1a1c1e",
        "secondary": "#6c7278",
        "accent": "#8b7355",
        "background": "#faf9f7",
        "surface": "#ffffff",
        "text": "#1a1c1e",
        "font": "Georgia"
    }
}

def generate_token(theme_name, custom_colors=None):
    """生成Design Token"""
    if theme_name and theme_name in THEMES:
        theme = THEMES[theme_name]
    else:
        theme = THEMES["ocean"]

    colors = {
        "primary": custom_colors.get("primary", theme["primary"]) if custom_colors else theme["primary"],
        "secondary": custom_colors.get("secondary", theme["secondary"]) if custom_colors else theme["secondary"],
        "tertiary": custom_colors.get("accent", theme["accent"]) if custom_colors else theme["accent"],
        "background": custom_colors.get("background", theme["background"]) if custom_colors else theme["background"],
        "surface": custom_colors.get("surface", theme["surface"]) if custom_colors else theme["surface"],
        "text": custom_colors.get("text", theme["text"]) if custom_colors else theme["text"],
    }

    token = {
        "version": "alpha",
        "name": custom_colors.get("name", theme["name"]) if custom_colors else theme["name"],
        "colors": colors,
        "typography": {
            "display-lg": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "84px",
                "fontWeight": 700,
                "lineHeight": 1.07,
                "letterSpacing": "-0.04em"
            },
            "headline-lg": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "32px",
                "fontWeight": 600,
                "lineHeight": 1.25,
                "letterSpacing": "-0.02em"
            },
            "headline-md": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "24px",
                "fontWeight": 500,
                "lineHeight": 1.33
            },
            "body-lg": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "18px",
                "fontWeight": 400,
                "lineHeight": 1.56
            },
            "body-md": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "16px",
                "fontWeight": 400,
                "lineHeight": 1.5
            },
            "label-sm": {
                "fontFamily": custom_colors.get("font", theme["font"]) if custom_colors else theme["font"],
                "fontSize": "12px",
                "fontWeight": 500,
                "lineHeight": 1.33
            }
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
            "3xl": "64px"
        },
        "rounded": {
            "none": "0px",
            "sm": "4px",
            "md": "8px",
            "lg": "16px",
            "xl": "24px",
            "full": "9999px"
        },
        "shadow": {
            "sm": "0 1px 2px rgba(0,0,0,0.05)",
            "md": "0 4px 6px rgba(0,0,0,0.1)",
            "lg": "0 10px 15px rgba(0,0,0,0.1)",
            "xl": "0 20px 25px rgba(0,0,0,0.15)"
        },
        "motion": {
            "fast": "120ms",
            "normal": "250ms",
            "slow": "400ms",
            "easing": "cubic-bezier(0.2, 0, 0, 1)"
        }
    }
    return token

def list_themes():
    """列出所有可用主题"""
    print("\n可用主题:")
    print("-" * 40)
    for name, theme in THEMES.items():
        print(f"  {name:15} - {theme['name']}")
    print()

def save_token(token, output_path):
    """保存Token到文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(token, f, indent=2, ensure_ascii=False)
    print(f"Design Token已保存: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='生成Design Token')
    parser.add_argument('--theme', '-t', choices=list(THEMES.keys()),
                        help='选择预设主题')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有可用主题')
    parser.add_argument('--output', '-o',
                        default='design-tokens.json',
                        help='输出文件路径')
    parser.add_argument('--primary', help='主色 (hex)')
    parser.add_argument('--secondary', help='次要色 (hex)')
    parser.add_argument('--accent', help='强调色 (hex)')
    parser.add_argument('--background', help='背景色')
    parser.add_argument('--font', help='字体')

    args = parser.parse_args()

    if args.list:
        list_themes()
        return

    custom_colors = None
    if args.primary or args.secondary or args.accent:
        custom_colors = {
            "name": "Custom",
            "primary": args.primary,
            "secondary": args.secondary,
            "accent": args.accent,
            "background": args.background,
            "font": args.font
        }

    token = generate_token(args.theme, custom_colors)
    save_token(token, args.output)

if __name__ == '__main__':
    main()
