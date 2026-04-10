#!/usr/bin/env python3
"""
合并6个Agent的调研结果，生成Phase 1.5调研Review检查点的摘要表格。
扫描 references/research/ 目录下的01-06 md文件，统计每个维度的来源数量、
一手/二手占比、关键发现。

用法:
    python3 merge_research.py <工作目录路径>

示例:
    python3 merge_research.py output/rag-book
"""

import sys
import re
from pathlib import Path

AGENTS = {
    '01-foundations': '基础',
    '02-architecture': '架构',
    '03-ecosystem': '生态',
    '04-applications': '应用',
    '05-challenges': '挑战',
    '06-trends': '趋势',
}


def count_sources(content: str) -> "dict":
    """统计来源数量和一手/二手占比"""
    urls = re.findall(r'https?://[^\s\)\]>]+', content)

    primary_markers = len(re.findall(
        r'一���|primary|官方|论文|源码|原始|标准|规范|RFC|arxiv|官方文档',
        content, re.IGNORECASE
    ))
    secondary_markers = len(re.findall(
        r'二手|secondary|转述|博客|教程|评论|总结|科普',
        content, re.IGNORECASE
    ))

    return {
        'url_count': len(urls),
        'unique_urls': len(set(urls)),
        'primary_markers': primary_markers,
        'secondary_markers': secondary_markers,
    }


def extract_key_findings(content: str, max_items: int = 3) -> "list[str]":
    """提取关键发现（取前几个二级标题或加粗项）"""
    headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    if headings:
        return headings[:max_items]

    bolds = re.findall(r'\*\*(.+?)\*\*', content)
    if bolds:
        return bolds[:max_items]

    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
    return [l[:50] + '...' if len(l) > 50 else l for l in lines[:max_items]]


def find_debates(files: "dict[str, str]") -> "list[str]":
    """检测跨文件争议点"""
    debates = []
    for name, content in files.items():
        matches = re.findall(
            r'(?:争议|分歧|批评|质疑|不同观点|反对|局限|但是|然而).{0,100}',
            content
        )
        for m in matches:
            debates.append(f"{AGENTS.get(name, name)}: {m[:80]}")
    return debates[:5]


def main():
    if len(sys.argv) < 2:
        print("用法: python3 merge_research.py <工作目录路径>")
        sys.exit(1)

    work_dir = Path(sys.argv[1])
    research_dir = work_dir / 'references' / 'research'

    if not research_dir.exists():
        print(f"❌ 目录不存在: {research_dir}")
        sys.exit(1)

    files = {}
    rows = []
    total_sources = 0
    total_primary = 0
    total_secondary = 0
    missing = []

    for key, label in AGENTS.items():
        md_file = research_dir / f"{key}.md"
        if not md_file.exists():
            missing.append(label)
            rows.append(f"│ {label:<12} │ {'❌ 缺失':<8} │ {'—':<24} │")
            continue

        content = md_file.read_text(encoding='utf-8')
        files[key] = content
        stats = count_sources(content)
        findings = extract_key_findings(content)

        total_sources += stats['unique_urls']
        total_primary += stats['primary_markers']
        total_secondary += stats['secondary_markers']

        findings_str = ', '.join(findings) if findings else '—'
        if len(findings_str) > 40:
            findings_str = findings_str[:37] + '...'

        rows.append(f"│ {label:<12} │ {stats['unique_urls']:<8} │ {findings_str:<24} │")

    debates = find_debates(files)

    print("┌──────────────┬──────────┬──────────────────────────┐")
    print("│ Agent        │ 来源数量  │ 关键发现                  │")
    print("├──────────────┼──────────┼──────────────────────────┤")
    for row in rows:
        print(row)
    print("├──────────────┼──────────┼──────────────────────────┤")

    primary_ratio = f"{total_primary}/{total_primary + total_secondary}" if (total_primary + total_secondary) > 0 else "未标记"
    print(f"│ 总来源数      │ {total_sources:<8} │ 一手占比: {primary_ratio:<15} │")

    if debates:
        print(f"│ 争议点        │ {len(debates)}处      │ {debates[0][:24]:<24} │")
    else:
        print(f"│ 争议点        │ 0处      │ {'—':<24} │")

    if missing:
        print(f"│ 信息不足维度   │ {len(missing)}个      │ {', '.join(missing):<24} │")
    else:
        print(f"│ 信息不足维度   │ 无       │ {'—':<24} │")

    print("└──────────────┴──��───────┴──────────────────────────┘")

    if total_sources < 15:
        print("\n⚠️ 总来源数 <15，建议降低期望或补充调研")
    if missing:
        print(f"\n⚠️ 缺失维度: {', '.join(missing)}，建议补充调研或在书籍前言中标注")


if __name__ == '__main__':
    main()
