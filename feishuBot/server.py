import imp
import threading
import fastapi
import uvicorn
from fastapi import FastAPI, Form , Header , Request , Response
from feishuBot import utils,route as fastapi_route
import json
import ctypes
import inspect

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)

def _stop_thread(thread):
    """终止-线程"""
    _async_raise(thread.ident, SystemExit)

class run_backend(threading.Thread):
    """
    The Feishu Webhook server backend, powered by FastAPI.
    """
    def __init__(self,method_list:dict,encrypt=False,encrypt_key=None,need_checksum=False,verfy_token=None,bind="0.0.0.0",bind_port=80):
        threading.Thread.__init__(self)
        self.encrypt = encrypt
        if encrypt_key is None:
            encrypt_key = ""
        self.encrypt_key = encrypt_key
        self.need_checksum = need_checksum
        if verfy_token is None:
            verfy_token = ""
        self.verfy_token = verfy_token
        self.fastapi = FastAPI()
        fastapi_route.method_list = method_list
        
        
        @self.fastapi.middleware("http")
        async def check_verifytoken(request: Request, call_next):
            try:
                org_data = request.state.origin_data
                token = org_data["header"]["token"]
            except:
                try:
                    
                    token = org_data["token"]
                except:
                    return Response("Verify Failed",status_code=400)
            if self.verfy_token != token:
                return Response("Verify Failed",status_code=400)
            response = await call_next(request)
            return response
        if need_checksum:
            @self.fastapi.middleware("http")
            async def checksum_message(request: Request, call_next):
                org_data = request.state.origin_data
                if not ("type" in org_data and org_data["type"] == "url_verification"):
                    try:
                        req_timestamp = request.headers["X-Lark-Request-Timestamp"]
                        req_nonce = request.headers["X-Lark-Request-Nonce"]
                        req_sign = request.headers["X-Lark-Signature"]
                        content = request.state.origin_data_raw
                        req_sign2 = utils.signature_check(req_timestamp,req_nonce,self.encrypt_key,content)
                        if req_sign != req_sign2:
                            return Response("Checksign Failed",status_code=400)
                    except:
                        return Response("Checksign Failed",status_code=400)
                response = await call_next(request)
                return response
        if encrypt:
            self.decrypter = utils.AESCipher(encrypt_key)
            @self.fastapi.middleware("http")
            async def decrypt_message(request: Request, call_next):
                try:
                    encrypted_data_raw = await request.body()
                    request.state.origin_data_raw = encrypted_data_raw
                    encrypted_data = json.loads(encrypted_data_raw)["encrypt"]
                    origin_data = self.decrypter.decrypt_string(encrypted_data)
                    if origin_data != "":
                        request.state.origin_data = json.loads(origin_data)
                except:
                    return Response("Decode Failed",status_code=400)
                response = await call_next(request)
                return response
        else:
            @self.fastapi.middleware("http")
            async def passthrough_message(request: Request, call_next):
                origin_data = await request.body()
                request.state.origin_data_raw = origin_data
                request.state.origin_data = json.loads(origin_data)
                response = await call_next(request)
                return response
        self.bind = bind
        self.bind_port = bind_port
        self.fastapi.include_router(fastapi_route.router)


    def run(self):
        uvicorn.run(self.fastapi,host=self.bind,port=self.bind_port)

    def stop(self):
        _stop_thread(self)

    