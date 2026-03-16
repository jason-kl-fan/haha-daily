import json
import os
from datetime import datetime

def generate_page(title, items, output_path):
    items_html = ""
    for item in items:
        items_html += f"""
        <div class="item">
            <h2 class="title">{item['title']}</h2>
            <p class="takeaway"><strong>重點：</strong>{item['takeaway']}</p>
            <p class="summary">{item['summary']}</p>
            <p class="source">來源：<a href="{item['sourceUrl']}">{item['source']}</a></p>
        </div>
        <hr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; color: #333; }}
            h1 {{ color: #1a73e8; }}
            .item {{ margin-bottom: 30px; }}
            .title {{ font-size: 1.25rem; color: #000; margin-bottom: 10px; }}
            .takeaway {{ color: #d93025; font-weight: bold; }}
            .summary {{ color: #5f6368; }}
            .source {{ font-size: 0.8rem; color: #9aa0a6; }}
            a {{ color: #1a73e8; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p>更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <div class="content">
            {items_html}
        </div>
        <footer>
            <p><a href="/">返回首頁</a></p>
        </footer>
    </body>
    </html>
    """
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

# Load data
date_str = "2026-03-16"
data_file = f'data/{date_str}/semiconductor.json'
if os.path.exists(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update paths
    generate_page(f"哈哈狗報 - 半導體 ({date_str})", data['items'], f"{date_str}/semiconductor/index.html")
    generate_page(f"哈哈狗報 ({date_str})", data['items'], f"{date_str}/index.html")
    generate_page("哈哈狗報 - 半導體 (最新)", data['items'], "semiconductor/index.html")
    generate_page("哈哈狗報 (最新)", data['items'], "index.html")
