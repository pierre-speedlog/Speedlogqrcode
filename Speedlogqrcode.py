from fastapi import FastAPI, UploadFile, File
from pyzbar.pyzbar import decode
from PIL import Image
import io
import json
import requests

app = FastAPI()


@app.post("/recognize_qrcode")
async def recognize_qrcode(image: UploadFile = File(...)):
    """
    接收上传的图片文件，识别其中二维码信息的接口，返回格式尽量类似ChatGPT交互响应格式
    """
    try:
        # 读取上传的图片文件内容并转换为Image对象
        image_data = await image.read()
        image = Image.open(io.BytesIO(image_data))

        # 利用pyzbar库解码二维码
        decoded_objects = decode(image)

        results = []
        if decoded_objects:
            for obj in decoded_objects:
                result = {
                    "type": obj.type,
                    "data": obj.data.decode('utf-8')
                }
                results.append(result)

        # 构造类似ChatGPT交互的响应格式（简单示例）
        response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(results, indent=4) if results else "未识别到二维码内容",
                        "role": "assistant"
                    }
                }
            ]
        }

        return response
    except Exception as e:
        print(f"识别二维码出现错误: {str(e)}")
        return {
            "choices": [
                {
                    "message": {
                        "content": f"出现错误: {str(e)}",
                        "role": "assistant"
                    }
                }
            ]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
