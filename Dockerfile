FROM python:3.8.0-buster
ADD "https://api.github.com/repos/1103s/crypto-bot/commits?per_page=1" check.json
RUN git clone https://github.com/1103s/crypto-bot.git
WORKDIR ./crypto-bot
RUN python3 -m pip install -r ./requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1 python3-opencv libgl1-mesa-glx  -y
# CMD ["-h"]
CMD ["python3", "./gui.py"]
