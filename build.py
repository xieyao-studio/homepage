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
  <title>{title} | XY · 通俗解释</title>
  <style>
    :root {{
      --bg: #fafafa;
      --surface: #ffffff;
      --text-main: #111827;
      --text-muted: #6b7280;
      --border: #e5e7eb;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --tag-bg: #f3f4f6;
      --tag-text: #374151;
      --max-w: 740px;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0f172a;
        --surface: #1e293b;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border: #334155;
        --accent: #38bdf8;
        --accent-hover: #7dd3fc;
        --tag-bg: #334155;
        --tag-text: #e2e8f0;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.8;
      padding: 40px 20px 80px;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{
      max-width: var(--max-w);
      margin: 0 auto;
    }}
    nav {{
      margin-bottom: 32px;
      display: flex;
      gap: 16px;
      font-size: 0.95rem;
    }}
    nav a {{
      color: var(--accent);
      text-decoration: none;
      font-weight: 500;
    }}
    nav a:hover {{ text-decoration: underline; }}
    header {{
      margin-bottom: 32px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.35;
      margin-bottom: 12px;
    }}
    .meta {{
      font-size: 0.9rem;
      color: var(--text-muted);
    }}
    .content {{
      font-size: 1.05rem;
      line-height: 1.85;
    }}
    .content p {{
      margin-bottom: 1.5em;
    }}
    .content h2, .content h3, .content h4 {{
      margin-top: 1.8em;
      margin-bottom: 0.8em;
      line-height: 1.4;
    }}
    .content img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      margin: 1.5em 0;
      display: block;
      border: 1px solid var(--border);
    }}
    .content figure {{
      margin: 1.5em 0;
    }}
    .content blockquote {{
      border-left: 4px solid var(--accent);
      padding: 8px 16px;
      margin: 1.5em 0;
      background: var(--surface);
      border-radius: 0 8px 8px 0;
      color: var(--text-muted);
    }}
    .content ul, .content ol {{
      margin: 1em 0 1.5em 24px;
    }}
    .content li {{
      margin-bottom: 0.5em;
    }}
    footer {{
      margin-top: 64px;
      padding-top: 24px;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav>
      <a href="../index.html">← 返回首页</a>
      <a href="../articles.html">全部文章</a>
    </nav>
    <header>
      <h1>{title}</h1>
      <div class="meta">发布日期：{date} · XY · 通俗解释</div>
    </header>
    <article class="content">
      {content}
    </article>
    <footer>
      <p>&copy; 2026 XY · 通俗解释 · 保留所有权利</p>
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
  <title>文章归档 | XY · 通俗解释</title>
  <style>
    :root {{
      --bg: #fafafa;
      --surface: #ffffff;
      --text-main: #111827;
      --text-muted: #6b7280;
      --border: #e5e7eb;
      --accent: #2563eb;
      --tag-bg: #f3f4f6;
      --tag-text: #374151;
      --radius: 12px;
      --max-w: 800px;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #0f172a;
        --surface: #1e293b;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border: #334155;
        --accent: #38bdf8;
        --tag-bg: #334155;
        --tag-text: #e2e8f0;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      padding: 40px 20px 80px;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{ max-width: var(--max-w); margin: 0 auto; }}
    nav {{ margin-bottom: 32px; }}
    nav a {{ color: var(--accent); text-decoration: none; font-weight: 500; }}
    nav a:hover {{ text-decoration: underline; }}
    header {{ margin-bottom: 40px; }}
    h1 {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 8px; }}
    .subtitle {{ color: var(--text-muted); font-size: 1.05rem; }}
    .post-list {{ display: flex; flex-direction: column; gap: 14px; }}
    .post-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px 22px;
      text-decoration: none;
      color: inherit;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }}
    .post-card:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
    }}
    .post-title {{ font-size: 1.05rem; font-weight: 600; color: var(--text-main); }}
    .post-date {{ font-size: 0.85rem; color: var(--text-muted); white-space: nowrap; margin-left: 16px; }}
    footer {{
      margin-top: 64px;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      padding-top: 24px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav><a href="index.html">← 返回首页</a></nav>
    <header>
      <h1>文章归档</h1>
      <p class="subtitle">历史发表的科技深度科普、产业机制拆解与行业动态。</p>
    </header>
    <div class="post-list">
      {post_items_html}
    </div>
    <footer>
      <p>&copy; 2026 XY · 通俗解释 · 保留所有权利</p>
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
    # Match https://tongsujieshi.com/wp-content/uploads/.../filename.ext
    def repl_img(m):
        full_url = m.group(0)
        parsed = urllib.parse.urlsplit(full_url)
        name = os.path.basename(urllib.parse.unquote(parsed.path))
        return f"../images/{name}"
    
    clean_content = re.sub(r'https?://tongsujieshi\.com/wp-content/uploads/[^\s"\'<>)]+', repl_img, raw_content)
    # Also strip leftover WP block comments like <!-- wp:... -->
    clean_content = re.sub(r'<!--\s*/?wp:[^>]*-->', '', clean_content)
    
    # Build slug
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

# Sort posts by date descending
posts_data.sort(key=lambda x: x['date'], reverse=True)

# Generate articles.html
post_items_html = ""
for p in posts_data:
    post_items_html += f"""      <a href="posts/{p['slug']}" class="post-card">
        <span class="post-title">{p['title']}</span>
        <span class="post-date">{p['date']}</span>
      </a>\n"""

with open(os.path.join(base_dir, 'articles.html'), 'w', encoding='utf-8') as f:
    f.write(articles_index_template.format(post_items_html=post_items_html))

print(f"Generated {len(posts_data)} article pages and articles.html successfully.")
