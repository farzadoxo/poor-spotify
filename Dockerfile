FROM python:latest

WORKDIR /src

COPY requirements.txt nginx.conf /src/

RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./src /src/

ENTRYPOINT ["python3","main.py"]