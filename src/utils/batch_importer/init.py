import os
import pathlib
from music.models import Music
from colorama import Fore
from tinytag import TinyTag


music_dir = 'static/musics'
cover_dir = 'static/covers'

class InvalidPath(Exception):
    # def __init__(self,path:str):
    #     self.path = path
    
    # def __str__(self):
    #     f"PATH IS INVALID!!! >>> {self.path}"

    pass


def main(path:str):
    if pathlib.Path(path).exists():
        os.chdir(path=path)

        allowed_format = ['mp3','m4a','ogg']
        items = os.listdir()

        for i in items:
            # print(Fore.WHITE+"-"*30)
            print(Fore.YELLOW+f"Item detect: {i}")
            name = i.split('.')[0]
            format = i.split('.')[-1]
            if os.path.isfile(i) and format in allowed_format:
                # making file ready
                guid = os.urandom(3).hex()
                saved_song = TinyTag.get(f'path/{i}')
                metadata = {'filename':saved_song.filename,
                    'title':saved_song.title,
                    'artist':saved_song.artist,
                    'album':saved_song.album,
                    'cover':saved_song.images.front_cover}
                
                os.rename(i,f'{guid}.{format}')
                print(Fore.BLUE+f"CHANGE: {name}.{format} >>> {guid}.{format}")
                if metadata['cover']:
                    cover_format = metadata['cover'].mime_type.split('/')[-1]
                    os.makedirs(cover_dir,exist_ok=True)
                    with open(f'{cover_dir}/{guid}.{cover_format}','wb+') as buffer:
                        buffer.write(metadata['cover'].data)

                # insert in Database
                song = Music(fileName=metadata['filename'],
                     title=metadata['title'],
                     artist=metadata['artist'] ,
                     isSingleTrack=True if metadata['album'] == None else False,
                     album=metadata['album'],
                     hasCover=True if metadata['cover'] != None else False,
                     coverFormat=cover_format if metadata['cover'] != None else None,
                     url=guid,
                     format=format)
                song.save()

                print(Fore.GREEN+"Item added to Database!")
                print(Fore.WHITE+"-"*30)

            else:
                print(Fore.RED+f"Invalid item: {i}")
                print(Fore.WHITE+"-"*30)


    else:
        raise InvalidPath(f'PATH IS INVALID!!! >>> {path}')
