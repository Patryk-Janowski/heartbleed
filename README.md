# Heartbleed Example

## Additional info

**Format of the Heartbeat request/response packet**

```c
struct {
    HeartbeatMessageType type;  // 1 byte: request or the response
    uint16 payload_length;      // 2 byte: the length of the payload
    opaque payload[HeartbeatMessage.payload_length];
    opaque padding[padding_length];
} HeartbeatMessage;
```

The first field (1 byte) of the packet is the type information, and the second field (2 bytes) is the payload length, followed by the actual payload and paddings. The size of the payload should be the same as the value in the payload length field, but in the attack scenario, payload length can be set to a different value. The following code snippet shows how the server copies the data from the request packet to the response packet.

**Process the Heartbeat request packet and generate the response packet**

```c
/* Allocate memory for the response, size is 1 byte
 * message type, plus 2 bytes payload length, plus
 * payload, plus padding
*/

unsigned int payload;
unsigned int padding = 16; /* Use minimum padding */

// Read from type field first
hbtype = *p++; /* After this instruction, the pointer
                * p will point to the payload_length field */

// Read from the payload_length field from the request packet
n2s(p, payload); /* Function n2s(p, payload) reads 16 bits
                  * from pointer p and store the value
                  * in the INT variable "payload". */

pl = p; // pl points to the beginning of the payload content

if (hbtype == TLS1_HB_REQUEST)
{
    unsigned char *buffer, *bp;
    int r;

    /* Allocate memory for the response, size is 1 byte
     * message type, plus 2 bytes payload length, plus
     * payload, plus padding
     */

    buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    bp = buffer;

    // Enter response type, length and copy payload *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);

    // copy payload
    memcpy(bp, pl, payload);   /* pl is the pointer which
                                * points to the beginning
                                * of the payload content */
    bp += payload;

    // Random padding
    RAND_pseudo_bytes(bp, padding);

    // this function will copy the 3+payload+padding bytes
    // from the buffer and put them into the heartbeat response
    // packet to send back to the request client side.
    OPENSSL_free(buffer);
    r = ssl3_write_bytes(s, TLS1_RT_HEARTBEAT, buffer, 3 + payload + padding);
}
```

**The vulnerability lies here**

```c
    // copy payload
    memcpy(bp, pl, payload);
```

There is no check to determine if `pl` is valid or not. Therefore, a memory breach can occur.

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
## Excercise 1: Get to know server

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

## Excercise 2 Exploit using script

This repo includes heartbleed.py script (in python2)

You can use it calling it with python. This is its help
output:

```shell
./heartbleed.py -h
```

* using script try to extract some sensitive data
* set verbose option analize how script executes
* try to steal server private key and certificate

## Excersice 3 Exploit using metaspoit

* Start the Metasploit console
```shell
# msfconsole
```