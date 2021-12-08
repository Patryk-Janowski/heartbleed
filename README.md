# Heartbleed Example

## Introduction

As part of my Software Security classes, I wanted to make this code available
for OpenSSL's Heartbleed vulnerability demostration.

## Requirements and instalation

* Docker
* Metasploit
* Python 2
```shell
sudo apt-get update
sudo apt-get install -y python2-dev docker.io metasploit-framework curl
```
* Python 2 packages
```shell
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output /tmp/get-pip.py
sudo python2 /tmp/get-pip.py
pip install --upgrade setuptools
pip install gmpy pyasn1
```
## Docker Setup

```shell
docker pull docker.io/andrewmichaelsmith/docker-heartbleed
```

## Run the container

On a terminal window, run the command:

```shell
sudo docker run -it -p 127.0.0.1:443:443 andrewmichaelsmith/docker-heartbleed bash
```

This command will execute bash in conatiner and map host adress 127.0.0.1:443 to local conatiner adress on port 443

Type exit to exit container


## Run the server
inside contrainer run"
```shell
apache2ctl -D FOREGROUND
```
You can access server via https://127.0.0.1
(unfortunetly this is default website for old version of apache2)

## Stimulate the server

Before exploiting, you must stimulate the server with potentially sensitive data
that can be harvested later by the exploit. The `stimulate_server.py` script
does that, sending random credentials to the server via HTTP POST requests. The
following is its usage and options:

```shell
Usage: stimulate_server.py [-a server_address] [-t sleep]
```
## Get to know server
* using nmap check if server is vulnerable
```shell
sudo nmap -p 443 --script ssl-heartbleed 127.0.0.1
```

* if you wish to run another instance of bash inside container do:
```shell
sudo docker ps -a 
sudo docker exec -it <id> /bin/bash
```
* view certificate
* check openssl version

## Exploit using script

This repo includes heartbleed.py script (in python2)

You can use it calling it with python. This is its help
output:

```shell
./heartbleed.py -h
```

* using script try to extract some sensitive data
* set verbose option analize how script executes
* try to steal server private key and certificate