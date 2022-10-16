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
from feishuBot.utils import build_get_string
class Bot:
    def __init__(self,app_id,app_secret,webhook_enable = False,bind="0.0.0.0",bind_port=80):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self._request = requestMaker(app_id,app_secret)
        self.hooklist = []
        self.webhook_enable = webhook_enable
        self.bind = bind
        self.bind_port = bind_port


    def send_message_req(self,data,*args,**kwargs):
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        return self._request.make_request(url,data,*args,**kwargs)
    def send_message(self,chat_id,text):
        data = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text":text}),
        }
        return self.send_message_req(data)

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
        return self.send_message_req(data)
    
    def send_image(self,chat_id,image):
        image_id = self.upload_image(image)
        return self.send_image_by_id(chat_id,image_id)

    def get_message(self,message_id):
        url = "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}"
        url = url.format(message_id=message_id)
        data = {}
        return self._request.make_request(url,data,method="GET")
    
    def get_message_read_users(self,message_id,user_id_type="open_id",page_size=50,page_token=None):
        data = {
            "user_id_type":user_id_type,
            "page_size":page_size,
            "page_token":page_token
        }
        post_str = build_get_string(data)
        url = "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/read_users{post_str}"
        url = url.format(message_id=message_id,post_str=post_str)
        return self._request.make_request(url,data,method="GET")

    def get_history_message(self,chat_id,start_time=None,end_time=None,page_size=None,page_token=None):
        data = {
            "container_id_type":"chat",
            "container_id":chat_id,
            "start_time":start_time,
            "end_time":end_time,
            "page_size":page_size,
            "page_token":page_token
        }
        post_str = build_get_string(data)
        url = "https://open.feishu.cn/open-apis/im/v1/messages{post_str}"
        url = url.format(post_str=post_str)
        return self._request.make_request(url,data,method="GET")

    def get_file(self,message_id,file_key,file_type="file"):
        data = {
            "type":file_type
        }
        post_str = build_get_string(data)
        url = "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}{post_str}"
        url = url.format(message_id=message_id,file_key=file_key,post_str=post_str)
        return self._request.get_content(url,data,method="GET")

    def reply_message(self,message_id,text):
        data = {
            "msg_type": "text",
            "content": json.dumps({"text":text}),
        }
        url = "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply"
        url = url.format(message_id=message_id)
        return self._request.make_request(url,data)

    def delete_message(self,message_id):
        url="https://open.feishu.cn/open-apis/im/v1/messages/{message_id}"
        url = url.format(message_id=message_id)
        data = {}
        return self._request.make_request(url,data,method="DELETE")
    