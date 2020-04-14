# Cyberland Server

New, rewritten Cyberland. We have done our best to emulate the way in which the old instances worked, however, some of these things are bad design and lack proper documentation. We are aware that MANY CLIENTS WILL BREAK which used to work on older versions. If you think there is something that can be done better

The source code for Cyberland.

## Setup 

Various methods of setting up the Flask application. The current build of this project is `Python 3.6`.


### Docker

Build the docker image with
```bash
docker build -t cyberland:latest .
```

Then create a directory (anywhere on your system) to hold the database in
```bash
mkdir instance
```
Create the docker container with
```bash
docker run -dit --name cyberland -p {PORT_ON_LOCAL_MACHIENE}:80 -v {PATH_TO_DATABASE FOLDER}:/usr/src/app/instance cyberland
```
For first run you will need to create the database
```bash
docker exec -it cyberland bash 
```
In this shell run
```bash
pipenv run flask init-db
```
If you set up the volumes correctly it should give you a success message. You can now exit the container shell with`exit`