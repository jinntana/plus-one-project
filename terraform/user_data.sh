#!/bin/bash

apt update -y
apt install -y python3 python3-pip python3-venv git

git clone https://github.com/jinntana/plus-one-project.git /home/ubuntu/plus-one-project

chown -R ubuntu:ubuntu /home/ubuntu/plus-one-project

runuser -u ubuntu -- bash -c '
cd /home/ubuntu/plus-one-project

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

nohup uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  > /home/ubuntu/plus-one-api.log 2>&1 &
'
