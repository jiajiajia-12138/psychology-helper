from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# OpenAI 客户端配置
client = OpenAI(
    api_key="sk-feede42c3daf4f4897c8919eedb18999",  # <<< 这里换成你自己的
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
Model = "qwen-plus"

# 系统提示词
system_prompt = """
你是一个心理辅导助手，专门帮助留守儿童解决心理问题。你的任务是：
1. 倾听用户的情感表达。
2. 提供情感支持和建议。
3. 引导用户积极面对问题。
"""

# 首页，渲染聊天页面
@app.route('/')
def index():
    return render_template('index.html')

# 聊天接口
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    try:
        response = client.chat.completions.create(
            model=Model,
            messages=messages
        )
        reply = response.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
