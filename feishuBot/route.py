from fastapi import APIRouter, Request, Response, BackgroundTasks
import json
import importlib
router = APIRouter(
    responses={404: {"description": "Not found"}},
)
method_list = {}
@router.post("/")
def feishu_main(request:Request,background_task:BackgroundTasks):
    """
    The default route of feishu
    """
    data = request.state.origin_data
    #print(data)
    #Challenge
    if "challenge" in data:
         return {"challenge": data["challenge"]}
    if "schema" in data and data["schema"] == "2.0":
        event_type = data["header"]["event_type"]
        loader_class = "feishuBot.event."+event_type
        try:
            loader_mod = importlib.import_module(loader_class)
            if event_type not in method_list:
                method_list[event_type]=[]
            background_task.add_task(loader_mod.handle_event,method_list[event_type],data["event"])
        except:
            return Response("Not Support Event",status_code=200)
    else:
        return Response("Not Support Schema",status_code=400)
    return Response("200 OK",status_code=200)
