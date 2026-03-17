#!/usr/bin/env python3
import json, html, os
from datetime import datetime

ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT, 'data')
UPDATED = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')

CSS = """
:root{--bg:#020617;--card:#0f172a;--text:#e5eefc;--muted:#94a3b8;--line:#1e293b;--accent:#7dd3fc;--soft:#082f49;--good:#86efac}
*{box-sizing:border-box} html{font-size:18px} body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC","Noto Sans TC",sans-serif;line-height:1.72}
a{color:var(--accent);text-decoration:none} strong{font-weight:800}
.wrap{max-width:900px;margin:0 auto;padding:20px 14px 52px}.narrow{max-width:760px}
.card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:20px 18px;box-shadow:0 12px 32px rgba(0,0,0,.35);margin-bottom:14px}
.pill{display:inline-block;padding:6px 12px;border-radius:999px;background:var(--soft);color:var(--accent);font-weight:700;font-size:.95rem}.muted{color:var(--muted)}
h1,h2,h3{margin:0 0 10px;line-height:1.25} h1{font-size:1.8rem} h2{font-size:1.35rem} h3{font-size:1.06rem}
p{margin:.45em 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.topic-card{display:block;color:inherit}
.topic-card h3{color:var(--accent)} .list{margin:.5em 0 0 1.15em;padding:0} .list li+li{margin-top:8px}
.story{padding:14px 0;border-top:1px solid rgba(148,163,184,.18)} .story:first-of-type{border-top:0;padding-top:0}.story h3{margin-bottom:6px}
.kicker{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px}.source{font-size:.95rem;color:var(--muted)}
.nav{display:flex;gap:8px;flex-wrap:wrap}.nav a{padding:9px 12px;border:1px solid var(--line);border-radius:999px;background:rgba(125,211,252,.06)}
.small{font-size:.95rem}.stat{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.stat div{padding:12px;border:1px solid var(--line);border-radius:16px;background:rgba(125,211,252,.05)}.stat b{display:block;color:var(--accent)}
.footer{font-size:.95rem;color:var(--muted)}
@media (max-width:720px){html{font-size:17px}.wrap{padding:16px 12px 40px}.card{border-radius:18px;padding:16px 14px}.stat{grid-template-columns:repeat(2,minmax(0,1fr))}}
"""

TOPIC_META = {
    'ai': ('AI', '模型、產品、公司與監管動態。'),
    'storage-server': ('Storage / Server', '存儲、伺服器、企業基礎設施軟硬體與供應鏈。'),
    'cooling': ('Cooling', '資料中心液冷、熱管理與散熱供應鏈。'),
    'security': ('Security', '資安事故、漏洞通報、駭客行動與防禦技術。'),
    'startup': ('Startup', '新創融資、產品、合作、轉型與併購。'),
    'semiconductor': ('Semiconductor', '晶圓代工、記憶體、封裝、設備與 EDA 動態。'),
    'server-hardware-vendors': ('Server Hardware Vendors', '伺服器品牌 / OEM / ODM / 整機供應商動態。'),
    'big-tech': ('Big Tech', '大型科技公司策略、產品與監管動態。'),
    'geopolitics': ('Geopolitics', '地緣政治、制裁、供應鏈與國際局勢。'),
}
TOPIC_ORDER = ['ai','storage-server','cooling','security','startup','semiconductor','server-hardware-vendors','big-tech','geopolitics']


def ensure(path):
    os.makedirs(path, exist_ok=True)


def render_page(title, body, root='.'):
    extra_css = '.save-btn{appearance:none;border:1px solid rgba(125,211,252,.35);background:rgba(125,211,252,.08);color:var(--accent);border-radius:999px;padding:8px 12px;font:inherit;font-size:.92rem;font-weight:700;cursor:pointer;line-height:1.1}.save-btn[data-saved="true"]{background:rgba(134,239,172,.12);border-color:rgba(134,239,172,.45);color:var(--good)}.story-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:10px}.saved-meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.saved-tag,.saved-date{display:inline-block;padding:4px 10px;border:1px solid var(--line);border-radius:999px;font-size:.85rem;color:var(--muted);background:rgba(125,211,252,.05)}'
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{html.escape(title)}</title>
  <style>{CSS}{extra_css}</style>
</head>
<body>
  <main class="wrap">{body}</main>
  <script src="{root}/assets/saved.js"></script>
