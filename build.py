import os
import re
import urllib.parse
from datetime import datetime

base_dir = os.path.expanduser('~/Desktop/homepage')
posts_dir = os.path.join(base_dir, 'archive/posts')
out_posts_dir = os.path.join(base_dir, 'posts')
os.makedirs(out_posts_dir, exist_ok=True)

article_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 通俗解释</title>
  <style>
    :root {{
      --bg: #F2F0E9;
      --card-bg: #FAF9F5;
      --text: #1a1a1a;
      --text-muted: #666666;
      --text-light: #8c8c8c;
      --border: #eae6df;
      --border-dark: #d5cfc4;
      --accent: #111111;
      --max-width: 720px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.8;
      padding: 50px 24px 100px;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{
      max-width: var(--max-width);
      margin: 0 auto;
    }}
    nav {{
      margin-bottom: 36px;
      display: flex;
      gap: 16px;
      font-size: 0.95rem;
    }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      border-bottom: 1px dotted var(--text-muted);
      padding-bottom: 2px;
    }}
    nav a:hover {{
      color: var(--text);
      border-bottom-color: var(--text);
    }}
    header {{
      margin-bottom: 36px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.4;
      margin-bottom: 12px;
    }}
    .meta {{
      font-size: 0.9rem;
      color: var(--text-light);
    }}
    .content {{
      font-size: 1.05rem;
      line-height: 1.85;
      color: var(--text);
    }}
    .content p {{
      margin-bottom: 1.6em;
    }}
    .content h2, .content h3, .content h4 {{
      margin-top: 2em;
      margin-bottom: 0.8em;
      line-height: 1.4;
      font-weight: 700;
    }}
    .content img {{
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      margin: 1.8em 0;
      display: block;
      border: 1px solid var(--border);
    }}
    .content figure {{
      margin: 1.8em 0;
    }}
    .content blockquote {{
      border-left: 3px solid var(--border-dark);
      padding: 10px 18px;
      margin: 1.6em 0;
      background: var(--card-bg);
      color: var(--text-muted);
    }}
    .content ul, .content ol {{
      margin: 1em 0 1.6em 24px;
      color: var(--text-muted);
    }}
    .content li {{
      margin-bottom: 0.5em;
    }}
    footer {{
      margin-top: 80px;
      padding-top: 28px;
      border-top: 1px solid var(--border);
      text-align: left;
      font-size: 0.85rem;
      color: var(--text-light);
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav>
      <a href="../index.html">← 返回首页</a>
      <a href="../articles.html">全部文章归档</a>
    </nav>
    <header>
      <h1>{title}</h1>
      <div class="meta">发布日期：{date} · 通俗解释</div>
    </header>
    <article class="content">
      {content}
    </article>
    <footer>
      <p>&copy; 2026 通俗解释. 保留所有权利。</p>
    </footer>
  </div>
</body>
</html>
"""

articles_index_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文章归档 | 通俗解释</title>
  <style>
    :root {{
      --bg: #F2F0E9;
      --card-bg: #FAF9F5;
      --text: #1a1a1a;
      --text-muted: #666666;
      --text-light: #8c8c8c;
      --border: #eae6df;
      --border-dark: #d5cfc4;
      --accent: #111111;
      --max-width: 720px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.75;
      padding: 50px 24px 100px;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{ max-width: var(--max-width); margin: 0 auto; }}
    nav {{ margin-bottom: 36px; }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      border-bottom: 1px dotted var(--text-muted);
      padding-bottom: 2px;
      font-size: 0.95rem;
    }}
    nav a:hover {{ color: var(--text); border-bottom-color: var(--text); }}
    header {{ margin-bottom: 48px; }}
    h1 {{ font-size: 1.85rem; font-weight: 700; margin-bottom: 10px; }}
    .subtitle {{ color: var(--text-muted); font-size: 1rem; }}
    .post-list {{ display: flex; flex-direction: column; }}
    .post-card {{
      padding: 18px 0;
      border-bottom: 1px solid var(--border);
      text-decoration: none;
      color: inherit;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 16px;
    }}
    .post-card:last-child {{ border-bottom: none; }}
    .post-card:hover .post-title {{ text-decoration: underline; }}
    .post-title {{ font-size: 1.05rem; font-weight: 600; color: var(--text); }}
    .post-date {{ font-size: 0.85rem; color: var(--text-light); white-space: nowrap; }}
    footer {{
      margin-top: 80px;
      text-align: left;
      font-size: 0.85rem;
      color: var(--text-light);
      border-top: 1px solid var(--border);
      padding-top: 28px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav><a href="index.html">← 返回首页</a></nav>
    <header>
      <h1>文章归档</h1>
      <p class="subtitle">历史发表的科技科普、机制拆解与行业动态。</p>
    </header>
    <div class="post-list">
      {post_items_html}
    </div>
    <footer>
      <p>&copy; 2026 通俗解释. 保留所有权利。</p>
    </footer>
  </div>
</body>
</html>
"""

posts_data = []

for filename in os.listdir(posts_dir):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(posts_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract title and date
    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename[:-3]
    
    date_match = re.search(r'\*\*发布日期\*\*:\s*([^\n]+)', text)
    date_str = date_match.group(1).strip() if date_match else ''
    
    # Split content after ---
    parts = text.split('---', 1)
    raw_content = parts[1].strip() if len(parts) > 1 else text
    
    # Replace image URLs
    def repl_img(m):
        full_url = m.group(0)
        parsed = urllib.parse.urlsplit(full_url)
        name = os.path.basename(urllib.parse.unquote(parsed.path))
        return f"../images/{name}"
    
    clean_content = re.sub(r'https?://tongsujieshi\.com/wp-content/uploads/[^\s"\'<>)]+', repl_img, raw_content)
    clean_content = re.sub(r'<!--\s*/?wp:[^>]*-->', '', clean_content)
    
    slug = re.sub(r'[\\/*?:\":<>|\s]', '-', title)[:50].strip('-')
    out_html = os.path.join(out_posts_dir, f'{slug}.html')
    
    page_html = article_template.format(
        title=title,
        date=date_str[:10],
        content=clean_content
    )
    
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(page_html)
        
    posts_data.append({
        'title': title,
        'date': date_str[:10] or '2024-10-01',
        'slug': f'{slug}.html'
    })

posts_data.sort(key=lambda x: x['date'], reverse=True)

post_items_html = ""
for p in posts_data:
    post_items_html += f"""      <a href="posts/{p['slug']}" class="post-card">
        <span class="post-title">{p['title']}</span>
        <span class="post-date">{p['date']}</span>
      </a>\n"""

with open(os.path.join(base_dir, 'articles.html'), 'w', encoding='utf-8') as f:
    f.write(articles_index_template.format(post_items_html=post_items_html))

print(f"Generated {len(posts_data)} article pages and articles.html successfully.")
