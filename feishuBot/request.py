import requests
import json
import uuid
import time
import os
import sys
if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))

class requestMaker:
    """
    The object of make request to feishu
    """
    def __init__(self,app_id:str,app_secret:str,feishu_url="https://open.feishu.cn"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.feishu_url = feishu_url
        self.get_new_tenant_access_token()
    def get_new_tenant_access_token(self)->dict:
        """
        Get the new tenant access token and expire time.
        """
        url = self.feishu_url + "/open-apis/auth/v3/tenant_access_token/internal"
        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })


        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        ret_data = response.json()
        if ret_data["code"] == 0:
            self.tenantTTL = time.time() + ret_data["expire"] - 30
            self.tenantToken = ret_data["tenant_access_token"]
            return ret_data
        else:
            raise ValueError
    
    def make_request(self,url,data,method="POST",*args,**kwargs):
        """
        Make a general Restful API Request to feishu
        """
        if time.time() > self.tenantTTL:
            self.get_new_tenant_access_token()
        if "headers" in kwargs:
            headers = kwargs["headers"]
            headers["Authorization"] = 'Bearer {token}'.format(token=self.tenantToken)
            del kwargs["headers"]
        else:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=self.tenantToken)
            }
        if "Content-Type" in headers and headers["Content-Type"] == 'application/json' and type(data) is not str:
            data = json.dumps(data)
        if len(data) == 0:
            data=None
        if data is not None and data != "":
            kwargs["data"]=data
        response = requests.request(method, url, headers=headers,*args,**kwargs)
        ret_data = response.json()
        if ret_data["code"] == 0:
            return ret_data["data"]
        else:
            raise ValueError
    
    def get_content(self,url,data,method="POST",*args,**kwargs):
        """
        Get a file from feishu
        """
        if time.time() > self.tenantTTL:
            self.get_new_tenant_access_token()
        if "headers" in kwargs:
            headers = kwargs["headers"]
            headers["Authorization"] = 'Bearer {token}'.format(token=self.tenantToken)
            del kwargs["headers"]
        else:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=self.tenantToken)
            }
        if "Content-Type" in headers and headers["Content-Type"] == 'application/json' and type(data) is not str:
            data = json.dumps(data)
        if len(data) == 0:
            data=None
        if data is not None and data != "":
            kwargs["data"]=data
        response = requests.request(method, url, headers=headers,*args,**kwargs)
        return response.content