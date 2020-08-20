#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, sys
import re
import hashlib
import subprocess
import threading
import json
from PIL import Image, ImageDraw

__autor__ = 'Hernani Aleman Ferraz'
__email__ = 'afhernani@gmail.com'
__apply__ = 'moviebox.py'
__version__ = 0.3
__all__ = ('Boxd', 'MovieBox')

class Boxd:
    def __init__(self, datos=None, **kwargs):
        self.box = {
                        "id":'xxx', "time": 0.0, "fps": 0.0, "width": 1, "height": 1,
                        "bitrate": 7, "num": 1, "remove": True, "file": "unknown",
                        "path_file": ".", "exists": False, "sucess": False,
                        "code_frame": "unknown", "working_file": ".Thumbails"
                      } if datos is None else datos
    
        if kwargs is not None:
            keys = self.box.keys()
            for k in keys:
                v = kwargs.get(k, None)
                if v:
                    self.box[k] = v
        if os.path.isdir(self.box['path_file']):
            self.name, self.exts = os.path.splitext(self.box['file'])
        else:
            return
        self.fileMovie = os.path.join(self.box['path_file'], self.box['file'])
        if os.path.exists(self.fileMovie):
            self.box['exists'] = True
            self.namegif = self.box['file'] + '_thumbs_0000.gif'
            self.filegif = os.path.join(self.box['working_file'], self.namegif)
            self._check()
        else:
            return

    def move_to(self, topath):
        '''move box to new path
            parameters:
                topath := moving to path - add directory to move
        '''
        if os.path.exists(self.fileMovie) and os.path.exists(self.filegif):
            if os.path.isdir(topath):
                tofileMovie = os.path.join(topath, self.box['file'])
                if self.fileMovie == tofileMovie: return
                tofilegifpath = os.path.join(topath, '.Thumbails')
                if not os.path.exists(tofilegifpath): os.mkdir(tofilegifpath)
                tofilegif = os.path.join(tofilegifpath, self.namegif)
                try:
                    os.rename(self.fileMovie, tofileMovie)
                    os.rename(self.filegif, tofilegif)
                except Exception as e:
                    print(f'Exception has happened, {str(e.args)}') 
            else:
                print(f"hei!!, to path {topath} do not exist")
        else:
            print(f"Hei!!, one of files {self.fileMovie} - {self.filegif} , do not exist for to move")

    def rename(self, newname):
        '''
        rename files box,
            parameter:
                newname: name of video file with extension
        '''
        if os.path.exists(self.fileMovie) and os.path.exists(self.filegif):
            
            renfileMovie = os.path.join(self.box['path_file'], newname)
            if self.fileMovie == renfileMovie: return
            newname_gif = newname + '_thumbs_0000.gif'
            renfilegifpath = os.path.join(self.box['working_file'], newname_gif)
            try:
                os.rename(self.fileMovie, renfileMovie)
                os.rename(self.filegif, renfilegifpath)
            except Exception as e:
                print(f'Exception has happened, {str(e.args)}') 
            
        else:
            print(f"Hei!!, one of files {self.fileMovie} - {self.filegif} , do not exist for to move")

    @staticmethod
    def hashfile(path, blocksize = 65536):
        '''read file and return its hasher 
        paramters:
            path -  this is actual name of the file
            blocksize = 65536 this is the long bate readed
        '''
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()   

    def hash_rename(self):
        source = self.fileMovie
        if os.path.exists(source):
            hash_name_file = Boxd.hashfile(path=source) + self.exts
            self.rename(hash_name_file)
            ''' hash_name_file_gif =hash_name_file + '_thumbs_0000.gif'
            path_to_newname_file = os.path.join(self.box['path_file'], hash_name_file)
            path_to_newname_file_gif = os.path.join(self.box['working_file'], hash_name_file_gif)
            try:
                os.rename(source, path_to_newname_file)
                if os.path.exists(self.filegif):
                    os.rename(self.filegif, path_to_newname_file_gif)
                else:
                    print(f'source do not exist {self.filegif}')
            except Exception as e:
                print(f'problem to rename file {source} to {path_to_newname_file} - {str(e.args)}')
        else:
            print(f'source do not exist {source}') '''

    def _check(self):
        source = self.fileMovie
        if os.path.exists(source):
            moviebox = MovieBox(source=source)
            if not os.path.exists(self.filegif):
                moviebox.compiler()
            # self.box = moviebox.datos.copy()
        else:
            print(f'some issue, source do not exist {source}')
    
    def remove(self):
        try:
            os.remove(self.fileMovie)
            os.remove(self.filegif)
        except Exception as e:
            print(f"some issue to remove the {self.fileMovie} - {self.filegif} : {str(e.args)}")


