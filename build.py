# -*- coding: utf-8 -*-
import os
import re
import json

def build():
    """
    玉山日报自动化数据注入引擎 (JSON 驱动版)
    """
    # 确保 _posts 目录存在
    if not os.path.exists('_posts'):
        print("提示：未找到 _posts 目录，正在为您创建...")
        os.makedirs('_posts')

    posts = []
    file_list = sorted(os.listdir('_posts'), reverse=True)
    post_id = 1
    
    for filename in file_list:
        if filename.endswith('.md'):
            filepath = os.path.join('_posts', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                title = filename.replace('.md', '')
                category = "未分类"
                body = content
                
                # 兼容性 YAML 解析
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        yaml_content = parts[1]
                        body = parts[2].strip()
                        
                        title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', yaml_content, re.MULTILINE)
                        if title_match:
                            title = title_match.group(1).strip()
                            
                        category_match = re.search(r'category:\s*["\']?(.*?)["\']?\s*$', yaml_content, re.MULTILINE)
                        if category_match:
                            category = category_match.group(1).strip()
                
                posts.append({
                    "id": post_id,
                    "title": title,
                    "category": category,
                    "body": body
                })
                post_id += 1

    if not os.path.exists('index.html'):
        print("错误：未找到 index.html 主模板文件！")
        return

    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 无转义 JSON 封装
    json_data_str = json.dumps(posts, ensure_ascii=False, indent=2)

    # 运用安全 Lambda 纯字面量匹配，将 JSON 完美注入至前端插槽
    pattern = r'/\* BUILD_MARKER_DATA_START \*/[\s\S]*?/\* BUILD_MARKER_DATA_END \*/'
    replacement = f'/* BUILD_MARKER_DATA_START */\n        const RAW_POSTS = {json_data_str};\n        /* BUILD_MARKER_DATA_END */'

    updated_html = re.sub(pattern, lambda m: replacement, html_content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"云端编译成功！已完美加载并渲染了 {len(posts)} 篇文献。")

if __name__ == "__main__":
    build()

