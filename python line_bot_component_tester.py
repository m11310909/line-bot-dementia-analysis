#!/usr/bin/env python3
"""
Flex Component Inspector
Analyze and visualize LINE Flex Message components
"""

import json
import os
from pathlib import Path


def analyze_flex_message(json_file):
    """Analyze a flex message JSON structure"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n📄 Analyzing: {json_file}")
        print("=" * 40)

        # Check message type
        if 'type' in data:
            print(f"🔧 Message Type: {data['type']}")

        # Look for flex content
        flex_content = None
        if 'altText' in data:
            print(f"📝 Alt Text: {data['altText']}")

        if 'contents' in data:
            flex_content = data['contents']
        elif 'template' in data and 'contents' in data['template']:
            flex_content = data['template']['contents']

        if flex_content:
            print(f"📦 Flex Type: {flex_content.get('type', 'Unknown')}")

            # Analyze components
            components = find_components(flex_content)
            if components:
                print("🎯 Components Found:")
                for comp in components:
                    print(f"  • {comp}")
            else:
                print("⚠️ No recognizable components found")

            # Check color scheme
            colors = find_colors(flex_content)
            if colors:
                print(f"🎨 Colors Used: {', '.join(colors)}")

            # Check layout structure
            structure = analyze_structure(flex_content)
            if structure:
                print(f"🏗️ Layout: {structure}")

        return True

    except Exception as e:
        print(f"❌ Error analyzing {json_file}: {e}")
        return False


def find_components(content, components=None):
    """Recursively find components in flex content"""
    if components is None:
        components = []

    if isinstance(content, dict):
        # Check for component indicators
        if 'text' in content:
            text = content['text']
            if '正常老化' in text or '警訊特徵' in text:
                components.append('⚠️ Comparison Card')
            if '信心度' in text or '%' in text:
                components.append('📊 Confidence Meter')
            if '分析說明' in text or 'AI 解釋' in text:
                components.append('💡 XAI Box')
            if '建議步驟' in text or '下一步' in text:
                components.append('🎯 Action Card')
            if '時間軸' in text or '追蹤' in text:
                components.append('📅 Timeline List')
            if '重要提醒' in text or '注意' in text:
                components.append('🚨 Warning Box')

        # Check for specific styling that indicates components
        if 'backgroundColor' in content:
            bg_color = content['backgroundColor']
            if bg_color in ['#ffebee', '#fff3e0']:  # Warning colors
                components.append('🚨 Warning Element')
            elif bg_color in ['#e8f5e8', '#f0f8ff']:  # Info colors
                components.append('ℹ️ Info Element')

        # Recurse through nested content
        for key, value in content.items():
            if key in ['body', 'header', 'footer', 'contents']:
                find_components(value, components)

    elif isinstance(content, list):
        for item in content:
            find_components(item, components)

    return list(set(components))  # Remove duplicates


def find_colors(content, colors=None):
    """Find all colors used in the flex message"""
    if colors is None:
        colors = set()

    if isinstance(content, dict):
        for key, value in content.items():
            if 'color' in key.lower() and isinstance(value, str):
                colors.add(value)
            elif isinstance(value, (dict, list)):
                find_colors(value, colors)
    elif isinstance(content, list):
        for item in content:
            find_colors(item, colors)

    return list(colors)


def analyze_structure(content):
    """Analyze the layout structure"""
    if isinstance(content, dict):
        if content.get('type') == 'bubble':
            sections = []
            if 'header' in content:
                sections.append('Header')
            if 'body' in content:
                sections.append('Body')
            if 'footer' in content:
                sections.append('Footer')
            return f"Bubble with {', '.join(sections)}"
        elif content.get('type') == 'carousel':
            bubbles = len(content.get('contents', []))
            return f"Carousel with {bubbles} bubbles"
        elif content.get('type') == 'box':
            layout = content.get('layout', 'unknown')
            return f"Box ({layout})"

    return "Unknown structure"


def main():
    """Main function to inspect all test files"""
    print("🔍 Flex Component Inspector")
    print("=" * 50)

    # Find all test JSON files
    test_files = list(Path('.').glob('test_*.json'))

    if not test_files:
        print("❌ No test JSON files found. Run the component tester first.")
        return

    analyzed_count = 0
    for test_file in test_files:
        if analyze_flex_message(test_file):
            analyzed_count += 1

    print(f"\n📊 Analysis Summary")
    print("=" * 50)
    print(f"Files analyzed: {analyzed_count}/{len(test_files)}")
    print("\n💡 Tips:")
    print("• Send the same messages to your LINE Bot to see visual results")
    print("• Use LINE Bot Designer to preview flex messages")
    print("• Test on different devices for compatibility")


if __name__ == "__main__":
    main()
