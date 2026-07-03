import os
import re

def build():
    # 1. 确保 _posts 目录存在
    if not os.path.exists('_posts'):
        print("错误：找不到 _posts 文件夹，请创建它并放入 markdown 文件。")
        return

    posts = []
    # 2. 读取文章
    for filename in sorted(os.listdir('_posts'), reverse=True):
        if filename.endswith('.md'):
            with open(f'_posts/{filename}', 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取标题，如果找不到则用文件名代替
                title_match = re.search(r'title: "(.*?)"', content)
                title = title_match.group(1) if title_match else filename.replace('.md', '')
                # 去掉元数据后的正文
                body = re.sub(r'---[\s\S]*?---', '', content).strip()
                posts.append({'title': title, 'body': body})

    if not posts: 
        print("没有找到文章，请确认 _posts 文件夹里是否有 .md 文件。")
        return

    # 3. 生成内容
    main_post = posts[0]
    side_posts = posts[1:]

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

    # 4. 更新 index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        # 检查标记是否存在
        if '<!-- BUILD_MARKER_MAIN_START -->' not in html:
            print("错误：index.html 中缺少构建标记，请检查 HTML 模板。")
            return

        html = re.sub(r'<!-- BUILD_MARKER_MAIN_START -->[\s\S]*?<!-- BUILD_MARKER_MAIN_END -->', f'<!-- BUILD_MARKER_MAIN_START -->\n{main_html}\n<!-- BUILD_MARKER_MAIN_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_LEFT_START -->[\s\S]*?<!-- BUILD_MARKER_LEFT_END -->', f'<!-- BUILD_MARKER_LEFT_START -->\n{left_html}\n<!-- BUILD_MARKER_LEFT_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_RIGHT_START -->[\s\S]*?<!-- BUILD_MARKER_RIGHT_END -->', f'<!-- BUILD_MARKER_RIGHT_START -->\n{right_html}\n<!-- BUILD_MARKER_RIGHT_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_ARCHIVE_START -->[\s\S]*?<!-- BUILD_MARKER_ARCHIVE_END -->', f'<!-- BUILD_MARKER_ARCHIVE_START -->\n{archive_html}\n<!-- BUILD_MARKER_ARCHIVE_END -->', html)

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("成功！玉山日报 UI 更新完成。")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    build()
