# Heartbleed

## Requirements and instalation

### Ubuntu 20.04

* Docker
* Metasploit
* Python 2
*
```shell
sudo apt-get update &&
sudo apt-get install -y python2-dev docker.io metasploit-framework curl build-essential zlib1g zlib1g-dev libpq-dev libpcap-dev libsqlite3-dev ruby ruby-dev
```
* Install Metasploit
```shell
git clone https://github.com/rapid7/metasploit-framework.git &&
cd metasploit-framework/ &&
sudo gem install bundlerlibsqlite3-dev ruby ruby-dev &&
sudo bundle install
```


* Python 2 packages
```shell
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output /tmp/get-pip.py &&
sudo python2 /tmp/get-pip.py &&
pip install --upgrade setuptools &&
pip install gmpy pyasn1
```
## Docker Setup

```shell
sudo docker pull docker.io/andrewmichaelsmith/docker-heartbleed
```
## Clone Repository

```shell
git clone https://github.com/okrutnik420/heartbleed.git &&
cd heartbleed &&
chmod 755 *
```

## Run the container

On a terminal window, run the command:

```shell
sudo docker run -it -p 127.0.0.1:443:443 andrewmichaelsmith/docker-heartbleed bash
```

This command will execute bash in conatiner and map host address 127.0.0.1:443 to local conatiner address on port 443

Type exit to exit container


## Run the server
Inside container run
```shell
apache2ctl -D BACKGROUND
```
You can access server via https://127.0.0.1
(unfortunetly this is default website for old version of apache2)


## Excercise 1: Find potential victims and get to know the sever

#### 1. Finding vulnerable sites
* use https://safeweb.norton.com/heartbleed to check if your favourite site is vulnerable.
* try to find site which is vulnerable to heartbleed (for example you can use https://shodan.io).

#### 2. Using nmap check if server and found site are vulnerable
```shell
sudo nmap -p 443 --script ssl-heartbleed <IP>
```

#### If you wish to run another instance of bash inside container do:
```shell
sudo docker ps -a 
sudo docker exec -it <id> /bin/bash
```
#### 3. View certificate and private key
If you wish to run another bash instance inside container

```shell
sudo docker ps -a 
sudo docker exec -it <id> /bin/bash
```
You can inspect Dockerfile to check how server was set up

#### 4. Check openssl version

## Excercise 2: Exploit using script

* Before exploiting, you must stimulate the server with potentially sensitive data
that can be harvested later by the exploit. The `stimulate_server.py` script
does that, sending random credentials to the server via HTTP POST requests. The
following is its usage and options:

```shell
./stimulate_server.py [-a server_address] [-t sleep]
```

* Troubleshooting in case curl failure:

Edit openssl.conf file:

"""shell
sudo nano /etc/ssl/openssl.cnf
"""

Add this line at the top:

"""shell
openssl_conf = openssl_init
"""

And then this to the end:

"""shell
[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
CipherString = DEFAULT@SECLEVEL=1
"""

* To populate server memory with keys run:
```shell
watch 'cat /etc/apache2/ssl/apache.crt ; cat /etc/apache2/ssl/apache.key'

```

#### 1. Using script try to extract some sensitive data
This repo includes heartbleed.py script (in python2)

```shell
./heartbleed.py -h
```
* read script manual
* explore options

#### 2. Analize how script executes
* Set verbose flag
* Addionatly you can use Wireshark to inspect network traffic

#### 3. Try to steal server private key and certificate


## Exercise 3: Exploit using metasploit

#### 1. Start the Metasploit console
```shell
sudo ./msfconsole
```

#### 2. Search Heartbleed module by using built in search feature in Metasploit framework
```shell
search heartbleed
```

#### 3. Load the heartbleed by module
```shell
use auxiliary/scanner/ssl/openssl_heartbleed
```

#### 4. After loading the auxiliary module, extract the info page to reveal the options to set the target
```shell
show info
```

#### 5. This is a list of all auxiliary actions that the scanner/ssl/openssl_heartbleed module can do:
```shell
show actions
```

#### 6. Here is a complete list of advanced options supported by the scanner/ssl/openssl_heartbleed auxiliary module:
```shell
show advanced
```

#### 7. To view full list of possible evasion options supported by the scanner/ssl/openssl_heartbleed auxiliary module in order to evade defenses:
```shell
show evasion
```

#### 8. Explore available options and actions than:
 * Set RHOST 
 * Set Action
 * Run
#### 9. Extract Certificate and Private Key using metaspolit

## Excercise 4: some code snippet 

#### 1. Inspect heartbeat request/response packet

**Format of the Heartbeat request/response packet**

```c
struct {
    HeartbeatMessageType type;  // 1 byte: request or the response
    uint16 payload_length;      // 2 byte: the length of the payload
    opaque payload[HeartbeatMessage.payload_length];
    opaque padding[padding_length];
} HeartbeatMessage;
```

The first field (1 byte) of the packet is the type information, and the second field (2 bytes) is the payload length, followed by the actual payload and paddings. The size of the payload should be the same as the value in the payload length field, but in the attack scenario, payload length can be set to a different value.

#### 2. Find faulty line in code below

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

