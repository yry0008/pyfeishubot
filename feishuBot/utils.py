import sys
import os
if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))
def at(user_id,text):
    return """<at user_id="{user_id}">{text}</at>""".format(user_id=user_id,text=text)
