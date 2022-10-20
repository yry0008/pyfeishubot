import json
import re
def handle_event(event_list,event_data):
    for event in event_list:
        f = event[0]
        args = event[1]
        kwargs = event[2]
        for kwarg in kwargs:
            if type(kwargs[kwarg]) is str and kwarg != "regex":
                kwargs[kwarg] = [kwargs[kwarg]]
        if "chat_type" in kwargs and event_data["message"]["chat_type"] not in kwargs["chat_type"]:
            continue
        if "message_type" in kwargs and event_data["message"]["message_type"] not in kwargs["message_type"]:
            continue
        if "sender_type" in kwargs and event_data["sender"]["sender_type"] not in kwargs["sender_type"]:
            continue
        if "regex" in kwargs and event_data["message"]["message_type"]== "text":
            text_content = json.loads(event["message"]["content"])
            text = text_content["text"]
            if(re.match(kwargs["regex"],text) == None):
                continue
        f(event_data)
        return