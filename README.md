# Cyberland Server

The source code for Cyberland.

## Setup 

Various methods of setting up the Flask application. The current build of this project is `Python 3.6`. Please make sure you have this version of greater to create the virtualenv.


### Virtualenv
Create a virtual environment with python 3.6 in the root of the project.
```bash
virtualenv -p python3.6 venv
```
Then activate the environment using
```bash
source venv/bin/activate
```
Install python dependencies
```bash
pip install -r requirements.txt
```

To run the project first set environment variables
```bash
export FLASK_APP=flaskr
```
Then start the development server with
```bash
flask run
```