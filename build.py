import os
import re

def build():
    posts = []
    for filename in sorted(os.listdir('_posts'), reverse=True):
        if filename.endswith('.md'):
            with open(f'_posts/{filename}', 'r', encoding='utf-8') as f:
                content = f.read()
                title = re.search(r'title: "(.*?)"', content).group(1)
                body = re.sub(r'---[\s\S]*?---', '', content).strip()
                posts.append({'title': title, 'body': body})

    if not posts: return

    # 分配文章：第一篇主，之后交替放入左右和归档
    main_post = posts[0]
    side_posts = posts[1:]

    # 生成 HTML 代码片段
    main_html = f'<h2 class="text-4xl font-bold mb-6">{main_post["title"]}</h2><div class="text-lg leading-relaxed">{main_post["body"][:300]}...</div>'
    
    left_html = ""
    right_html = ""
    archive_html = ""

    for i, post in enumerate(side_posts):
        item = f'''<div class="cursor-pointer hover:bg-gray-50 p-2 transition" onclick="openArticle('{post["title"]}', '{post["body"].replace("'", "’")}')">
                     <h4 class="font-bold text-sm mb-1">{post["title"]}</h4>
                     <p class="text-xs text-gray-500">{post["body"][:40]}...</p>
                   </div>'''
        if i % 2 == 0: left_html += item
        else: right_html += item
        archive_html += item.replace('p-2', 'border-b pb-4').replace('text-sm', 'text-lg').replace('text-xs', 'text-sm')

    # 更新 index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = re.sub(r'<!-- BUILD_MARKER_MAIN_START -->[\s\S]*?<!-- BUILD_MARKER_MAIN_END -->', f'<!-- BUILD_MARKER_MAIN_START -->\n{main_html}\n<!-- BUILD_MARKER_MAIN_END -->', html)
    html = re.sub(r'<!-- BUILD_MARKER_LEFT_START -->[\s\S]*?<!-- BUILD_MARKER_LEFT_END -->', f'<!-- BUILD_MARKER_LEFT_START -->\n{left_html}\n<!-- BUILD_MARKER_LEFT_END -->', html)
    html = re.sub(r'<!-- BUILD_MARKER_RIGHT_START -->[\s\S]*?<!-- BUILD_MARKER_RIGHT_END -->', f'<!-- BUILD_MARKER_RIGHT_START -->\n{right_html}\n<!-- BUILD_MARKER_RIGHT_END -->', html)
    html = re.sub(r'<!-- BUILD_MARKER_ARCHIVE_START -->[\s\S]*?<!-- BUILD_MARKER_ARCHIVE_END -->', f'<!-- BUILD_MARKER_ARCHIVE_START -->\n{archive_html}\n<!-- BUILD_MARKER_ARCHIVE_END -->', html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("玉山日报 UI 更新完成！")

if __name__ == "__main__":
    build()
