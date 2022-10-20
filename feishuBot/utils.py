import sys
import os
import hashlib
import base64
import json
from Crypto.Cipher import AES
if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))
def at(user_id,text):
    """
    build the text of @ someone
    """
    return """<at user_id="{user_id}">{text}</at>""".format(user_id=user_id,text=text)

def build_get_string(data):
    """
    Build the http param string
    """
    return_list = []
    for key in data:
        val = data[key]
        if val is None:
            continue
        add_str = key+"="+val
        return_list.append(add_str)
    return "?"+("&".join(return_list))

class  AESCipher(object):
    """
    The AES decrypt object by feishu official
    """
    def __init__(self, key):
        self.bs = AES.block_size
        self.key=hashlib.sha256(AESCipher.str_to_bytes(key)).digest()
    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return  self._unpad(cipher.decrypt(enc[AES.block_size:]))
    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return  self.decrypt(enc).decode('utf8')

def signature_check(timestamp,nonce,encrypt_key,body):
    """
    Check the signature
    """
    bytes_b1 = (timestamp + nonce + encrypt_key).encode('utf-8')
    bytes_b = bytes_b1 + body
    h = hashlib.sha256(bytes_b)
    signature = h.hexdigest()
    return signature

def get_message_text(message:dict)->str:
    """
    Get the message text from the message object
    """
    content = json.loads(message["message"]["content"])
    text = content["text"]
    return text
