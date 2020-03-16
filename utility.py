# ! /usr/bin/env python3
# -*- coding:UTF-8 -*-
import os, sys
from threading import Thread

def lunch_video(pathfile):
    #obtener el nombre del fichero de video
    _video_name = os.path.basename(pathfile).split("_thumbs_")[0]
    _video = os.path.join(os.path.dirname(pathfile), './../',  _video_name)
    print('video ->', _video)
    if os.path.isfile(_video):
        thread = Thread(target=tarea, args=("ffplay " + "\"" + _video + "\"",))
        thread.daemon = True
        thread.start()

# @staticmethod
def tarea(args=None):
    if not args:
        return
    os.system(args)