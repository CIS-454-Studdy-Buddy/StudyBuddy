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
Create virtual environment
pip3 install -r requirements.txt
## Do the remaining steps everytime  
source venv/bin/activate // this activates the virtual environment
flask run
copy and paste the url shown in the terminal 