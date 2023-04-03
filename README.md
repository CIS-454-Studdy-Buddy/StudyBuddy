# StudyBuddy
## STEP BY STEP INSTRUCTIONS

### HOW TO RUN LOCALLY ON YOUR COMPUTER

**Visit [sustudybuddy.com](https://sustudybuddy.com) to see the website**

INSTALLS:

Install python 3.9 or higher and make sure to install pip


**Install for linux:**
1. `sudo apt-get update`
2. `sudo apt install python3.10 python3-pip python3.10-venv`
3. Installing sqlite3 `sudo apt install sqlite3`


**Install for mac:**
Use package manager or download the python package from
https://www.python.org/downloads/

Insure python is installed by running `python3 –-version` in terminal
Insure pip is installed by running `pip3 –-version` in terminal

Open up the terminal and change your directory to a place you would like to save the project.
Using Git clone the repository
`git clone https://github.com/CIS-454-Studdy-Buddy/StudyBuddy.git`
Use the ls command to verify the newly made StudyBuddy project folder is in the directory

`cd` into the StudyBuddy directory

type in terminal `python3 -m venv “venv”` to create the new environment name

type in terminal `source venv/bin/activate` to activate the python environment

Make sure you are in the Study Buddy folder and type
`pip3 install -r requirements.txt`

Next, to create a database type in the terminal
`python3`
Then `from app.utils import create_db, seed_data`
Then `create_db()`
Then `seed_data()`



### OPTIONAL:
For creating testing seed data the function seed_data() in the file StudyBuddy/app/utils.py will create 5 existing users in the database to test from.
These are accounts with our team's emails stored in them. 
Using the website with these accounts will send us emails but feel free to use them.

**Email:**
aalakkad@syr.edu
mjfaiola@syr.edu
thakki@syr.edu

**Password for all:**
123456





### TO RUN THE APP FROM TERMINAL

In terminal `flask run` or `flask run –port 5001`
Copy the output address into your web browser and the website should be running there. 


If you want to go into the database used in the local testing you can run `sqlite3 database.db` in the terminal from the StudyBuddy main folder.




## FOR DEVS:

Create ssh key by following instructions to the link: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Then add ssh public key in github by following this link: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account



### Build project for distribution
Run the build command below and it will create tar file in dist folder

`python -m build`

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