</body>
</html>'''


def rich(text):
    text = html.escape(text or '')
    return text.replace('**', '<strong>', 1).replace('**', '</strong>', 1) if text.count('**') >= 2 else text


def choose_latest_date():
    dates = []
    for name in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, name)
        if os.path.isdir(path):
            try:
                datetime.strptime(name, '%Y-%m-%d')
                dates.append(name)
            except ValueError:
                pass
    if not dates:
        raise SystemExit('No dated data directories found')
    return sorted(dates)[-1]


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_item(raw):
    title = raw.get('title') or raw.get('headline') or 'Untitled'
    summary = raw.get('summary') or raw.get('desc') or raw.get('description') or ''
    takeaway = raw.get('takeaway') or f'**{summary or title}**'
    source = raw.get('source') or raw.get('vendor') or raw.get('topic') or '來源待補'
    url = raw.get('url') or raw.get('link') or raw.get('sourceUrl') or '#'
    return {
        'title': title,
        'takeaway': takeaway,
        'summary': summary,
        'source': source,
        'url': url,
    }


def load_topics(date):
    topic_dir = os.path.join(DATA_DIR, date)
    found = []
    for slug in TOPIC_ORDER:
        path = os.path.join(topic_dir, f'{slug}.json')
        if not os.path.exists(path):
            continue
        raw = load_json(path)
        if isinstance(raw, dict):
            items = raw.get('items') or raw.get('news') or []
            name = raw.get('name') or raw.get('topic') or TOPIC_META.get(slug, (slug, ''))[0]
            desc = TOPIC_META.get(slug, (name, ''))[1]
        elif isinstance(raw, list):
            items = raw
            name = TOPIC_META.get(slug, (slug, ''))[0]
            desc = TOPIC_META.get(slug, (name, ''))[1]
        else:
            continue
        normalized = [normalize_item(x) for x in items if isinstance(x, dict)]
        if not normalized:
            continue
        if slug in TOPIC_META:
            name, meta_desc = TOPIC_META[slug]
            desc = desc or meta_desc
        found.append({'slug': slug, 'name': name, 'desc': desc, 'items': normalized})
    return found


def build_curated(date, topics):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    curated = {
        'site': {
            'name': '哈哈狗報',
            'date': date,
            'dateLabel': f'{date_obj.year} 年 {date_obj.month} 月 {date_obj.day} 日',
            'weekday': ['星期一','星期二','星期三','星期四','星期五','星期六','星期日'][date_obj.weekday()],
            'intro': f'今天整理 {len(topics)} 個主題，首頁、日期頁與主題頁入口已同步補齊。',
            'overview': [
                f'**今日已整理 {len(topics)} 個主題**：' + '、'.join(t['name'] for t in topics) + '。',
                '**首頁與日期頁已同步修正**：避免只剩單一主題導致入口缺失。',
                '**各主題頁保留原風格**：僅修正內容與站內連結同步。',
            ],
        },
        'topics': topics,
    }
    out = os.path.join(DATA_DIR, f'{date}-curated.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(curated, f, ensure_ascii=False, indent=2)
    return curated


def item_html(item):
    takeaway_html = rich(item['takeaway'])
    summary_text = (item.get('summary') or '').strip()
    takeaway_text = (item.get('takeaway') or '').replace('**', '').strip()
    summary_block = '' if (not summary_text or summary_text == takeaway_text) else f'\n      <p class="small">{html.escape(summary_text)}</p>'
    return f'''<article class="story">
      <h3>{html.escape(item['title'])}</h3>
      <p>{takeaway_html}</p>{summary_block}
      <p class="source">來源：<strong>{html.escape(item['source'])}</strong> · <a href="{html.escape(item['url'])}">原文連結</a></p>
    </article>'''


def stats_block(topic_count):
    return f'''<div class="stat small">
      <div><b>topics</b>{topic_count}</div>
      <div><b>style</b>kept</div>
      <div><b>links</b>synced</div>
      <div><b>updated</b>{UPDATED.split()[1]}</div>
      <div><b>status</b>published</div>
    </div>'''


def topic_nav(topics, prefix='.'):
    return '<div class="nav">' + ''.join(
        f'<a href="{prefix}/{t["slug"]}/">{html.escape(t["name"])} →</a>' for t in topics
    ) + '</div>'


def build_pages(curated):
    site = curated['site']
    date = site['date']
    date_label = site['dateLabel']
    topics = curated['topics']
    ensure(os.path.join(ROOT, date))

    sections = []
    for idx, t in enumerate(topics, 1):
        items = ''.join(item_html(i) for i in t['items'])
        sections.append(f'''<section class="card" id="{t['slug']}">
      <div class="kicker"><span class="pill">{idx}. {html.escape(t['name'])}</span><a class="small" href="./{t['slug']}/">看本主題頁 →</a></div>
      <p class="muted">{html.escape(t['desc'])}</p>
      {items}
    </section>''')

    daily = f'''
<section class="card">
  <div class="kicker"><span class="pill">哈哈狗報</span><a class="small" href="../">← 回首頁</a></div>
  <h1>{date_label}｜每日科技・產業・地緣新聞</h1>
  <p>{html.escape(site['intro'])}</p>
  <p class="muted">{site['weekday']} · 手機閱讀版</p>
