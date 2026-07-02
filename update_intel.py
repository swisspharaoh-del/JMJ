import os
import google.generativeai as genai

# 配置 API
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro") # 使用 Pro 版本以获得更好的逻辑推理能力

def generate_intel_brief():
    # 这里加载你的复杂指令集
    with open("INTELLIGENCE_PROMPT.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
    print("正在构建情报简报，此过程需要数秒，请稍候...")
    
    # 调用 AI
    response = model.generate_content(system_prompt)
    
    # 自动生成的 HTML 包装
    intel_html = f"""
    <div class="intel-briefing">
        <h2 class="text-4xl font-black mb-6">今日全球战略情报简报</h2>
        <div class="prose max-w-none text-gray-800">
            {response.text}
        </div>
    </div>
    """
    
    # 更新 index.html 中的 ARTICLE 区域
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 替换 <!-- ARTICLE_START --> 和 <!-- ARTICLE_END --> 之间的内容
    import re
    pattern = r"<!-- ARTICLE_START -->(.*?)<!-- ARTICLE_END -->"
    new_content = re.sub(pattern, f"<!-- ARTICLE_START -->\n{intel_html}\n<!-- ARTICLE_END -->", content, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("情报简报已写入 index.html，请提交至 GitHub。")

if __name__ == "__main__":
    generate_intel_brief()