class MovieBox:
    def __init__(self, source=None, datos=None, block=None):
        self.block ={'thumbs': []} if block is None else block
        self.datos = {
                        "time": 0.0,
                        "fps": 0.0,
                        "width": 1,
                        "height": 1,
                        "bitrate": 7,
                        "num": 1,
                        "remove": True,
                        "file": "unknown",
                        "path_file": ".",
                        "exists": False,
                        "sucess": False,
                        "code_frame": "unknown",
                        "working_file": ".Thumbails"
                      } if datos is None else datos
        self.source = os.getcwd() if source is None else os.path.abspath(source)
        if source is None:
            if datos is not None:
                self.source = os.path.abspath(self.datos['path_file'])
            elif block is not None and len(block['thumbs']) > 0:
                self.datos = self.block['thumbs'][-1].copy()
                self.source = os.path.abspath(self.datos['path_file'])
            return 
        if not os.path.isdir(self.source):
            self.datos['file'] = os.path.basename(self.source)
            self.datos['path_file'] = os.path.dirname(self.source)
            self.datos['exists'] = True
            self._info_from_video()
            self._work_file()
            self.block['thumbs'].append(self.datos.copy())
        else:
            self.datos['path_file'] = self.source
            self.datos['exists'] = False
            self._make_block()
            
    def _make_block(self):
        ext = ('.mp4', '.flv', '.avi', '.mpg')
        source = self.datos['path_file']
        fount = os.listdir(source)
        for file in fount:
            if file.endswith(ext):
                self.datos['file'] = file
                self.datos['exists'] = True
                self._info_from_video()
                self._work_file()
                self.block['thumbs'].append(self.datos.copy())
                self.datos['sucess'] = False

    def _work_file(self):
        self.datos['working_file'] = os.path.join(self.datos['path_file'] ,'.Thumbails')
        # import uuid
        name = os.path.splitext(self.datos['file'])[0]
        # name = str(uuid.uuid4()) + '-%04d.png'
        name += '-%04d.png'
        self.datos['code_frame'] = name
    
    def __str__(self, *args):
        return str(self.datos)

    def save_to_json(self, path=None):
        if path:
            path = os.path.abspath(path)
            with open(path, 'w') as f:
                json.dump(self.block, f, indent=2)
    
    def load_from_json(self, path=None):
        if path:
            with open(path, 'r') as f:
                data = f.read()
            self.block = json.loads(data)
            self.datos = self.block['thumbs'][-1].copy()

    def make_cadencia(self):
        scale = '740:-2'
        if self.block['thumbs']:
            try:
                for f in self.block['thumbs']:
                    i = f['width']
                    if i > 920:
                        file = os.path.join(f['path_file'], f['file'])
                        out = os.path.splitext(f['file'])[0][0:12] + '.mp4'
                        out = os.path.join(f['path_file'], out)
                        if os.path.exists(file):
                            command = ['ffmpeg', '-y', '-i', file]
                            command2 = ['-vf', 'scale=' + scale, out]
                            command.extend(command2)
                            self.runCommand(command)
                
            except Exception as e:
                print('Exception make_cadencia:', str(e.args))

    def compiler(self, num=15, framerate=1, scale='320:-1'):
        ''' create thum at Thumbails
        parameter:
            num : number of images extracting
            framerate : 1, for 1 frame por second
            scale : scale image gif

        print(f'begin the compilation {self.block}')
        
        recorre self.block - obtiene elemento y extrae los datos importantes
        - verifica si existe compilado si, saltar . no compilar 
        '''
        if self.block['thumbs']:
            # scale = '300:-1'
            try:
                for f in self.block['thumbs']:
                    wfd = f['working_file']
                    if not os.path.exists(wfd): os.mkdir(wfd)
                    i = f['code_frame']
                    if i:
                        frames = os.path.join(wfd, i)
                        file = os.path.join(f['path_file'], f['file'])
                        out = f['file'] + '_thumbs_0000.gif'
                        out = os.path.join(wfd, out)
                        if not os.path.exists(out):
                            command = ['ffmpeg']
                            valor = f['time']
                            if valor:
                                valor = valor / (num + 1)
                                if valor < 1: # no puede ser ziro
                                    valor = 1
                            command.extend(['-ss', str(int(valor)), '-i', 
                                            file, '-vf', 'fps=1/' + str(int(valor)),
                                            '-vframes', str(num),
                                            frames, '-hide_banner'])
                            print('Extract ->', command)
                            self.runCommand(command)
                            # aqui creamos el gif
                            command = ['ffmpeg', '-y', '-framerate', str(framerate), '-i', frames] #, '-vf', 'scale=' + scale]
        
                            if scale: # add scale if not nathing
                                command2 = ['-vf', 'scale=' + scale, out]
                                command.extend(command2)
                            print('create gif command ->', command)
                            self.runCommand(command)
                            # vamos a borrar los ficheros de imagen segun remove
                            if f['remove']:
                                code = i.split('-')[0]
                                pattern = '^' + code
                                # mypath = f['working_file']
                                print('remove:')
                                for root, dirs, files in os.walk(wfd):
                                    for file in filter(lambda x: re.match(pattern, x), files):
                                        print(file)
                                        os.remove(os.path.join(root, file))             
            except Exception as e:
                print('Exception make_cadencia:', str(e.args))

    def extract_images(self, num=None):
        ''' extract images from file datos.
            parameters:
               num: number image extracting
        '''
        num = 15 if num is None else num
        if self.block['thumbs']:
            # scale = '300:-1'
            try:
                for f in self.block['thumbs']:
                    wfd = f['working_file']
                    if not os.path.exists(wfd): os.mkdir(wfd)
                    i = f['code_frame']
                    if i:
                        frames = os.path.join(wfd, i)
                        file = os.path.join(f['path_file'], f['file'])
                        out = f['file'] + '_thumbs_0000.gif'
                        out = os.path.join(wfd, out)

                        command = ['ffmpeg']
                        valor = f['time']
                        if valor:
                            valor = valor / (num + 1)
                            if valor < 1: # no puede ser ziro
                                valor = 1
                        command.extend(['-ss', str(int(valor)), '-i', 
                                        file, '-vf', 'fps=1/' + str(int(valor)),
                                        '-vframes', str(num),
                                        frames, '-hide_banner'])
                        print('Extract ->', command)
                        self.runCommand(command)
            except Exception as e:
                print('Exception make_cadencia:', str(e.args))

    def extract_image(self, time=None)->Image:
        """ extract image a time definided temp
            return image """
        img = self.CreateImg()
        lasso = 0 if time is None else time
        if self.block['thumbs']:
            # scale = '300:-1'
            try:
                for f in self.block['thumbs']:
                    wfd = f['working_file']
                    if not os.path.exists(wfd): os.mkdir(wfd)
                    i = f['code_frame']
                    if i:
                        frames = os.path.join(wfd, i)
                        filein = os.path.join(f['path_file'], f['file'])

                        command = ['ffmpeg']
                        valor = f['time']
                        if lasso == 0 and valor: lasso = valor/3
                        elif lasso > 0 and lasso < valor:
                            pass #condicion a establecer.
                        # ffmpeg -loglevel quiet -ss 26 -i sample-video.mp4  -t 1 -f image2 anyfilename.jpeg
                        # ffmpeg -ss hh:mm:ss -i $INPUT_FILE -vframes 1 output.jpg
                        command.extend(['-loglevel', 'quiet' , '-y', '-ss', str(lasso), '-i', 
                                        filein, '-vframes', '1',
                                        frames, '-hide_banner'])
                        # print('Extract ->', command)
                        self.runCommand(command)
                        # cargamos la imagen
                        if f['remove']:
                                code = i.split('-')[0]
                                pattern = '^' + code
                                # mypath = f['working_file']
                                # print('remove:')
                                for root, dirs, files in os.walk(wfd):
                                    for fi in filter(lambda x: re.match(pattern, x), files):
                                        # print(fi)
                                        img = Image.open(os.path.join(root, fi)).copy()
                                        # os.remove(os.path.join(root, fi))
            except Exception as e:
                print('Exception make_cadencia:', str(e.args))
        return img

    def add_dato(self, block=None):
        ''' add list of dictionary datos from another file or files json 
            to present block 
            parameter:
                block : list of datos = [ { "time": 0.0, "fps": 0.0, "width": 1,
                            "height": 1, "bitrate": 7, "num": 1, "remove": True,
                            "file": "unknown", "path_file": ".", "exists": False,
                            "sucess": False, "code_frame": "unknown","working_file": ".Thumbails"
                            } ]
            here don't check is date redunant
        '''
        if block['thumbs'] and type(block['thumbs']) == type(list()):
            self.block['thumbs'].extend(block.copy())
            self.datos = self.block['thumbs'][-1].copy()

    def printOutput(self, string):
        '''
        Pretty print multi-line string
        '''
        for line in string.splitlines():
            print('>> {}'.format(line.decode('utf8')))

    def runCommand(self, command):
        p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT).stdout
        while True and p:
            line = p.readline()
            if not line:
                break
            self.printOutput(line)              

    def _info_from_video(self):
        print('extrac_informacion ->', self.datos['file'])
        if not self.datos['exists']:
            print('no se pudo extraer informacion del fichero')
            return
        movie = os.path.join(self.datos['path_file'], self.datos['file'])
        if not os.path.exists(movie):
            return
        command = ['ffmpeg', '-i', movie]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()

            matches = re.search(b'Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),',
                                stdout, re.DOTALL).groupdict()
            if matches:
                t_hour = matches['hours']
                t_min = matches['minutes']
                t_sec = matches['seconds']

                t_hour_sec = int(t_hour) * 3600
                t_min_sec = int(t_min) * 60
                t_s_sec = float(t_sec)

                total_sec = t_hour_sec + t_min_sec + t_s_sec
                self.datos['time'] = total_sec
                print('hora, minuto, segundo:', t_hour, t_min, t_sec)
                print('total de segundos:', total_sec)

            # This matches1 is to get the frames por segundo
            matches1 = re.search(b'(?P<fps>(\d+.)* fps)', stdout)
            if matches1:
                print('fps ->', matches1['fps'])
                frame_rate = matches1['fps'].split(b' ')[0]
                self.datos['fps'] = float(frame_rate)
                print('fps ->', self.datos['fps'])

            matches2 = re.search(b' (?P<width>\d+)x(?P<height>\d{2,4}[, ])', stdout)
            if matches2:
                print(matches2)
                width = int(matches2['width'])
                height = int(matches2['height'].replace(b',', b' '))
                print('formato: ->', matches2, width, height)
                self.datos['width'] = width
                self.datos['height'] = height

            # averiaguar el ratio. 
            matches3 = re.search(b'bitrate:\s{1}(?P<bitrate>\d+?)\s{1}', stdout)
            if matches3:
                print('matches3 ->', matches3['bitrate'])
                self.datos['bitrate'] = int(matches3['bitrate'])

        except subprocess.CalledProcessError as e:
            print(e.output)
            return
        self.datos['sucess'] = True
        print('extracted informacion from ->', self.datos['file'])

    def CreateImg(self)->Image:
        im = Image.new('RGBA', (320, 240), (0, 0, 0, 255)) 
        draw = ImageDraw.Draw(im)
        p1 = (0, 0, im.size[0], im.size[1])
        p2 = (0, im.size[1], im.size[0], 0)
        draw.line(p1, fill=(255,0,0), width=20)
        draw.line(p2, fill=(255,0,0), width=20)
        # im.save('x.png')
        # os.startfile('x.png')
        return im

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='moviebox', description='Working movie gif staff')
    parser.add_argument('action', choices=['run', 'list', 'load', 'add', 'box'],
                        help='''action to be performed, run new video with scale 720:-2,
                        create list, load list, add list, and box options, rename''')
    parser.add_argument('-d', '--directory', type=str,
                        help='directory to be worked')
    parser.add_argument('-f', '--file', type=str,
                        help='file to be worked')
    parser.add_argument('-c', '--compiler', action='store_true',
                        help='directory or file to be compiled')
    parser.add_argument('-r', '--rename', action='store_true',
                        help='rename or file to be hash code')
    parser.add_argument('-m', '--move', type=str,
                        help='move file to other directory')
    parser.add_argument('-x', '--remove', action='store_true',
                        help='remove file')
    parser.add_argument('-i', '--image', type=int,
                        help='extract from video file a number of images')
    parser.add_argument('-t', '--time', type=int,
                        help='extract from video file a image at time: box -f path_to_file -t time')
    parser.add_argument('-o', '--out', type=str,
                        help='dir for out image: box -f path_to_file -t time -o full_name_file_image')
    parser.add_argument('--version', action='version', version='%(prog)s '+str(__version__))
    args = parser.parse_args()


    if args.directory:
        path = os.path.abspath(args.directory)
        if not os.path.isdir(path): 
            print('select directory not file')
            sys.exit(1)
        source = os.path.join(path, 'Thumb.json')
        if args.action == 'list':
            video = MovieBox(source=path)
            video.save_to_json(source)
            if args.compiler:
                '''list -d . -c'''
                video.compiler()
        elif args.action == 'run':
            video = MovieBox(source=path)
            video.save_to_json(source)
            video.make_cadencia()
        elif args.action == 'load':
            ''' load -d . '''
            video = MovieBox()
            if not os.path.exists(source):
                print('do not exist Thumb.json, before obtion: list -d . ')
                sys.exit(1)
            video.load_from_json(source)
            # aqui hacemos lo que quermos hacer con la lista
            # compilar, revisar, add , etc..
            if args.compiler:
                ''' load -d . -c '''
                video.compiler()
        elif args.action == 'add':
            ''' add -d . # busca todos los json en la raiz y los add al thumb.json '''
            print('enything to do for now, not encoding')
        elif args.action == 'box':
            if args.rename:
                ''' box -d directory -r '''
                video = MovieBox(source=path)
                for it in video.block['thumbs']:
                    box = Boxd(datos=it)
                    box.hash_rename()
            
    elif args.file:
        path = os.path.abspath(args.file)
        if os.path.isdir(path):
            print('select a file not a directory')
            sys.exit(1)
        if not os.path.exists(path):
            print('do not exist file')
            sys.exit(0)
        ruta = os.path.dirname(path)
        name = os.path.splitext(path)[0].split('\\')[-1] +'.json'
        name_ruta = os.path.join(ruta, name)

        if args.action == 'list':
            video = MovieBox(source=path)
            video.save_to_json(name_ruta)
            if args.compiler:
                ''' list -f path_to_file - c : crea lista del fichero y compila'''
                video.compiler()
        elif args.action == 'run':
            video = MovieBox(source=path)
            video.make_cadencia()
        elif args.action == 'add':
            ''' add -f path_to_file : add file to thumb.json'''
            video = MovieBox()
            if not os.path.exists(name_ruta):
                print(f'file {name} not exist, befor this obtion list -f namefile') 
                sys.exit(1)
            video.load_from_json(name_ruta)
            new_dato = video.block.copy()
            print(f'adding datos: {new_dato}')
            thumb_json = os.path.join(ruta, "Thumb.json")
            if not os.path.exists(thumb_json):
                print(f'Thumb.json at {ruta} do not exists, before obtion: list -d . ')
                sys.exit(1)
            video.load_from_json(thumb_json)
            video.add_dato(new_dato)
            video.save_to_json(thumb_json)
            print(f'{name} add to Thumb.json')
        elif args.action == 'load':
            ''' load -f path_to_file '''
            video = MovieBox()
            if not os.path.exists(name_ruta):
                print(f'file {name} not exist, befor this obtion list -f namefile') 
                sys.exit(1)
            video.load_from_json(name_ruta)
            if args.compiler:
                ''' load -f path_to_file -c '''
                video.compiler()
        elif args.action == 'box':
            video = MovieBox(source=path)
            box = Boxd(datos=video.datos)
            if args.rename:
                ''' box -f path_to_file -r '''
                box.hash_rename()
            if args.move:
                ''' box -f path_to_file -m new_path '''
                box.move_to(os.path.abspath(args.move))
            if args.remove:
                ''' box -f path_to_file -x '''
                box.remove()
            if args.image:
                ''' box -f path_to_file -i num '''
                video.extract_images(num=args.image)
            if args.time:
                ''' box -f path_to_file -t time '''
                img = video.extract_image(time=args.time)
                if args.out:
                    '-o full_name_image'
                    p_img = os.path.join(args.out)
                else:
                    p_img = os.path.join(ruta, 'prueba.png')
                img.save(p_img)


