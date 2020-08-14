import os, sys
from boxes import Box
import pyglet
import json
import subprocess
import threading


class BuildBox:

    def __init__(self, source):
        # get types in Box.
        self.box = Box()
        if os.path.exists(source):
            self.source = os.path.abspath(source)    
            # info video.
            self.box.video['source'] = self.source
            self.box.video['name'] = self.source.split("\\")[-1]
            self._sourceVideo()
            # info imagen
            self._make_image_source()
        else:
            self.box.video['source'] = 'unknown'
            self.box.video['name'] = 'unknown'

    def _make_image_source(self):
        basename = os.path.dirname(self.source)
        name = self.box.video['name'] + '_thumbs_0000.gif'
        self.box.image['name'] = name
        source = os.path.join(basename, 'Thumbails', name)
        base_source = os.path.abspath(source)
        if os.path.exists(base_source):
            self.box.image['source'] = base_source
            self._define_image(base_source)
        else:
            self.box.image['source'] = 'unknown'

    def _define_image(self, source):
        # Importing Required Library
        from PIL import Image
        try:
            # Opening Image as an object
            with Image.open(self.box.image['source']) as Img:
                # Getting the format of image
                self.box.image['format'] = Img.format
                # Getting the mode of image
                self.box.image['mode'] = Img.mode
                # Getting the size of image
                self.box.image['size'] = Img.size
                # Getting only the width of image
                self.box.image['width'] = Img.width
                # Getting only the height of image
                self.box.image['height'] = Img.height
                # Getting the info about image
                #self.box.image['info'] = Img.info
                # Getting the color palette of image
                #self.box.image['palette'] = str(Img.palette).decode('utf8')
        # Closing Image object
        except Exception as e:
            print('Exception load imagen', str(e.args))

        self.box.image['hash'] = self.hashfile(self.box.image['source'])

    def _print_ffmpeg_info(self):
        from pyglet.media import have_ffmpeg

        if have_ffmpeg():
            from pyglet.media.codecs import ffmpeg
            print('Using FFmpeg version {0}'.format(ffmpeg.get_version()))
        else:
            print('FFmpeg not available; required for media decoding.')
            print('https://www.ffmpeg.org/download.html\n')

    def _sourceVideo(self):
        self._print_ffmpeg_info()
        try:
            print(self.source.split('\\')[-1])
            source = pyglet.media.load(self.source, streaming=True)
            self._source_info(source)
        except Exception: #pyglet.media.MediaException:
            print('Could not open %s' % self.source)

    def _source_info(self, source):
        if source.video_format:
            vf = source.video_format
            if vf.frame_rate:
                self.box.video['rate'] = '%.02f' % vf.frame_rate
            else:
                self.box.video['rate'] = 'unknown'
            
            self.box.video['aspect'] = vf.sample_aspect
            self.box.video['width'] = vf.width
            self.box.video['height'] = vf.height
        
        self.box.video['duration'] = source.duration
        import datetime
        self.box.video['time'] = str(datetime.timedelta(seconds=source.duration))
        self.box.video['hash'] = self.hashfile(self.source)

    def showVideo(self):
        '''show video with os.startfile source'''
        source = self.box.video['source']
        # subprocess.call(['ffplay', source])
        os.startfile(source)

    def showImage(self):
        '''show image with os.startfile source'''
        os.startfile(self.box.image['source'])

    def hashfile(self, path, blocksize = 65536):
        '''read file and return its hasher 
        paramters:
            path -  this is actual name of the file
            blocksize = 65536 this is the long bate readed
        '''
        import hashlib
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()

    def __str__(self):
        return str(self.box)

    def __repr__(self):
        return str(self.box)


class ManagerBox:

    def __init__(self, source=None):
        self.tr = None
        self.source = None
        self.managerlist = []
        self.files = []
        self.ext = ('.mp4', '.flv', '.mpeg', '.avi')
        if source:
            self.source = os.path.abspath(source)
            print('ManagerBox._init_.source:', self.source)
            if os.path.isdir(self.source):
                for f in os.listdir(self.source):
                    if f.endswith(self.ext):
                        self.files.append(f)
                self.tr = threading.Thread(target=self._load_thread, args=(self.files,), daemon=True)
                self.tr.start()
                # self.load_thread(self.files)

    def _load_thread(self, files=[]):
        for item in files:
            source = os.path.join(self.source, item)
            buildbox = BuildBox(source)
            self.managerlist.append(buildbox.box)
            buildbox = None
    
    def save(self, path=None):
        if path:
            with open(path, 'w') as f:
                json.dump(self.managerlist, f, default=Box().to_json, indent=2)
    
    def load(self, path=None):
        if path:
            with open(path, 'r') as f:
                data = f.read()
            self.managerlist = json.loads(data, object_hook=Box().from_json)

    def isAlive(self):
        if self.tr is None:
            return False  
        return self.tr.isAlive()

    def showVideo(self, index=0):
        '''show video with os.startfile source'''
        ln = len(self.managerlist)
        if index <= ln and index >= 0:
            source = self.managerlist[index].video['source']
            os.startfile(source)

    def showImage(self, index=0):
        '''show image with os.startfile source'''
        ln = len(self.managerlist)
        if index <= ln and index >= 0:
            os.startfile(self.managerlist[index].image['source'])

    def __str__(self):
        return str(self.managerlist)
    
    def __repr__(self):
        return str(self.managerlist)


if __name__ == '__main__':
    import time
    print('current_dir:', os.getcwd())
    source = 'video/awesome sucks - Amatuer wifey sucks crazy.mp4'
    buildbox = BuildBox(source=source)
    print(buildbox)
    with open('buildbox_file.json', 'w') as f:
        json.dump(buildbox.box, f, default=buildbox.box.to_json, indent=2)
    # buildbox.showVideo()
    # buildbox.showImage()
    # ManagerBox.
    
    managerbox = ManagerBox('video')
    while managerbox.isAlive():
        time.sleep(2)
    managerbox.save('managerbox_list.json')
    print('managerbox -->>', managerbox)
    print('ManagerBox load from file json')
    otro = ManagerBox()
    otro.load('managerbox_list.json')
    data = json.dumps(otro.managerlist, default=Box().to_json, indent=2)
    print(data)
    with open('cuota.txt', 'w') as f:
        f.write(data)
    otro.showVideo()
    otro.showVideo(index=10)

    
    