FROM python:3-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update \
  && apt install -y ipmitool \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ipmi.py" ]
