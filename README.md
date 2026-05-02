# Poor Spotify 🎵
This Project will help you to share your music and podcasts with your friends when internet goes down!

Just upload a mp3 file and everything is getting ready to enjoy listening 🫠

## Options
- No need to register or authorize
- Auto Exteract file metadata (name,artist,cover and etc...)
- Spoify like UI
- Streaming system (chunk by chunk)
- Portable database
- Add a batch of music [utils](https://github.com/farzadoxo/poor-spotify/tree/master/src/utils)
## How to use:

### Docker:

### Local:
1. Activate you venv and install packages using command bellow:
```bash
$~ pip install -r requirements.txt
# if official pypi mirrors was not available use a internal mirror like runflare mirror eg:
# pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt
```
2. Clone this project and `cd` to `src/` directory
3. Create a `.env` file and insert HOST and PORT in it eg:
```bash
# inside of .env file
HOST='127.0.0.1'
PORT='6969'

# if you want to make access on network for other devices; set HOST on 0.0.0.0
```
4. Just run `main.py` file.
```bash
$~ python3 main.py 
# this is a setup file that make everything ready and run project 
```

## Notes
- Frontend of this project will render by django render engien.
- Music file will saved in `static/musics/`
- Music cover file will saved in `static/covers/`
- Playlist mechanism front-end is not ready but backend is ready. if you can help, tell me :) 