</section>
<section class="card">
  <h2>快速導讀 / TL;DR</h2>
  <ul class="list">{''.join(f'<li>{rich(x)}</li>' for x in site['overview'])}</ul>
</section>
<section class="card">
  <h2>主題捷徑</h2>
  {topic_nav(topics, '.')}
</section>
{''.join(sections)}
<section class="card">
  <h2>任務資訊</h2>
  <p class="muted">更新時間：{UPDATED}</p>
  {stats_block(len(topics))}
</section>
<section class="footer">哈哈狗報 · /saved 保留給手動收藏，不做自動加入。</section>
'''
    with open(os.path.join(ROOT, date, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_page(f'哈哈狗報｜{date_label}', daily, '..'))

    for t in topics:
        ddir = os.path.join(ROOT, date, t['slug'])
        ensure(ddir)
        topic_body = f'''
    <section class="card">
      <div class="kicker"><span class="pill">{html.escape(t['name'])}</span><a class="small" href="../">← 回今日總覽</a><a class="small" href="../../">回首頁</a></div>
      <h1>{date_label}｜{html.escape(t['name'])}</h1>
      <p>{html.escape(t['desc'])}</p>
    </section>
    <section class="card">{''.join(item_html(i) for i in t['items'])}</section>
    <section class="card"><h2>任務資訊</h2><p class="muted">更新時間：{UPDATED}</p>{stats_block(len(topics))}</section>
    '''
        with open(os.path.join(ddir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(render_page(f'哈哈狗報｜{date_label}｜{t["name"]}', topic_body, '../..'))

        history = f'''
    <section class="card">
      <div class="kicker"><span class="pill"><a href="../">← 回首頁</a></span></div>
      <h1>{html.escape(t['name'])}</h1>
      <p>{html.escape(t['desc'])}</p>
      <p class="muted">主題歷史頁：目前保留最新一期與入口。</p>
    </section>
    <section class="card">
      <h2>最新一期</h2>
      <p><a href="../{date}/{t['slug']}/"><strong>{date_label}</strong> · {html.escape(t['name'])} 專頁 →</a></p>
      {''.join(item_html(i) for i in t['items'][:3])}
    </section>
    '''
        ensure(os.path.join(ROOT, t['slug']))
        with open(os.path.join(ROOT, t['slug'], 'index.html'), 'w', encoding='utf-8') as f:
            f.write(render_page(f'哈哈狗報｜{t["name"]}', history, '..'))

    cards = []
    for t in topics:
        first = t['items'][0]
        cards.append(f'''<a class="card topic-card" href="./{date}/{t['slug']}/"><h3>{html.escape(t['name'])}</h3><p>{rich(first['takeaway'])}</p><p class="muted small">最新：{html.escape(first['title'])}</p></a>''')

    topic_links = ' / '.join(f'<a href="./{t["slug"]}/">{html.escape(t["name"])}<\/a>' for t in topics)
    home = f'''
<section class="card">
  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap"><img src="./assets/husky-logo.png" alt="哈哈狗報 Logo" style="width:72px;height:72px;filter:drop-shadow(0 8px 18px rgba(125,211,252,.18))" /><div><div class="pill">哈哈狗報</div><h1>每日科技・產業・地緣情報整理</h1></div></div>
  <p>{html.escape(site['intro'])}</p>
  <p><a href="./{date}/"><strong>進入今日主頁：{date_label}</strong></a></p>
  <p class="muted">最新更新：{UPDATED}</p>
</section>
<section class="card">
  <h2>快速導讀 / TL;DR</h2>
  <ul class="list">{''.join(f'<li>{rich(x)}</li>' for x in site['overview'])}</ul>
</section>
<section class="card">
  <h2>今日主題</h2>
  <div class="grid">{''.join(cards)}</div>
</section>
<section class="card">
  <h2>站點導覽</h2>
  <ul class="list">
    <li><a href="./{date}/">今日總覽</a>：聚焦當日所有可閱讀主題。</li>
    <li>主題歷史頁：{topic_links}</li>
    <li><a href="./saved/">Saved</a> 僅保留手動收藏，不會自動加入。</li>
  </ul>
</section>
<section class="card">
  <h2>任務資訊</h2>
  {stats_block(len(topics))}
</section>
'''
    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_page('哈哈狗報', home))


def main():
    date = choose_latest_date()
    topics = load_topics(date)
    if not topics:
        raise SystemExit(f'No topic data found for {date}')
    curated = build_curated(date, topics)
    build_pages(curated)
    print(f'built {date} with {len(topics)} topics')


if __name__ == '__main__':
    main()
