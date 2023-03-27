#!/bin/bash
cd /home/ec2-user
rm -r studybuddy/
rm studybuddy.tar.gz
sudo systemctl stop studybuddy.service 
aws s3 cp s3://sustudybuddy-deployment/StudyBuddy-1.0.1.tar.gz /home/ec2-user/studybuddy.tar.gz
yes | tar -xvf studybuddy.tar.gz 
mv StudyBuddy-1.0.1 studybuddy
sudo yum install python3.9
sudo yum install python-pip
cd studybuddy
pip install -r requirements.txt
cd app
mv __init__.py application.py
touch __init__.py
cd ..
sudo systemctl stop studybuddy.service
sudo systemctl daemon-reload
sudo systemctl enable studybuddy.service
sudo systemctl start studybuddy.service
sudo systemctl status studybuddy.service
#flask run --host=0.0.0.0 --port=8080