from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    # 检查请求是否为 JSON 格式
    if request.is_json:
        # 获取 JSON 数据
        data = request.get_json()
        # 检查是否包含所需的键（例如 'text'）
        if 'text' in data:
            received_text = data['text']
            # print(f"接收到的文字内容: {received_text}")
            # 可以添加更多的业务逻辑，例如将文本存储到数据库，进行文本分析等
            return jsonify(received_text)      
        else:
            return jsonify({"error": "请求中未包含 'text' 字段"}), 400
    else:
        # 检查请求是否为表单格式
        if 'text' in request.form:
            received_text = request.form['text']
            print(f"接收到的文字内容: {received_text}")
        else:
            return jsonify({"error": "请求中未包含 'text' 字段"}), 400

    # 假设你还想接收文件，例如图片文件
    if 'image' in request.files:
        image_file = request.files['image']
        # 确保文件名安全
        filename = os.path.join('uploads', image_file.filename)
        # 保存文件
        image_file.save(filename)
        print(f"接收到的图片文件: {filename}")
        # 你可以在此添加对图片的进一步处理，例如使用 PIL 库对图片进行操作
        # from PIL import Image
        # img = Image.open(filename)
        # img.show()
    else:
        print("未接收到图片文件")

    # 响应请求
    return jsonify({"message": "Webhook 接收成功"}), 200


if __name__ == "__main__":
    # 创建 'uploads' 目录，如果不存在
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    # 启动应用程序，监听在 5000 端口
    app.run(host='0.0.0.0', port=5005)
