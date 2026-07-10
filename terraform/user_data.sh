#!/bin/bash

# Install and start the Plus One API

apt update -y
apt install -y python3 python3-pip python3-venv git
git clone https://github.com/jinntana/plus-one-project.git /home/ubuntu/plus-one-project

chown -R ubuntu:ubuntu /home/ubuntu/plus-one-project

runuser -u ubuntu -- bash -c '
cd /home/ubuntu/plus-one-project

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export JWT_SECRET="e864240766c9fae306e0f553841309331d84747c0e9448e79e29a2c100d6719d"
export JWT_ALGORITHM="HS256"
export JWT_EXPIRY_MINUTES= "30"



nohup uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  > /home/ubuntu/plus-one-api.log 2>&1 &
'
