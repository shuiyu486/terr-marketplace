"""
将旧格式的大漠插件 API 文档转换为 AI 友好的结构化格式。
同时生成 functions_index.json 函数索引。

旧格式: 冗长的中文描述，不规则空白，参数格式松散
新格式: 结构化 Markdown，表格参数，标准化类型，精简描述
"""

import re
import os
import json
from pathlib import Path

# 中文类型 → 英文简写
TYPE_NORMALIZE = {
    '整形数': 'int',
    '长整形数': 'long',
    '字符串': 'str',
    '双精度浮点数': 'double',
    '单精度浮点数': 'float',
    '变参指针': 'int*',
    '整形数:': 'int',
    '字符串:': 'str',
    '双精度浮点数:': 'double',
    '单精度浮点数:': 'float',
    '变参指针:': 'int*',
}

SECTION_MARKERS = ['函数简介:', '函数原型:', '参数定义:', '返回值:', '示例:', '注:', '注意:']


def normalize_type(cn_type: str) -> str:
    """将中文类型名标准化为英文简写"""
    for cn, en in TYPE_NORMALIZE.items():
        if cn_type.startswith(cn):
            return en
    return cn_type.strip().rstrip(':').strip()


def clean_lines(text: str) -> str:
    """清理多余空白和换行"""
    lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    return ' '.join(lines)


def parse_by_sections(content: str) -> dict:
    """使用状态机按章节解析文档"""
    sections = {m: '' for m in SECTION_MARKERS}
    current_section = None
    current_lines = []

    for line in content.split('\n'):
        stripped = line.strip()
        found_marker = None
        for marker in SECTION_MARKERS:
            if stripped.startswith(marker):
                found_marker = marker
                break

        if found_marker:
            if current_section:
                sections[current_section] = '\n'.join(current_lines)
            current_section = found_marker
            # 保留标记行中标记后的内容
            remaining = stripped[len(found_marker):].strip()
            current_lines = [remaining] if remaining else []
        elif current_section:
            current_lines.append(line)

    if current_section and current_lines:
        sections[current_section] = '\n'.join(current_lines)

    return sections


def parse_signature(raw: str) -> str:
    """从原始文本提取函数签名"""
    raw = raw.strip()
    # 移除多余的换行和空白
    sig = ' '.join(raw.split())
    # 还原 Markdown 转义的下划线
    sig = sig.replace('\\_', '_')
    # 确保是一个干净的签名行
    return sig


def parse_parameters(raw: str) -> list[dict]:
    """解析参数列表，处理同行多参数、无空格紧密格式等情况"""
    params = []
    raw = raw.strip()
    if not raw:
        return params

    # 预处理: 还原 Markdown 转义
    raw = raw.replace('\\_', '_')

    CN_TYPES = r'(?:整形数|长整形数|字符串|双精度浮点数|单精度浮点数|变参指针)'
    # 参数起始模式: param_name + (可选空格) + 中文类型名
    PARAM_START = re.compile(rf'([a-zA-Z_]\w*)\s*{CN_TYPES}')

    lines = raw.split('\n')

    # 合并断行——不以参数模式开头的行视为上一行的续行
    merged = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if merged and not PARAM_START.match(stripped) and not stripped[0].isdigit():
            merged[-1] += ' ' + stripped
        else:
            merged.append(stripped)

    # 解析每行（可能含多个参数）
    for param_line in merged:
        param_line = re.sub(r'^\d+\.\s*', '', param_line)
        # 找出该行所有参数起始位置
        matches = list(re.finditer(rf'([a-zA-Z_]\w*)\s*({CN_TYPES})[:：]?', param_line))
        if not matches:
            continue

        for i, m in enumerate(matches):
            name = m.group(1)
            raw_type = m.group(2)
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(param_line)
            desc = param_line[start:end].strip().lstrip(':').strip()
            params.append({
                'name': name,
                'type': normalize_type(raw_type),
                'desc': desc
            })

    return params


