import os
import sys
import json
if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))
from feishuBot.request import requestMaker
class Bot:
    def __init__(self,app_id,app_secret,webhook_enable = False,bind="0.0.0.0",bind_port=80):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self._request = requestMaker(app_id,app_secret)
        self.hooklist = []
        self.webhook_enable = webhook_enable
        self.bind = bind
        self.bind_port = bind_port



    
    def send_message(self,chat_id,text):
        data = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text":text}),
        }
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        return self._request.make_request(url,data)

    def get_openid(self,phone=None,email=None):
        if type(phone) is str:
            phone = [phone]
        if type(email) is str:
            email = [email]
        data = {
            "emails": email,
            "mobiles": phone
        }
        url="https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
        return self._request.make_request(url,data)["user_list"]

    def upload_image(self,image):
        url = "https://open.feishu.cn/open-apis/im/v1/images"

        data={
            'image_type': 'message'
        }
        files={
            'image':image,
        }
        
        headers = {
        }
        response = self._request.make_request(url, data,headers=headers,files=files)
        return response["image_key"]

    def send_image_by_id(self,chat_id,image_id):
        data = {
            "receive_id": chat_id,
            "msg_type": "image",
            "content": json.dumps({"image_key":image_id},)
        }
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        return self._request.make_request(url,data)
    
    def send_image(self,chat_id,image):
        image_id = self.upload_image(image)
        return self.send_image_by_id(chat_id,image_id)

