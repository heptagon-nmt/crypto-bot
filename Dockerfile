FROM python:3.8.0-buster
RUN git clone https://github.com/1103s/crypto-bot.git
WORKDIR ./crypto-bot
RUN python3 -m pip install -r ./requirements.txt
CMD ["./crypto_util.py"]
ENTRYPOINT ["python3"]