def parse_return_values(raw: str) -> str:
    """清理返回值描述，过滤掉裸类型声明行，合并续行"""
    raw = raw.strip()
    lines = []
    for line in raw.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        # 跳过裸类型声明行 (如 "整形数:", "字符串:")
        if re.match(r'^(整形数|字符串|双精度浮点数|长整形数|变参指针)[:：]?\s*$', stripped):
            continue
        # 检测是否为续行 (不以值标记 '-' 或数字开头)
        if lines and not re.match(r'^-?\d+', stripped) and not stripped.startswith('-'):
            lines[-1] += ' ' + stripped
        else:
            lines.append(stripped)

    text = '\n'.join(lines)
    text = re.sub(r' {2,}', ' ', text)
    return text


def parse_examples(raw: str) -> str:
    """清理示例代码"""
    lines = raw.split('\n')
    code_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if code_lines and code_lines[-1] != '':
                code_lines.append('')
            continue
        code_lines.append(stripped)

    # 移除首尾空行
    while code_lines and not code_lines[0]:
        code_lines.pop(0)
    while code_lines and not code_lines[-1]:
        code_lines.pop()

    # 合并断开的赋值语句: "dm_ret =" 后紧跟 "dm.Func(...)" → "dm_ret = dm.Func(...)"
    merged = []
    i = 0
    while i < len(code_lines):
        line = code_lines[i]
        # 还原 Markdown 转义
        line = line.replace('\\_', '_')
        # 检查是否是独立的赋值左值 (dm_ret =)
        if re.match(r'^(dm_ret|value|hwnd|foobar|t\d+|ver|dm_ver)\s*=\s*$', line) and i + 1 < len(code_lines):
            merged.append(line + ' ' + code_lines[i + 1].lstrip())
            i += 2
        else:
            merged.append(line)
            i += 1

    return '\n'.join(merged)


def parse_notes(raw: str) -> list[str]:
    """解析注意事项"""
    raw = raw.strip()
    if not raw:
        return []

    notes = []
    for line in raw.split('\n'):
        stripped = line.strip()
        if stripped and len(stripped) > 3:
            # 移除编号
            stripped = re.sub(r'^\d+\.\s*', '', stripped)
            notes.append(stripped)

    # 过滤太短的行(可能是残片)
    notes = [n for n in notes if len(n) > 5]
    return notes


def get_description(raw: str) -> str:
    """从原始简介提取一句话描述"""
    raw = raw.strip()
    # 还原 Markdown 转义
    raw = raw.replace('\\_', '_')
    # 取第一句
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    if not lines:
        return ''
    desc = lines[0]
    # 截断过长的描述 (保留核心意思)
    if len(desc) > 200:
        # 尝试在第一句结束处截断
        for sep in ['。', '，', '；']:
            idx = desc[:200].rfind(sep)
            if idx > 50:
                desc = desc[:idx + 1]
                break
        else:
            desc = desc[:200]
    return desc


def generate_new_format(func_name: str, category: str, parsed: dict) -> str:
    """生成新的 AI 友好格式文档"""
    parts = []

    # 标题
    parts.append(f'# {func_name}')
    parts.append('')

    # 元数据行
    parts.append(f'**分类:** {category}')
    parts.append('')

    # 签名
    sig = parsed.get('signature', '')
    parts.append(f'**签名:** `{sig}`')
    parts.append('')

    # 描述
    desc = parsed.get('description', '') or parsed.get('desc_raw', '')
    desc_text = get_description(desc)
    parts.append(f'**描述:** {desc_text}')
    parts.append('')

    # 参数
    params = parsed.get('parameters', [])
    if params:
        parts.append('## 参数')
        parts.append('')
        parts.append('| 参数 | 类型 | 说明 |')
        parts.append('|------|------|------|')
        for p in params:
            parts.append(f'| {p["name"]} | {p["type"]} | {p["desc"]} |')
        parts.append('')
    else:
        parts.append('## 参数')
        parts.append('')
        parts.append('*此函数无参数。*')
        parts.append('')

    # 返回值
    returns = parsed.get('returns', '')
    parts.append('## 返回值')
    parts.append('')
    if returns:
        # 尝试格式化返回值列表
        ret_text = parse_return_values(returns)
        for rline in ret_text.split('\n'):
            rline = rline.strip()
            if rline:
                parts.append(f'- {rline}')
    else:
        parts.append('- *无返回值说明*')
    parts.append('')

    # 示例
    examples = parsed.get('examples', '')
    if examples:
        parts.append('## 示例')
        parts.append('')
        parts.append('```vbs')
        parts.append(examples)
        parts.append('```')
        parts.append('')
    else:
        parts.append('## 示例')
        parts.append('')
        parts.append('*无示例代码。*')
        parts.append('')

    # 注意
    notes = parsed.get('notes', [])
    if notes:
        parts.append('## 注意')
        parts.append('')
        for note in notes:
            parts.append(f'- {note}')
        parts.append('')

    return '\n'.join(parts)


