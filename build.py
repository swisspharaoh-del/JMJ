import os
import re
import json
import html

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
                
                # 正则匹配，兼容有无引号的写法
                title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                category_match = re.search(r'category:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                
                title = title_match.group(1).strip() if title_match else filename.replace('.md', '')
                category = category_match.group(1).strip() if category_match else "未分类"
                
                # 去掉元数据后的正文 (使用 split 确保只去掉最开头的 front matter 块，防止破坏正文中的水平线)
                body_raw = content
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        body_raw = parts[2].strip()
                
                # 换行转为 <br> 以便在 HTML 模态框中完整还原换行格式
                body_html = body_raw.replace('\n', '<br>')
                
                posts.append({
                    'title': title, 
                    'category': category, 
                    'body_html': body_html,
                    'preview': body_raw[:85].replace('\n', ' ') + "..."
                })

    if not posts: 
        print("没有找到文章。")
        return

    # 3. 三栏横向分配：中主头条(1篇) + 左右分栏(多篇)
    main_post = posts[0]
    side_posts = posts[1:]

    # 对主头条的数据进行 JSON 序列化和 HTML 实体转义，防止引号冲突，使其完美支持点击阅读
    main_title_escaped = html.escape(json.dumps(main_post["title"]))
    main_body_escaped = html.escape(json.dumps(main_post["body_html"]))

    main_html = f'''
    <span class="text-[10px] uppercase tracking-widest bg-stone-100 text-stone-600 px-2.5 py-1 rounded font-serif border border-stone-300 inline-block mb-3">{main_post["category"]}</span>
    <h2 class="font-serif text-4xl font-extrabold mt-2 mb-6 text-stone-900 leading-tight cursor-pointer hover:text-stone-700 transition" onclick="openArticle({main_title_escaped}, {main_body_escaped})">{main_post["title"]}</h2>
    <div class="text-lg leading-relaxed text-stone-700 font-serif space-y-4 cursor-pointer" onclick="openArticle({main_title_escaped}, {main_body_escaped})">{main_post["body_html"]}</div>
    '''
    
    def gen_card(post, is_archive=False):
        # 核心修复：对属性内的参数运行 html.escape，彻底阻断双引号破环属性引号的行为
        title_escaped = html.escape(json.dumps(post["title"]))
        body_escaped = html.escape(json.dumps(post["body_html"]))
        
        # 往期文章采用带有下划线隔开的优雅布局，卡片文章采用纯净的传统单栏分割线(border-b)
        if is_archive:
            padding = "border-b border-stone-200 pb-6 mb-2"
            text_size = "text-lg"
        else:
            padding = "border-b border-stone-200 pb-5 mb-5 last:border-b-0 last:pb-0"
            text_size = "text-sm"
        
        return f'''<div class="cursor-pointer hover:bg-stone-50/50 {padding} transition-all duration-200 group" onclick="openArticle({title_escaped}, {body_escaped})">
                     <span class="text-[9px] uppercase tracking-widest bg-stone-100 px-2 py-0.5 text-stone-500 rounded border border-stone-200 mb-2 inline-block font-medium">{post["category"]}</span>
                     <h4 class="font-serif font-bold {text_size} text-stone-900 group-hover:text-stone-700 transition mb-2">{post["title"]}</h4>
                     <p class="text-xs text-stone-500 leading-relaxed line-clamp-3 font-serif">{post["preview"]}</p>
                   </div>'''

    left_html = ""
    right_html = ""
    archive_html = ""

    # 精确轮询分发，保证左右栏的文章比例呈现完美的视觉对称
    for i, post in enumerate(side_posts):
        item = gen_card(post)
        if i % 2 == 0: left_html += item
        else: right_html += item
        archive_html += gen_card(post, is_archive=True)

    # 4. 精准写入更新 HTML
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        html_content = re.sub(r'<!-- BUILD_MARKER_MAIN_START -->[\s\S]*?<!-- BUILD_MARKER_MAIN_END -->', f'<!-- BUILD_MARKER_MAIN_START -->\n{main_html}\n<!-- BUILD_MARKER_MAIN_END -->', html_content)
        html_content = re.sub(r'<!-- BUILD_MARKER_LEFT_START -->[\s\S]*?<!-- BUILD_MARKER_LEFT_END -->', f'<!-- BUILD_MARKER_LEFT_START -->\n{left_html}\n<!-- BUILD_MARKER_LEFT_END -->', html_content)
        html_content = re.sub(r'<!-- BUILD_MARKER_RIGHT_START -->[\s\S]*?<!-- BUILD_MARKER_RIGHT_END -->', f'<!-- BUILD_MARKER_RIGHT_START -->\n{right_html}\n<!-- BUILD_MARKER_RIGHT_END -->', html_content)
        html_content = re.sub(r'<!-- BUILD_MARKER_ARCHIVE_START -->[\s\S]*?<!-- BUILD_MARKER_ARCHIVE_END -->', f'<!-- BUILD_MARKER_ARCHIVE_START -->\n{archive_html}\n<!-- BUILD_MARKER_ARCHIVE_END -->', html_content)

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("成功！玉山日报 UI 更新完成。")
    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    build()
