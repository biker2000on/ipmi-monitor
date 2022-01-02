FROM python:3-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt install ipmitool && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ipmi.py" ]
