#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'exercises.json'
OUT = ROOT / 'data' / 'exercises.zh-HK.json'

# Best-effort translation map for the dataset's English names.
# Any unmatched item falls back to the original English label in zh-HK mode.
TRANSLATIONS = {
    '3/4 sit-up': '3/4 仰臥起坐',
    '45° side bend': '45° 側屈',
    'air bike': '空中腳踏車',
    'alternate heel touchers': '交替腳跟觸碰',
    'alternate lateral pulldown': '交替側拉下拉',
    'alt row': '交替划船',
    'alternating lunge': '交替箭步蹲',
    'arm circles': '手臂轉圈',
    'assisted dip': '輔助下壓',
    'back extension': '背部伸展',
    'barbell bench press': '槓鈴臥推',
    'barbell deadlift': '槓鈴硬舉',
    'barbell front squat': '槓鈴前蹲',
    'barbell full squat': '槓鈴深蹲',
    'barbell hip thrust': '槓鈴臀推',
    'barbell overhead press': '槓鈴肩上推舉',
    'barbell row': '槓鈴划船',
    'barbell shrug': '槓鈴耸肩',
    'barbell squat': '槓鈴深蹲',
    'bent-over row': '俯身划船',
    'bench press': '臥推',
    'biceps curl': '二頭肌彎舉',
    'bird dog': '鳥犬式',
    'bodyweight squat': '自重深蹲',
    'bodyweight row': '自重划船',
    'cable chest press': '纜繩胸推',
    'cable row': '纜繩划船',
    'calf raise': '小腿抬升',
    'chest press': '胸推',
    'close-grip bench press': '窄握臥推',
    'crunch': '腹部捲曲',
    'dead bug': '仰臥撐腿',
    'deadlift': '硬舉',
    'decline bench press': '下斜臥推',
    'dips': '下壓',
    'dumbbell biceps curl': '啞鈴二頭肌彎舉',
    'dumbbell floor press': '啞鈴地面推舉',
    'dumbbell lateral raise': '啞鈴側平舉',
    'dumbbell overhead press': '啞鈴肩上推舉',
    'dumbbell row': '啞鈴划船',
    'dumbbell shoulder press': '啞鈴肩推',
    'front raise': '前平舉',
    'good morning': '早晨挺身',
    'hammer curl': '反握彎舉',
    'hang clean': '懸掛潔淨',
    'hip thrust': '臀推',
    'incline bench press': '上斜臥推',
    'kettlebell clean': '壺鈴潔淨',
    'kettlebell deadlift': '壺鈴硬舉',
    'kettlebell swing': '壺鈴擺盪',
    'lat pulldown': '拉背下拉',
    'leg curl': '腿屈曲',
    'leg extension': '腿伸展',
    'leg press': '腿推',
    'lunge': '箭步蹲',
    'medicine ball slam': '藥球砸地',
    'mountain climber': '爬山式',
    'overhead press': '頭上推舉',
    'plank': '平板支撐',
    'pull-up': '引體向上',
    'push-up': '伏地挺身',
    'reverse fly': '反向飛鳥',
    'romanian deadlift': '羅馬尼亞硬舉',
    'russian twist': '俄式扭腰',
    'seated cable row': '坐姿纜繩划船',
    'shoulder press': '肩推',
    'single-leg deadlift': '單腿硬舉',
    'sit-up': '仰臥起坐',
    'squat': '深蹲',
    'standing calf raise': '站姿小腿抬升',
    'sumo squat': '相撲深蹲',
    'triceps dip': '三頭肌下壓',
    'triceps extension': '三頭肌伸展',
    'walking lunge': '走步箭步蹲',
    'wide-grip pull-up': '寬握引體向上',
    'yogi squat': '瑜伽深蹲',
    'bird dog': '鳥犬式',
    'all fours squad stretch': '四肢跪姿股四頭肌拉伸',
    'arm slingers hanging bent knee legs': '懸垂屈膝腿伸展',
    'archer pull up': '弓箭引體向上',
    'archer push up': '弓箭伏地挺身',
    'ankle circles': '腳踝轉圈',
    'band pull-apart': '橡膠帶分開拉伸',
    'band row': '橡膠帶划船',
    'barbell clean': '槓鈴潔淨',
    'barbell floor press': '槓鈴地面推舉',
    'barbell reverse curl': '槓鈴反握彎舉',
    'barbell shrug': '槓鈴耸肩',
    'bear crawl': '熊爬',
    'bridge': '橋式',
    'burpee': '波比跳',
    'cable curl': '纜繩彎舉',
    'cable fly': '纜繩飛鳥',
    'cable pulldown': '纜繩下拉',
    'chest dip': '胸部下壓',
    'chin-up': '下握引體向上',
    'diamond push-up': '鑽石伏地挺身',
    'dumbbell chest fly': '啞鈴胸飛鳥',
    'dumbbell clean': '啞鈴潔淨',
    'dumbbell deadlift': '啞鈴硬舉',
    'dumbbell pullover': '啞鈴拉過',
    'dumbbell squat': '啞鈴深蹲',
    'hang pull-up': '懸垂引體向上',
    'inverted row': '反向划船',
    'jump squat': '跳躍深蹲',
    'knee push-up': '跪姿伏地挺身',
    'lateral lunge': '側箭步蹲',
    'machine chest press': '機械胸推',
    'machine row': '機械划船',
    'oblique crunch': '斜腹捲曲',
    'overhead triceps extension': '頭上三頭肌伸展',
    'pike push-up': '俯身推',
    'seated twist': '坐姿扭腰',
    'shoulder tap': '肩部點觸',
    'split squat': '分腿深蹲',
    'step-up': '上台階',
    'superman': '超人式',
    'tricep kickback': '三頭肌反向伸展',
    'reverse wrist curl': '反向手腕彎舉',
    'jumping jacks': '開合跳',
    'wall sit': '牆坐',
    'farmer carry': '農夫搬運',
    'suitcase carry': '行李箱搬運',
    'single-arm row': '單臂划船',
    'incline dumbbell press': '上斜啞鈴推舉',
    'decline dumbbell press': '下斜啞鈴推舉',
    'lying leg curl': '臥式腿屈曲',
    'standing leg curl': '站立腿屈曲',
    'seated leg curl': '坐姿腿屈曲',
    'cross-body crunch': '交叉腹捲',
    'hollow body hold': '空心橋停住',
    'leg raise': '腿抬舉',
    'turkish get-up': '土耳其式起身',
    'side plank': '側平板支撐',
    'cobra stretch': '眼鏡蛇伸展',
    'child pose': '孩子姿勢'
}


