import os
import pathlib
from music.models import Music
from colorama import Fore



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
               os.rename(i,f'{guid}.{format}')
               print(Fore.BLUE+f"CHANGE: {name}.{format} >>> {guid}.{format}")

                # insert in Database
               music = Music(name=name,url=guid,format=format)
               music.save()
               print(Fore.GREEN+"Item added to Database!")
               print(Fore.WHITE+"-"*30)

            else:
                print(Fore.RED+f"Invalid item: {i}")
                print(Fore.WHITE+"-"*30)


    else:
        raise InvalidPath(f'PATH IS INVALID!!! >>> {path}')
