FROM python:3.11

WORKDIR /AiBot

COPY requirements.txt ./

RUN pip install --upgrade pip \
 && pip install -r requirements.txt;

COPY . .

CMD ["python", "-m", "tgbot.main"]
