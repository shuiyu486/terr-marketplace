"""验证转换后的文档质量"""
import re
from pathlib import Path

root = Path(r'C:\AI\m_projects\m_agents\terr-marketplace\plugins\dm-api\references\dm_api_docs')

issues = []

for category_dir in sorted(root.iterdir()):
    if not category_dir.is_dir():
        continue

    for md_file in category_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        func_name = md_file.stem

        # 检查是否有 "此函数无参数" 但签名中有参数
        sig_match = re.search(r'\*\*签名:\*\*\s*`\s*\w+\s+\w+\(([^)]*)\)', content)
        has_no_params = '此函数无参数' in content

        if sig_match and has_no_params:
            params_str = sig_match.group(1).strip()
            if params_str:  # 签名中有参数但显示无参数
                issues.append(f'[参数遗漏] {category_dir.name}/{func_name}: 签名有参数但标记为无参数')
                continue

        # 检查签名中参数数量 vs 表格中参数数量
        if sig_match:
            params_str = sig_match.group(1).strip()
            sig_param_count = len([p for p in params_str.split(',') if p.strip()]) if params_str else 0

            # 计算表格中的参数行
            table_rows = re.findall(r'\| (\w+) \| \w+\*? \| .+ \|', content)
            table_count = len(table_rows)

            if sig_param_count > 0 and table_count == 0 and not has_no_params:
                issues.append(f'[参数缺失] {category_dir.name}/{func_name}: 签名{sig_param_count}个参数, 表格{table_count}个')
            elif sig_param_count > 0 and table_count < sig_param_count * 0.5:
                issues.append(f'[参数偏少] {category_dir.name}/{func_name}: 签名{sig_param_count}个参数, 表格{table_count}个')

        # 检查是否有空的返回值
        if '## 返回值' in content:
            ret_section = content.split('## 返回值')[1].split('##')[0] if '## 示例' in content.split('## 返回值')[1] else content.split('## 返回值')[1]
            if '*无返回值说明*' in ret_section and sig_match:
                issues.append(f'[返回值空] {category_dir.name}/{func_name}: 标记为无返回值说明')

        # 检查是否有损坏的表格行
        broken_table = re.findall(r'^\| .+ \|$', content, re.MULTILINE)
        if broken_table:
            for line in broken_table:
                if line.count('|') < 3:
                    issues.append(f'[表格损坏] {category_dir.name}/{func_name}: {line[:60]}')

if issues:
    print(f'发现 {len(issues)} 个问题:')
    for issue in issues:
        print(f'  {issue}')
else:
    print('所有文件验证通过!')

# 统计
total = sum(1 for d in root.iterdir() if d.is_dir() for f in d.glob('*.md'))
print(f'\n总计: {total} 个文件')
