# StudyBuddy
## Setup Local Repo
Create project folder in your home directory

`mkdir project`

`cd project`

Create ssh key by following instructions to the link: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Then add ssh public key in github by following this link: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

Once these two are set then you do git clone command below

`git clone git@github.com:CIS-454-Studdy-Buddy/StudyBuddy.git`

## Run Locally 

Open terminal

Go to Project Folder called StudyBuddy

## Do only one time

Create virtual environment in the project folder  
name the venv "venv"  

python3 -m venv venv  
source venv/bin/activate // this activates the virtual environment  
pip3 install -r requirements.txt  

**command "deactivate" to close  

## Create new database if you get SQLAlchemy errors

```
python3
from app.utils import create_db, seed_data
create_db()
seed_data()

```


## Do the remaining steps everytime  
source venv/bin/activate  
flask run  
copy and paste the url shown in the terminal to your web browser  

https://github.com/git-guides/git-pull 


## Build project for distribution
Run the build command below and it will create tar file in dist folder

```
python -m build

```

Upload the tar file to s3 bucket

asg user data copies this file ec2

running manual commands on the terminal

```

yes | tar -xvf studybuddy.tar.gz 
mv StudyBuddy-1.0.1 studybuddy
sudo yum install python3.9
sudo yum install python-pip
cd studybuddy
pip install -r requirements.txt

```