def localize_name(name: str) -> str:
    name_lower = name.strip().lower()
    if name_lower in TRANSLATIONS:
        return TRANSLATIONS[name_lower]
    # Heuristic fallback for common patterns
    if 'press' in name_lower:
        return name + '（推舉）'
    if 'squat' in name_lower:
        return name + '（深蹲）'
    if 'row' in name_lower:
        return name + '（划船）'
    if 'curl' in name_lower:
        return name + '（彎舉）'
    if 'pull' in name_lower or 'pulldown' in name_lower:
        return name + '（拉伸）'
    if 'lunge' in name_lower:
        return name + '（箭步蹲）'
    if 'raise' in name_lower:
        return name + '（抬舉）'
    if 'dip' in name_lower:
        return name + '（下壓）'
    return name


def main():
    with SOURCE.open('r', encoding='utf-8') as f:
        items = json.load(f)

    output = {
        'language': 'zh-HK',
        'source': 'data/exercises.json',
        'generated_from': 'dataset english names',
        'count': len(items),
        'entries': []
    }

    for item in items:
        output['entries'].append({
            'id': item.get('id'),
            'name': item.get('name'),
            'name_zh_hk': localize_name(item.get('name', '')),
            'category': item.get('category'),
            'body_part': item.get('body_part'),
            'equipment': item.get('equipment'),
            'target': item.get('target'),
            'muscle_group': item.get('muscle_group')
        })

    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {len(output["entries"])} entries to {OUT}')


if __name__ == '__main__':
    main()
