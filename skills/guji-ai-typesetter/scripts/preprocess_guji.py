#!/usr/bin/env python3
"""
古籍文本预处理与规范化脚本 (供 Codex / WorkBuddy / CLI Agent 调用)
功能：
1. 支持读取普通 TXT / Markdown 以及 chinese-poetry JSON 格式语料
2. 清理冗余空白与现代排版符号，分离正文与注疏括号 -> 【双行夹注】
3. 可选将现代标点规范化为古籍句读（。、）
4. 自动识别卷次标题并生成 [卷标:...] 与 [书耳:...]
"""

import argparse
import json
import re
from pathlib import Path


def convert_modern_punct_to_judou(text: str) -> str:
    text = re.sub(r'[！？；!?;]', '。', text)
    text = re.sub(r'[，,：:]', '、', text)
    text = re.sub(r'[“”"‘’\'《》〈〉]', lambda m: m.group(0) if m.group(0) in '《》〈〉' else '', text)
    return text


def normalize_inline_notes(text: str) -> str:
    # 将全角/半角圆括号内的注释转换为 【双行夹注】
    text = re.sub(r'（([^（）\n]{2,300})）', r'【\1】', text)
    text = re.sub(r'\(([^()\n]{2,300})\)', r'【\1】', text)
    # 识别独立成行的“注曰：”、“按：”、“疏曰：”并转为夹注
    lines = text.splitlines()
    out_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^(注[曰云]?|按|案|疏[曰云]?|音義|集解)[:：]', stripped):
            out_lines.append(f'【{stripped}】')
        else:
            out_lines.append(line)
    return '\n'.join(out_lines)


def auto_split_volumes(text: str) -> str:
    lines = text.splitlines()
    out_lines = []
    vol_pattern = re.compile(r'^(卷[一二三四五六七八九十百零上中下全\d]+|第[一二三四五六七八九十百零\d]+[卷章回篇])\s*(.*)$')
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            out_lines.append('')
            continue
        m = vol_pattern.match(stripped)
        if m and '[卷标:' not in stripped:
            vol_tag = m.group(1)
            rest = m.group(2).strip()
            ear = (rest or vol_tag)[:4]
            out_lines.append(f'[卷标:{vol_tag}][书耳:{ear}]{stripped}')
        else:
            out_lines.append(stripped)
    return '\n'.join(out_lines)


def load_input_text(input_path: Path) -> str:
    raw = input_path.read_text(encoding='utf-8')
    if input_path.suffix.lower() == '.json':
        data = json.loads(raw)
        if isinstance(data, list):
            parts = []
            for idx, item in enumerate(data):
                if isinstance(item, dict):
                    title = item.get('title') or item.get('rhythmic') or item.get('chapter') or f'篇{idx+1}'
                    author = item.get('author', '')
                    paragraphs = item.get('paragraphs') or item.get('content') or []
                    if isinstance(paragraphs, str):
                        paragraphs = [paragraphs]
                    header = f'《{title}》' + (f'【〈{author}〉】' if author else '')
                    parts.append(header + '\n' + '\n'.join(paragraphs))
            return '\n'.join(parts)
    return raw


def main():
    parser = argparse.ArgumentParser(description='古籍文本预处理与规范化工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径 (.txt/.md/.json)')
    parser.add_argument('--output', '-o', required=True, help='输出规范化古籍文本路径')
    parser.add_argument('--judou', action='store_true', help='将现代标点转换为传统句读（。、）')
    parser.add_argument('--auto-notes', action='store_true', help='自动识别注疏并转换为【双行夹注】')
    parser.add_argument('--split-volumes', action='store_true', help='自动识别卷次并插入[卷标:]与[书耳:]')
    args = parser.parse_args()

    text = load_input_text(Path(args.input))
    # 清理多余空格与空行
    text = re.sub(r'[ \t]+', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()

    if args.auto_notes:
        text = normalize_inline_notes(text)
    if args.judou:
        text = convert_modern_punct_to_judou(text)
    if args.split_volumes:
        text = auto_split_volumes(text)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding='utf-8')
    print(f'OK: 已完成古籍文本规范化，输出至 {out_path}（共 {len(text)} 字符）')


if __name__ == '__main__':
    main()
