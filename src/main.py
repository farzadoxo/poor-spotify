import os
import dotenv

# load ip and port from .env 
dotenv.load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# command attribute
apps = ['music','playlist']
BASE_COMMAND = 'python3 manage.py'


def main():
    for app in apps:
        os.system(f'{BASE_COMMAND} makemigrations {app}')
    
    os.system(f'{BASE_COMMAND} migrate')

    os.system(f'{BASE_COMMAND} collectstatic --noinput')
    # os.system(f'{BASE_COMMAND} runserver {HOST}:{PORT}')

    os.system(f'python3 -m gunicorn --bind {HOST}:{PORT} poor_spotify.wsgi:application')



if __name__ == "__main__":
    main()