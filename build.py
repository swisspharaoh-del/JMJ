# -*- coding: utf-8 -*-
import os
import re
import json

def build():
    """
    玉山日报自动化数据注入引擎
    1. 扫描并保障 _posts 目录的存在
    2. 解析 Markdown 文件中的 YAML 头部信息与正文
    3. 将所有文献无损编译为标准的 JSON 数据库
    4. 将 JSON 数据库安全注入到 index.html 的特定插槽中
    """
    # 确保 _posts 目录存在，避免因无目录而报错
    if not os.path.exists('_posts'):
        print("提示：未找到 _posts 目录，正在为您创建...")
        os.makedirs('_posts')

    # 如果检测到 _posts 为空，自动生成一篇用于排版和 Mermaid 图表展示的指南文章
    if len(os.listdir('_posts')) == 0:
        with open('_posts/2026-07-03-markdown-chart-guide.md', 'w', encoding='utf-8') as f:
            f.write('''---
title: "图表与排版示范指南"
category: "文化"
---
# 欢迎查阅玉山日报高级排版指南

本系统已深度整合 **Marked.js** 与 **Mermaid.js**。您现在可以直接在 Markdown 文章中插入学术表格和动态流程图。

## 一、学术三线表示范

| 观测季度 | 核心资产流动性 | 信用违约率 | 杠杆健康评级 |
| :--- | :---: | :---: | :--- |
| **2026 Q1** | 极度充沛 | 0.12% | 🟢 AAA (稳健) |
| **2026 Q2** | 边际收紧 | 0.24% | 🟡 AA (中性) |
| **2026 Q3** | 主动防守 | 0.45% | 🔴 A- (谨慎) |

## 二、Mermaid 动态流向图示范

下面是系统自动为您渲染的资金流动生命周期图：

```mermaid
graph TD
    A[中央银行公开市场操作] -->|注入流动性| B[大型国有银行]
    B -->|同业拆借| C[中小商业银行]
    C -->|信贷投放| D[实体高新技术企业]
    D -->|创造社会价值与就业| E[玉山经济繁荣生态]
    C -->|抵押放贷| F[房地产及传统重资产]
    F -->|杠杆堆积| G{系统性风险评估}
    G -->|蓝灯安全| E
    G -->|红灯预警| H[主动降杠杆防御]
```

## 三、AI 伴读与字号调节

点击文章上方的 **"玉山雅音伴读"**，即可体验极高保真度的声音播报（在 Microsoft Edge 浏览器下效果尤佳）。您还可以随时通过 `A-` 和 `A+` 调节文章字号大小以获得最佳视力舒适度。
''')
        print("已自动在 _posts 目录下生成排版示范指南。")

    posts = []
    file_list = sorted(os.listdir('_posts'), reverse=True)
    post_id = 1
    
    for filename in file_list:
        if filename.endswith('.md'):
            filepath = os.path.join('_posts', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 默认元数据
                title = filename.replace('.md', '')
                category = "未分类"
                body = content
                
                # 正则解析兼容性更强的 YAML Front Matter 头部
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        yaml_content = parts[1]
                        body = parts[2].strip()
                        
                        # 匹配标题
                        title_match = re.search(r'title:\s*["\']?(.*?)["\']?\s*$', yaml_content, re.MULTILINE)
                        if title_match:
                            title = title_match.group(1).strip()
                            
                        # 匹配分类
                        category_match = re.search(r'category:\s*["\']?(.*?)["\']?\s*$', yaml_content, re.MULTILINE)
                        if category_match:
                            category = category_match.group(1).strip()
                
                # 将处理好的文章元数据和正文存入列表
                posts.append({
                    "id": post_id,
                    "title": title,
                    "category": category,
                    "body": body
                })
                post_id += 1

    # 检查主页面模板是否存在
    if not os.path.exists('index.html'):
        print("错误：未找到 index.html 主模板文件！")
        return

    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 将 Python 列表转为符合标准 JSON 格式的格式化字符串，确保无中文字符转义冲突
    json_data_str = json.dumps(posts, ensure_ascii=False, indent=2)

    # 使用正则定位，将编译出的 JSON 完美推入 index.html 的数据库插槽中
    pattern = r'/\* BUILD_MARKER_DATA_START \*/[\s\S]*?/\* BUILD_MARKER_DATA_END \*/'
    replacement = f'/* BUILD_MARKER_DATA_START */\n{json_data_str}\n/* BUILD_MARKER_DATA_END */'

    updated_html = re.sub(pattern, replacement, html_content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"编译成功！已成功将 {len(posts)} 篇文献编译并安全注入到 index.html 数据仓储中。")

if __name__ == "__main__":
    build()
