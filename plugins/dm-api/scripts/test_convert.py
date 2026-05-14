"""测试解析脚本 - 只输出不覆盖"""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))

from convert_docs import parse_by_sections, parse_parameters, parse_signature, parse_return_values, parse_examples, parse_notes, generate_new_format, get_description
from pathlib import Path

# 测试几个代表性文件
test_files = [
    ('图色', 'FindPic'),
    ('后台设置', 'BindWindow'),
    ('文字识别', 'FindStr'),
    ('内存', 'ReadInt'),
    ('窗口', 'FindWindow'),
    ('Ai', 'AiFindPic'),
    ('基本设置', 'Reg'),
    ('系统', 'GetTime'),
]

root = Path(r'C:\AI\m_projects\m_agents\terr-marketplace\plugins\dm-api\references\dm_api_docs')

for category, func_name in test_files:
    file_path = root / category / f'{func_name}.md'
    if not file_path.exists():
        print(f'[跳过] {file_path} 不存在')
        continue

    content = file_path.read_text(encoding='utf-8')
    raw = parse_by_sections(content)
    parsed = {
        'desc_raw': raw.get('函数简介:', ''),
        'signature': parse_signature(raw.get('函数原型:', '')),
        'parameters': parse_parameters(raw.get('参数定义:', '')),
        'returns': parse_return_values(raw.get('返回值:', '')),
        'examples': parse_examples(raw.get('示例:', '')),
        'notes': parse_notes(raw.get('注:', '') or raw.get('注意:', ''))
    }
    parsed['description'] = parsed['desc_raw']

    new_content = generate_new_format(func_name, category, parsed)

    # 输出到测试目录
    out_dir = Path(r'C:\AI\m_projects\m_agents\terr-marketplace\plugins\dm-api\test_output') / category
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f'{func_name}.md').write_text(new_content, encoding='utf-8')

    print(f'[OK] {category}/{func_name}')
    print(f'  参数: {len(parsed["parameters"])} 个')
    print(f'  注意: {len(parsed["notes"])} 条')
    print(f'  签名: {parsed["signature"][:80]}...' if len(parsed['signature']) > 80 else f'  签名: {parsed["signature"]}')

print('\n测试输出目录: test_output/')
