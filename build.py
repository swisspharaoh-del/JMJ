import os
import re
import json

def build():
    # 1. 确保 _posts 目录存在
    if not os.path.exists('_posts'):
        print("错误：找不到 _posts 文件夹。")
        return

    posts = []
    # 2. 读取并解析文章
    for filename in sorted(os.listdir('_posts'), reverse=True):
        if filename.endswith('.md'):
            with open(f'_posts/{filename}', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 优化正则，兼容有无引号的写法
                title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                category_match = re.search(r'category:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                
                title = title_match.group(1) if title_match else filename.replace('.md', '')
                category = category_match.group(1) if category_match else "未分类"
                
                # 去掉元数据后的正文
                body_raw = re.sub(r'---[\s\S]*?---', '', content).strip()
                # 换行转为 <br> 以便在 HTML 渲染
                body_html = body_raw.replace('\n', '<br>')
                
                posts.append({
                    'title': title, 
                    'category': category, 
                    'body_html': body_html,
                    'preview': body_raw[:60].replace('\n', ' ') + "..."
                })

    if not posts: 
        print("没有找到文章。")
        return

    # 3. 生成 HTML 内容
    main_post = posts[0]
    side_posts = posts[1:]

    main_html = f'''
    <span class="text-[10px] uppercase tracking-widest bg-black text-white px-2 py-1">{main_post["category"]}</span>
    <h2 class="text-4xl font-bold mt-2 mb-6">{main_post["title"]}</h2>
    <div class="text-lg leading-relaxed text-gray-700">{main_post["body_html"]}</div>
    '''
    
    def gen_card(post, is_archive=False):
        # 使用 json.dumps 转义内容，彻底解决引号和换行符导致的 JS 语法错误
        title_json = json.dumps(post["title"])
        body_json = json.dumps(post["body_html"])
        
        text_size = "text-lg" if is_archive else "text-sm"
        padding = "border-b pb-4" if is_archive else "p-2"
        
        return f'''<div class="cursor-pointer hover:bg-gray-50 {padding} transition" onclick="openArticle({title_json}, {body_json})">
                     <span class="text-[10px] uppercase tracking-widest bg-gray-100 px-1.5 py-0.5 text-gray-500 mb-1 inline-block">{post["category"]}</span>
                     <h4 class="font-bold {text_size} mb-1">{post["title"]}</h4>
                     <p class="text-xs text-gray-500">{post["preview"]}</p>
                   </div>'''

    left_html = ""
    right_html = ""
    archive_html = ""

    for i, post in enumerate(side_posts):
        item = gen_card(post)
        if i % 2 == 0: left_html += item
        else: right_html += item
        archive_html += gen_card(post, is_archive=True)

    # 4. 更新 index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        html = re.sub(r'<!-- BUILD_MARKER_MAIN_START -->[\s\S]*?<!-- BUILD_MARKER_MAIN_END -->', f'<!-- BUILD_MARKER_MAIN_START -->\n{main_html}\n<!-- BUILD_MARKER_MAIN_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_LEFT_START -->[\s\S]*?<!-- BUILD_MARKER_LEFT_END -->', f'<!-- BUILD_MARKER_LEFT_START -->\n{left_html}\n<!-- BUILD_MARKER_LEFT_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_RIGHT_START -->[\s\S]*?<!-- BUILD_MARKER_RIGHT_END -->', f'<!-- BUILD_MARKER_RIGHT_START -->\n{right_html}\n<!-- BUILD_MARKER_RIGHT_END -->', html)
        html = re.sub(r'<!-- BUILD_MARKER_ARCHIVE_START -->[\s\S]*?<!-- BUILD_MARKER_ARCHIVE_END -->', f'<!-- BUILD_MARKER_ARCHIVE_START -->\n{archive_html}\n<!-- BUILD_MARKER_ARCHIVE_END -->', html)

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("成功！UI 更新完成。")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    build()
