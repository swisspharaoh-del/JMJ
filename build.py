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
    <span class="text-[10px] uppercase tracking-widest bg-[#fcfbf9] text-stone-600 px-2.5 py-1 rounded font-serif border border-stone-300 inline-block mb-3">{main_post["category"]}</span>
    <h2 class="font-serif text-4xl font-extrabold mt-2 mb-6 text-stone-900 leading-tight">{main_post["title"]}</h2>
    <div class="text-lg leading-relaxed text-stone-700 font-serif space-y-4">{main_post["body_html"]}</div>
    '''
    
    def gen_card(post, is_archive=False):
        # 使用 json.dumps 转义内容，彻底解决引号和换行符导致的 JS 语法错误
        title_json = json.dumps(post["title"])
        body_json = json.dumps(post["body_html"])
        
        text_size = "text-lg" if is_archive else "text-sm"
        padding = "border-b pb-6" if is_archive else "p-4 bg-[#fcfbf9] border border-stone-200 hover:border-stone-400 rounded-lg shadow-sm"
        
        return f'''<div class="cursor-pointer hover:bg-stone-50/50 {padding} transition-all duration-200 group" onclick="openArticle({title_json}, {body_json})">
                     <span class="text-[10px] uppercase tracking-widest bg-stone-100 px-2 py-0.5 text-stone-500 rounded border border-stone-200 mb-2 inline-block font-medium">{post["category"]}</span>
                     <h4 class="font-serif font-bold {text_size} text-stone-900 group-hover:text-stone-700 transition mb-2">{post["title"]}</h4>
                     <p class="text-xs text-stone-500 leading-relaxed line-clamp-3">{post["preview"]}</p>
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
