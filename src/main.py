import os
import dotenv

# load ip and port from .env 
dotenv.load_dotenv()
HOST = os.getenv('IP')
PORT = os.getenv('PORT')

# command attribute
apps = ['music','playlist']
BASE_COMMAND = 'python3 manage.py'


def main():
    for app in apps:
        os.system(f'{BASE_COMMAND} makemigrations {app}')
    
    os.system(f'{BASE_COMMAND} migrate')

    os.system(f'{BASE_COMMAND} runserver {HOST}:{PORT}')



if __name__ == "__main__":
    main()