def build_function_info(func_name: str, category: str, parsed: dict) -> dict:
    """从解析结果构建索引条目"""
    params = parsed.get('parameters', [])
    sig = parsed.get('signature', '')
    desc = parsed.get('description', '') or parsed.get('desc_raw', '')

    return {
        'name': func_name,
        'category': category,
        'signature': sig,
        'description': get_description(desc),
        'param_count': len(params),
        'params': [{k: p[k] for k in ['name', 'type', 'desc']} for p in params]
    }


def convert_all_docs(docs_root: str, force: bool = False):
    """转换所有文档"""
    root = Path(docs_root)
    if not root.exists():
        print(f'错误: 目录不存在 {docs_root}')
        return

    all_functions = []
    stats = {'converted': 0, 'failed': 0, 'skipped': 0}

    for category_dir in sorted(root.iterdir()):
        if not category_dir.is_dir():
            continue

        category = category_dir.name
        md_files = list(category_dir.glob('*.md'))

        for md_file in md_files:
            func_name = md_file.stem

            try:
                content = md_file.read_text(encoding='utf-8')
                if not content.strip():
                    stats['skipped'] += 1
                    continue

                # 检查是否已经是新格式 (以 "# " 开头且包含 "**分类:**")
                if not force and content.startswith('# ') and '**分类:**' in content[:200]:
                    stats['skipped'] += 1
                    continue

                # 解析旧格式
                raw_sections = parse_by_sections(content)

                # 结构化提取
                parsed = {
                    'desc_raw': raw_sections.get('函数简介:', ''),
                    'signature': parse_signature(raw_sections.get('函数原型:', '')),
                    'parameters': parse_parameters(raw_sections.get('参数定义:', '')),
                    'returns': parse_return_values(raw_sections.get('返回值:', '')),
                    'examples': parse_examples(raw_sections.get('示例:', '')),
                    'notes': parse_notes(raw_sections.get('注:', '') or raw_sections.get('注意:', ''))
                }

                # 描述从 desc_raw 提取，但保持原始访问
                parsed['description'] = parsed['desc_raw']

                # 生成新格式
                new_content = generate_new_format(func_name, category, parsed)

                # 写回文件
                md_file.write_text(new_content, encoding='utf-8')
                stats['converted'] += 1

                # 构建索引条目
                info = build_function_info(func_name, category, parsed)
                all_functions.append(info)

            except Exception as e:
                print(f'  转换失败: {category}/{md_file.name} - {e}')
                stats['failed'] += 1

    # 生成函数索引
    index_path = root.parent / 'functions_index.json'
    index_data = {
        'total': len(all_functions),
        'categories': {},
        'functions': all_functions
    }

    # 按分类统计
    for func in all_functions:
        cat = func['category']
        if cat not in index_data['categories']:
            index_data['categories'][cat] = []
        index_data['categories'][cat].append(func['name'])

    # 排序每个分类的函数列表
    for cat in index_data['categories']:
        index_data['categories'][cat].sort()

    # 按名称排序所有函数
    all_functions.sort(key=lambda f: f['name'].lower())

    index_path.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    print(f'\n===== 转换完成 =====')
    print(f'转换: {stats["converted"]} 个文件')
    print(f'跳过: {stats["skipped"]} 个文件')
    print(f'失败: {stats["failed"]} 个文件')
    print(f'索引: {len(all_functions)} 个函数, {len(index_data["categories"])} 个分类')
    print(f'索引文件: {index_path}')

    return index_data


if __name__ == '__main__':
    import sys
    docs_root = 'references/dm_api_docs'
    force = '--force' in sys.argv
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            docs_root = arg
    script_dir = Path(__file__).parent.parent
    docs_path = script_dir / docs_root
    convert_all_docs(str(docs_path), force=force)
