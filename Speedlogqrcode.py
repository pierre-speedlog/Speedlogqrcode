from flask import Flask, request
import requests
from pyzbar.pyzbar import decode
import cv2
import io
import numpy as np

app = Flask(__name__)


def read_qr_code_from_url(url):
    """
    从给定的网络路径读取图像并识别其中的二维码内容
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_bytes = io.BytesIO(response.content)
            image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), 1)
            decoded_objects = decode(image)
            if decoded_objects:
                return decoded_objects[0].data.decode('utf-8')
            return "未识别到二维码内容"
        return f"获取图像失败，状态码: {response.status_code}"
    except Exception as e:
        return f"出现错误: {str(e)}"


@app.route('/qr_code_recognition', methods=['POST'])
def qr_code_recognition():
    """
    接收POST请求，请求中应包含图片网络路径信息，返回二维码文本内容
    """
    data = request.get_json()
    if 'image_url' in data:
        image_url = data['image_url']
        result = read_qr_code_from_url(image_url)
        return {"text": result}
    return {"text": "请求数据中缺少image_url字段"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
    
