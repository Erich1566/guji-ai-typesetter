#!/usr/bin/env python3
"""
Agent 控制下的古籍自动排版脚本 (生成芸窗古籍AI排版系统可直接导入的 .guji.json 工程)
"""

import argparse
import json
import math
import re
from pathlib import Path

GENRE_PRESETS = {
    'jing_zhushu': {
        'preset': 'song_sibu',
        'colsPerHalf': 9,
        'rowsPerCol': 18,
        'borderStyle': 'lr_double',
        'gridRule': 'wusi',
        'fishtail': 'single_solid',
        'mouth': 'thin_black',
        'paper': 'paper-bamboo',
        'judou': 'vermilion_side',
        'desc': '经部注疏/宋刻本规制（左右双边、乌丝栏、半叶9行×18字）'
    },
    'baiwen_kui': {
        'preset': 'edo_kui',
        'colsPerHalf': 7,
        'rowsPerCol': 14,
        'borderStyle': 'all_double',
        'gridRule': 'wusi',
        'fishtail': 'double_solid',
        'mouth': 'thick_black',
        'paper': 'paper-xuan',
        'judou': 'vermilion_side',
        'desc': '白文诵习魁本大字（四周双边、半叶7行×14字）'
    },
    'shibu_siku': {
        'preset': 'siku_zhusi',
        'colsPerHalf': 8,
        'rowsPerCol': 20,
        'borderStyle': 'all_double',
        'gridRule': 'zhusi',
        'fishtail': 'hollow_floral',
        'mouth': 'thin_black',
        'paper': 'paper-xuan',
        'judou': 'vermilion_side',
        'desc': '史部/四库朱丝栏（四周双边、朱丝栏、花鱼尾、半叶8行×20字）'
    },
    'shici_biji': {
        'preset': 'qing_langhuan',
        'colsPerHalf': 9,
        'rowsPerCol': 18,
        'borderStyle': 'all_double',
        'gridRule': 'wusi',
        'fishtail': 'double_solid',
        'mouth': 'thick_black',
        'paper': 'paper-bamboo',
        'judou': 'vermilion_side',
        'desc': '诗词总集/清刻琅环阁本（双黑鱼尾、大黑口、半叶9行×18字）'
    }
}


def estimate_leaves(text: str, cols_per_half: int, rows_per_col: int) -> int:
    clean = re.sub(r'\[[^\]]+\]', '', text)
    char_count = len(re.sub(r'\s+', '', clean))
    chars_per_leaf = cols_per_half * 2 * rows_per_col
    return max(1, math.ceil(char_count / max(1, chars_per_leaf)))


def main():
    parser = argparse.ArgumentParser(description='Agent 自动生成古籍排版工程文件 (.guji.json)')
    parser.add_argument('--input', '-i', required=True, help='规范化古籍文本路径')
    parser.add_argument('--title', required=True, help='书名')
    parser.add_argument('--author', default='〔佚名〕撰', help='撰者/校注者')
    parser.add_argument('--volume', default='卷一', help='默认卷次')
    parser.add_argument('--publisher', default='芸窗精校重梓', help='版心下款/藏板堂号')
    parser.add_argument('--genre', choices=list(GENRE_PRESETS.keys()), default='jing_zhushu', help='体裁与版式预设')
    parser.add_argument('--output-json', '-o', required=True, help='输出 .guji.json 工程路径')
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding='utf-8')
    cfg = GENRE_PRESETS[args.genre]
    est_leaves = estimate_leaves(text, cfg['colsPerHalf'], cfg['rowsPerCol'])
    volumes = re.findall(r'\[卷[标標][:：]([^\]]+)\]', text) or [args.volume]

    project = {
        'schema': 'yunchuang-guji-project/v1',
        'bookTitle': args.title,
        'bookVolume': args.volume,
        'bookAuthor': args.author,
        'publisher': args.publisher,
        'coverTitle': args.title,
        'paijiCenter': args.title,
        'paijiLeft': f"{args.publisher} · 依善本精校重梓",
        'preset': cfg['preset'],
        'colsPerHalf': cfg['colsPerHalf'],
        'rowsPerCol': cfg['rowsPerCol'],
        'borderStyle': cfg['borderStyle'],
        'gridRule': cfg['gridRule'],
        'fishtail': cfg['fishtail'],
        'mouth': cfg['mouth'],
        'paper': cfg['paper'],
        'judou': cfg['judou'],
        'sourceText': text
    }

    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"OK: 已生成古籍排版工程 {out_path}")
    print(f"版式规格: {cfg['desc']}")
    print(f"识别卷次: {', '.join(volumes)}")
    print(f"预计成书: 约 {est_leaves} 叶（筒子页）")


if __name__ == '__main__':
    main()
