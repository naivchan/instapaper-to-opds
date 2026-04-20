import os
import subprocess
import re
from instapaper import Instapaper

# Credentials from Environment
KEY = os.environ.get('INSTAPAPER_KEY')
SECRET = os.environ.get('INSTAPAPER_SECRET')
EMAIL = os.environ.get('INSTAPAPER_EMAIL')
PASS = os.environ.get('INSTAPAPER_PASSWORD')

def get_safe_filename(title):
    """Generates a consistent filename from the article title."""
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
    return f"{safe_title}.epub"

def main():
    print("Connecting to Instapaper Parser API...", flush=True)
    i = Instapaper(KEY, SECRET)
    i.login(EMAIL, PASS)

    bookmarks = i.bookmarks()
    print(f"Found {len(bookmarks)} articles in Unread.", flush=True)

    if not os.path.exists('/library'):
        os.makedirs('/library')

    # --- TRACK UNREAD ARTICLES ---
    unread_filenames = set()
    for bm in bookmarks:
        unread_filenames.add(get_safe_filename(bm.title))

    # --- CLEANUP PHASE ---
    print("Syncing local library with Instapaper...", flush=True)
    local_files = [f for f in os.listdir('/library') if f.endswith('.epub')]

    for local_file in local_files:
        if local_file not in unread_filenames:
            print(f"  [-] Removing archived/deleted: {local_file}", flush=True)
            os.remove(os.path.join('/library', local_file))

    # --- DOWNLOAD PHASE ---
    for bm in bookmarks:
        filename = get_safe_filename(bm.title)
        epub_path = os.path.join('/library', filename)
        temp_html = f"/tmp/{bm.bookmark_id}.html"

        if os.path.exists(epub_path):
            continue

        print(f"Processing: {bm.title}...", flush=True)

        try:
            article_content = bm.text
            if not article_content:
                continue

            # 1. Spacing Fix: Only fix broken line breaks, don't wrap in <p>
            # This converts double-breaks to paragraph markers without destroying <h1> or <div>
            cleaned = re.sub(r'(<br\s*/?>\s*){2,}', '</p><p>', article_content)
            
            # 2. Structure Fix: Wrap in a full HTML skeleton with a div
            # Using a div allows block elements (h1, p, ul) to live inside it
            final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{bm.title}</title>
</head>
<body>
    <div class="article-body">
        {cleaned}
    </div>
</body>
</html>
"""

            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(final_html)

            # 3. Pandoc Conversion
            subprocess.run([
                "pandoc", temp_html,
                "-f", "html",
                "-t", "epub",
                "-o", epub_path,
                "--css", "style.css",
                "--variable", "indent=false",
                "--metadata", f"title={bm.title}",
                "--standalone"
            ], check=True)

            print(f"  [✓] Success: {filename}", flush=True)

            if os.path.exists(temp_html):
                os.remove(temp_html)

        except Exception as e:
            print(f"  [✗] Error processing {bm.title}: {e}", flush=True)

if __name__ == "__main__":
    main()
