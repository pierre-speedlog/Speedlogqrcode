from flask import Flask, request, jsonify
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import requests
import base64
import io

app = Flask(__name__)

# 配置你的ChatGPT API token（假设你需要将其用于后续处理）
CHATGPT_API_TOKEN = 'your_chatgpt_api_token'
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'  # 示例URL，根据实际情况调整

def decode_qrcode(image_bytes):
    # 将字节流转换为OpenCV图像
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    # 使用pyzbar解码二维码
    decoded_objects = decode(image)
    
    # 提取二维码中的数据
    if decoded_objects:
        decoded_data = decoded_objects[0].data.decode("utf-8")
        return decoded_data
    else:
        return None

def send_to_chatgpt(text):
    # 准备请求数据
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'text-davinci-003',  # 或其他模型
        'prompt': text,
        'max_tokens': 150,
        'n': 1,
        'stop': None,
        'temperature': 0.7,
    }
    
    # 发送请求到ChatGPT API
    response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
    return response.json()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # 读取文件内容
    image_bytes = file.read()
    
    # 解码二维码
    qrcode_text = decode_qrcode(image_bytes)
    if qrcode_text is None:
        return jsonify({"error": "Failed to decode QR code"}), 400
    
    # 可选：将二维码文本发送到ChatGPT
    # chatgpt_response = send_to_chatgpt(qrcode_text)
    
    # 返回二维码文本
    return jsonify({"qrcode_text": qrcode_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
