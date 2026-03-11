#!/usr/bin/env python3
import json, html, os
from datetime import datetime

ROOT = os.path.dirname(__file__)
DATA = json.load(open(os.path.join(ROOT, 'data', '2026-03-10-curated.json')))
DATE = DATA['site']['date']
DATE_LABEL = DATA['site']['dateLabel']
TOPICS = DATA['topics']
UPDATED = '2026-03-10 21:40 America/Los_Angeles'
STATS = {
    'total': '約 18k',
    'input': '約 14k',
    'output': '約 4k',
    'duration': 'AI Tavily 重整',
    'status': 'published'
}
TOPIC_ORDER = [t['slug'] for t in TOPICS]

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

def topic_nav(prefix='.'):
    parts=[]
    for t in TOPICS:
        parts.append(f'<a href="{prefix}/{t["slug"]}/">{html.escape(t["name"])} →</a>')
    return '<div class="nav">' + ''.join(parts) + '</div>'

def rich(text):
    text = html.escape(text)
    return text.replace('**', '<strong>', 1).replace('**', '</strong>', 1) if text.count('**') >= 2 else text

def item_html(item):
    return f'''<article class="story">
      <h3>{html.escape(item['title'])}</h3>
      <p>{rich(item['takeaway'])}</p>
      <p class="small">{html.escape(item['summary'])}</p>
      <p class="source">來源：<strong>{html.escape(item['source'])}</strong> · <a href="{html.escape(item['url'])}">原文連結</a></p>
    </article>'''

def stats_block():
    return f'''<div class="stat small">
      <div><b>total token</b>{STATS['total']}</div>
      <div><b>input token</b>{STATS['input']}</div>
      <div><b>output token</b>{STATS['output']}</div>
      <div><b>duration</b>{STATS['duration']}</div>
      <div><b>status</b>{STATS['status']}</div>
    </div>'''

# daily page
ensure(os.path.join(ROOT, DATE))
sections=[]
for idx,t in enumerate(TOPICS,1):
    items=''.join(item_html(i) for i in t['items'])
    sections.append(f'''<section class="card" id="{t['slug']}">
      <div class="kicker"><span class="pill">{idx}. {html.escape(t['name'])}</span><a class="small" href="./{t['slug']}/">看本主題頁 →</a></div>
      <p class="muted">{html.escape(t['desc'])}</p>
      {items}
    </section>''')

daily = f'''
<section class="card">
  <div class="kicker"><span class="pill">哈哈狗報</span><a class="small" href="../">← 回首頁</a></div>
  <h1>{DATE_LABEL}｜每日科技・產業・地緣新聞</h1>
  <p>{html.escape(DATA['site']['intro'])}</p>
  <p class="muted">{DATA['site']['weekday']} · 固定八大主題 · 手機閱讀版</p>
</section>
<section class="card">
  <h2>快速導讀 / TL;DR</h2>
  <ul class="list">{''.join(f'<li>{rich(x)}</li>' for x in DATA['site']['overview'])}</ul>
</section>
<section class="card">
  <h2>主題捷徑</h2>
  {topic_nav('.')}
</section>
{''.join(sections)}
<section class="card">
  <h2>任務資訊</h2>
  <p class="muted">更新時間：{UPDATED}</p>
  {stats_block()}
</section>
<section class="footer">{DATA['site']['name']} · /saved 保留給手動收藏，不做自動加入。</section>
'''
open(os.path.join(ROOT, DATE, 'index.html'),'w').write(render_page(f"哈哈狗報｜{DATE_LABEL}", daily, '..'))

# topic daily pages + history pages
for t in TOPICS:
    ddir=os.path.join(ROOT, DATE, t['slug']); ensure(ddir)
    body=f'''
    <section class="card">
      <div class="kicker"><span class="pill">{html.escape(t['name'])}</span><a class="small" href="../">← 回今日總覽</a><a class="small" href="../../">回首頁</a></div>
      <h1>{DATE_LABEL}｜{html.escape(t['name'])}</h1>
      <p>{html.escape(t['desc'])}</p>
    </section>
    <section class="card">{''.join(item_html(i) for i in t['items'])}</section>
    <section class="card"><h2>任務資訊</h2><p class="muted">更新時間：{UPDATED}</p>{stats_block()}</section>
    '''
    open(os.path.join(ddir,'index.html'),'w').write(render_page(f"哈哈狗報｜{DATE_LABEL}｜{t['name']}", body, '../..'))

    history=f'''
    <section class="card">
      <div class="kicker"><span class="pill"><a href="../">← 回首頁</a></span></div>
      <h1>{html.escape(t['name'])}</h1>
      <p>{html.escape(t['desc'])}</p>
      <p class="muted">主題歷史頁：目前先保留最新一期與入口，後續會持續累積。</p>
    </section>
    <section class="card">
      <h2>最新一期</h2>
      <p><a href="../{DATE}/{t['slug']}/"><strong>{DATE_LABEL}</strong> · {html.escape(t['name'])} 專頁 →</a></p>
      {''.join(item_html(i) for i in t['items'][:3])}
    </section>
    '''
    open(os.path.join(ROOT,t['slug'],'index.html'),'w').write(render_page(f"哈哈狗報｜{t['name']}", history, '..'))

# homepage
cards=[]
for t in TOPICS:
    first=t['items'][0]
    cards.append(f'''<a class="card topic-card" href="./{DATE}/{t['slug']}/"><h3>{html.escape(t['name'])}</h3><p>{rich(first['takeaway'])}</p><p class="muted small">最新：{html.escape(first['title'])}</p></a>''')

home=f'''
<section class="card">
  <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap"><img src="./assets/husky-logo.png" alt="哈哈狗報 Logo" style="width:72px;height:72px;filter:drop-shadow(0 8px 18px rgba(125,211,252,.18))" /><div><div class="pill">哈哈狗報</div><h1>每日科技・產業・地緣情報整理</h1></div></div>
  <p>{html.escape(DATA['site']['intro'])}</p>
  <p><a href="./{DATE}/"><strong>進入今日主頁：{DATE_LABEL}</strong></a></p>
  <p class="muted">最新更新：{UPDATED}</p>
</section>
<section class="card">
  <h2>快速導讀 / TL;DR</h2>
  <ul class="list">{''.join(f'<li>{rich(x)}</li>' for x in DATA['site']['overview'])}</ul>
</section>
<section class="card">
  <h2>今日八大主題</h2>
  <div class="grid">{''.join(cards)}</div>
</section>
<section class="card">
  <h2>站點導覽</h2>
  <ul class="list">
    <li><a href="./{DATE}/">今日總覽</a>：固定八大主題、每則精簡摘要。</li>
    <li>主題歷史頁：<a href="./ai/">AI</a> / <a href="./big-tech/">Big Tech</a> / <a href="./semiconductor/">Semiconductor</a> / <a href="./storage-server/">Storage / Server</a> / <a href="./cooling/">Cooling</a> / <a href="./security/">Security</a> / <a href="./startup/">Startup</a> / <a href="./geopolitics/">Geopolitics</a></li>
    <li><a href="./saved/">Saved</a> 僅保留手動收藏，不會自動加入。</li>
  </ul>
</section>
<section class="card">
  <h2>任務資訊</h2>
  {stats_block()}
</section>
'''
open(os.path.join(ROOT,'index.html'),'w').write(render_page('哈哈狗報', home))
print('built')
