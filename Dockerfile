FROM python:3.10.11-bullseye

RUN apt update \
 && apt -y upgrade \
 && pip install --upgrade pip \
 && apt install -y --no-install-recommends build-essential git \
 && pip install psycopg2 \
 && pip install apscheduler \
 && pip install asyncio \
 && pip install datetime \
 && apt autoremove -y \
 && apt clean all \
 && rm -rf /etc/apk/cache \
 && rm -rf /var/lib/apt/lists/*
EXPOSE 8000
COPY . .

CMD ["python3", "main.py"]