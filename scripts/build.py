"""Build the public static handbook; upload only _site to GitHub Pages."""
from pathlib import Path
import html
import re
import shutil

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'
SELECTED = [1, 2, 4, 16, 18, 19, 20, 22, 23, 30, 36, 37, 38, 42, 43, 50, 62, 71, 82, 103]


def render(source: str, count: int) -> str:
    body = markdown.markdown(source, extensions=['tables', 'fenced_code', 'toc'])
    soup = BeautifulSoup(body, 'html.parser')
    navigation = []
    for heading in soup.find_all(['h2', 'h3']):
        title = heading.get_text(' ', strip=True)
        match = re.match(r'Q(\d+)', title)
        if match:
            heading['id'] = 'q' + str(int(match.group(1)))
        navigation.append(
            f'<a class="{"q" if match else "section"}" href="#{html.escape(heading["id"])}">'
            f'{html.escape(title)}</a>'
        )
    title = soup.h1.get_text(' ', strip=True)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="广东移动省数智化部系统开发岗位面试准备，包含120道问题与临场20题。">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="data:,">
</head>
<body>
<header><div><strong>广东移动 · 系统开发</strong> <span>个人面试准备 / {count}题 / 2026.10.20</span></div>
<nav aria-label="版本切换"><a href="quick.html">临场20题</a><a href="index.html">完整120题</a></nav></header>
<div class="layout"><aside aria-label="题目目录"><strong>题目导航</strong><p>Ctrl＋F 可全文查找</p>{''.join(navigation)}</aside>
<main>{soup}<div class="foot">基于岗位官网、公开面经与个人材料整理。做过的经历与假设方案分开表达，具体面试安排以本次通知为准。<br>个人学习资料，与中国移动及其下属单位无官方关联。</div></main></div>
</body></html>'''


def validate_site() -> None:
    for filename, expected in [('index.html', 120), ('quick.html', 20)]:
        document = (OUT / filename).read_text(encoding='utf-8')
        soup = BeautifulSoup(document, 'html.parser')
        questions = soup.find_all('h3')
        assert len(questions) == expected, f'{filename}: question count mismatch'
        ids = [item['id'] for item in soup.find_all(id=True)]
        assert len(ids) == len(set(ids)), f'{filename}: duplicate anchors'
        assert not re.search(r'(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|file://|127\.0\.0\.1|localhost)', document), 'Local path leaked'
        assert not re.search(r'(?:\bgh[pousr]_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+)', document), 'Credential-shaped string'
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#'):
                assert href[1:] in ids, f'{filename}: broken anchor {href}'
            elif not href.startswith(('https://', 'http://', 'mailto:')):
                target, _, fragment = href.partition('#')
                target_path = OUT / target
                assert target_path.is_file(), f'{filename}: missing {target}'
                if fragment:
                    other = BeautifulSoup(target_path.read_text(encoding='utf-8'), 'html.parser')
                    assert other.find(id=fragment), f'{filename}: missing fragment {fragment}'
        for stylesheet in soup.select('link[rel="stylesheet"]'):
            assert (OUT / stylesheet['href']).is_file(), 'Missing stylesheet'
    print('Validated 120 full questions, 20 quick questions, anchors, site links, and publication boundaries.')


def main() -> None:
    source = (ROOT / 'content/handbook.md').read_text(encoding='utf-8')
    numbers = [int(n) for n in re.findall(r'^### Q(\d+)', source, flags=re.M)]
    assert numbers == list(range(1, 121)), 'Questions must be numbered Q01 through Q120'
    questions = {}
    for section in re.split(r'(?=^### Q\d+)', source, flags=re.M)[1:]:
        number = int(re.match(r'### Q(\d+)', section).group(1))
        questions[number] = re.split(r'^## ', section, maxsplit=1, flags=re.M)[0].strip()
    quick = '''# 广东移动系统开发｜临场先看20题

靳驭哲专用｜2026-10-20｜目标：省数智化部—系统开发，广州天河。

这20题从完整120题中挑出，按“开场→AI编码→项目→工程基本功→反问”排列。先记每题的意思，再用自己的话说。通知只说明云来斯堡酒店现场面试，不能确定具体轮数。

事实提醒：硕士正式专业是大数据人工智能，预计2027年7月毕业；中海实习已于2026年9月15日结束；光储6.85%属于离线回放；企业Agent是团队原型之后的个人重构；当前Offer、空档期安排、调剂与薪资要按真实情况说。

原题号保留，便于找追问。出处、事实核对与其他100题见[完整120题](index.html)。

'''
    quick += '\n\n'.join(questions[n] for n in SELECTED)
    (OUT / 'assets').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'assets/site.css', OUT / 'assets/site.css')
    (OUT / 'index.html').write_text(render(source, 120), encoding='utf-8')
    (OUT / 'quick.html').write_text(render(quick, 20), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
    validate_site()


if __name__ == '__main__':
    main()
