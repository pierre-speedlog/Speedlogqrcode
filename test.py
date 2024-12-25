from flask import Flask, request, jsonify
from PIL import Image
from pyzbar.pyzbar import decode
import io

app = Flask(__name__)


@app.route('/qrcode/read', methods=['POST'])
def read_qrcode():
    # 检查请求中是否包含文件
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 将上传的文件字节流转换为图片对象
        image = Image.open(io.BytesIO(file.read()))
        # 对图片进行二维码解码
        decoded_objects = decode(image)
        if decoded_objects:
            # 如果识别出二维码，提取并返回文本内容
            text = decoded_objects[0].data.decode('utf-8')
            return jsonify({"result": text})
        return jsonify({"error": "No QR code found in the image"}), 404
    except Exception as e:
        # 若出现异常，返回包含错误信息的响应
        return jsonify({"error": f"Error processing the image: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
