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
from feishuBot.server import run_backend
import typing as t
class Bot:
    def __init__(self,app_id:str,app_secret:str,verification_token:str=None,encrypt_key:str=None,feishu_url:str="https://open.feishu.cn"):
        """
        Init the Feishu Bot
        """
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.feishu_url=feishu_url
        self._request = requestMaker(app_id,app_secret,feishu_url)
        self.hooklist = {}
        if verification_token is None:
            verification_token=""
        self.verification_token=verification_token
        if encrypt_key is None:
            encrypt_key = ""
        self.encrypt_key = encrypt_key


    def send_message_req(self,data:dict,receive_id_type:str="open_id",*args,**kwargs)->dict:
        """
        Make a Send Message Request
        """
        get_data = {
            "receive_id_type":receive_id_type
        }
        newtext = build_get_string(get_data)
        url = self.feishu_url + "/open-apis/im/v1/messages{newtext}".format(newtext=newtext)
        return self._request.make_request(url,data,*args,**kwargs)
    def send_message(self,chat_id:str,text:str,receive_id_type:str="open_id")->dict:
        """
        Send an message
        """
        data = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text":text}),
        }
        return self.send_message_req(data,receive_id_type=receive_id_type)

    def get_openid(self,phone:t.Union[None,str]=None,email:t.Union[None,str]=None)->list:
        """
        Get the openid of user by email
        """
        if type(phone) is str:
            phone = [phone]
        if type(email) is str:
            email = [email]
        data = {
            "emails": email,
            "mobiles": phone
        }
        url= self.feishu_url + "/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
        return self._request.make_request(url,data)["user_list"]

    def upload_image(self,image:bytes)->str:
        """
        Upload the image and get the image key
        """
        url = self.feishu_url + "/open-apis/im/v1/images"

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

    def send_image_by_id(self,chat_id:str,image_id:str,receive_id_type:str="open_id")->dict:
        """
        Send the image by image key
        """
        data = {
            "receive_id": chat_id,
            "msg_type": "image",
            "content": json.dumps({"image_key":image_id})
        }
        return self.send_message_req(data,receive_id_type=receive_id_type)
    
    def send_image(self,chat_id:str,image:bytes,receive_id_type:str="open_id")->dict:
        """
        Send image by upload it
        """
        image_id = self.upload_image(image)
        return self.send_image_by_id(chat_id,image_id,receive_id_type=receive_id_type)

    def get_image(self,image_key:str)->bytes:
        """
        Get the image
        """
        url = self.feishu_url + "/open-apis/im/v1/images/{image_key}"
        url = url.format(image_key=image_key)
        return self._request.get_content(url,{},method="GET")

    def get_message(self,message_id:str)->dict:
        """
        Get a message
        """
        url = self.feishu_url + "/open-apis/im/v1/messages/{message_id}"
        url = url.format(message_id=message_id)
        data = {}
        return self._request.make_request(url,data,method="GET")
    
    def get_message_read_users(self,message_id:str,user_id_type:str="open_id",page_size:int=50,page_token:t.Union[None,str]=None)->dict:
        """
        Get the readed users on a message
        """
        data = {
            "user_id_type":user_id_type,
            "page_size":page_size,
            "page_token":page_token
        }
        post_str = build_get_string(data)
        url = self.feishu_url + "/open-apis/im/v1/messages/{message_id}/read_users{post_str}"
        url = url.format(message_id=message_id,post_str=post_str)
        return self._request.make_request(url,data,method="GET")

    def get_history_message(self,chat_id:str,start_time:t.Union[None,str,int,float]=None,end_time:t.Union[None,str,int,float]=None,page_size:t.Union[None,int]=None,page_token:t.Union[None,str]=None)->dict:
        """
        Get history record on a chat
        """
        if type(start_time) is float:
            start_time=int(start_time)
        if type(start_time) is int:
            start_time=str(start_time)
        if type(end_time) is float:
            end_time=int(end_time)
        if type(end_time) is int:
            end_time=str(end_time)
        data = {
            "container_id_type":"chat",
            "container_id":chat_id,
            "start_time":start_time,
            "end_time":end_time,
            "page_size":page_size,
            "page_token":page_token
        }
        post_str = build_get_string(data)
        url = self.feishu_url + "/open-apis/im/v1/messages{post_str}"
        url = url.format(post_str=post_str)
        return self._request.make_request(url,data,method="GET")

    def upload_file(self,file:bytes,filename:str,filetype:str="stream")->str:
        """
        Upload a file and get the file id
        """
        url = self.feishu_url + "/open-apis/im/v1/images"

        data={
            'file_name': filename,
            'file_type': filetype
        }
        files={
            'file':file,
        }
        
        headers = {
        }
        response = self._request.make_request(url, data,headers=headers,files=files)
        return response["file_key"]

    def send_file_by_id(self,chat_id:str,file_id:str,receive_id_type:str="open_id",msg_type:str="file")->dict:
        """
        Send a file by file id
        """
        data = {
            "receive_id": chat_id,
            "content": json.dumps({"file_key":file_id}),
	        "msg_type": msg_type
        }
        return self.send_message_req(data,receive_id_type=receive_id_type)

    def send_file(self,chat_id:str,file:bytes,filename:str,filetype:str,receive_id_type:str="open_id",msg_type:str="file")->dict:
        """
        Send a file by upload it
        """
        file_id = self.upload_file(file,filename,filetype)
        return self.send_file_by_id(chat_id,file_id,receive_id_type=receive_id_type,msg_type=msg_type)

    def send_audio(self,chat_id:str,file:bytes,filename:str,filetype:str="mp3",receive_id_type:str="open_id")->dict:
        """
        Send an audio by upload it
        """
        return self.send_file(chat_id,file,filename,filetype,receive_id_type,msg_type="audio")
    
    def send_video(self,chat_id:str,file:bytes,filename:str,poster:str=None,filetype:str="mp4",receive_id_type:str="open_id")->dict:
        """
        Send an video by upload it
        """
        file_id = self.upload_file(file,filename,filetype)
        data = {
            "receive_id": chat_id,
            "content": "",
	        "msg_type": "media"
        }
        if poster is not None:
            poster_id = self.upload_image(poster)
            data["content"]=json.dumps({"file_key":file_id,"image_key":poster_id})
        else:
            data["content"]=json.dumps({"file_key":file_id})
        return self.send_message_req(data,receive_id_type=receive_id_type)
        

    def get_file(self,message_id:str,file_key:str,file_type:str="file")->bytes:
        """
        Get a file by file_key
        """
        data = {
            "type":file_type
        }
        post_str = build_get_string(data)
        url = self.feishu_url + "/open-apis/im/v1/messages/{message_id}/resources/{file_key}{post_str}"
        url = url.format(message_id=message_id,file_key=file_key,post_str=post_str)
        return self._request.get_content(url,data,method="GET")

    def reply_message(self,message_id:str,text:str)->dict:
        """
        Reply an message
        """
        data = {
            "msg_type": "text",
            "content": json.dumps({"text":text}),
        }
        url = self.feishu_url + "/open-apis/im/v1/messages/{message_id}/reply"
        url = url.format(message_id=message_id)
        return self._request.make_request(url,data)

    def delete_message(self,message_id:str)->None:
        """
        Delete(Recall) an message
        """
        url=self.feishu_url + "/open-apis/im/v1/messages/{message_id}"
        url = url.format(message_id=message_id)
        data = {}
        return self._request.make_request(url,data,method="DELETE")
    
    def runserver_background(self,bind:str="0.0.0.0",bind_port:int=80,is_sign:bool = False,is_encrypt:bool = False)->None:
        """
        Run the webhook server on the background
        """
        self.backend = run_backend(self.hooklist,is_encrypt,self.encrypt_key,is_sign,self.verification_token,bind,bind_port)
        self.backend.start()
        return

    def runserver(self,bind:str="0.0.0.0",bind_port:int=80,is_sign:bool = False,is_encrypt:bool = False):
        """
        Run the webhook server
        """
        self.runserver_background(bind,bind_port,is_sign,is_encrypt)
        self.backend.join()

    def register_handler(self, event_type: str,*args,**kwargs) -> t.Callable:
        """
        Register a webhook handler
        """
        def decorator(f: t.Callable) -> t.Callable:
            if event_type not in self.hooklist:
                self.hooklist[event_type]=[]
            self.hooklist[event_type].append((f,args,kwargs))
            return f
        return decorator