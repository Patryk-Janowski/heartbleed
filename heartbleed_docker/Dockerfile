FROM ubuntu:13.04

RUN apt-get update
RUN apt-get install -y build-essential \
 	checkinstall \ 
 	zlib1g-dev \ 
 	apt-utils \
	wget \ 
	nano \ 
	apache2




RUN echo """WORKDIR /usr/local/src/
RUN wget -P /usr/local/src/ https://www.openssl.org/source/old/1.0.1/openssl-1.0.1c.tar.gz
RUN apt-get purge openssl --auto-remove -y
RUN tar -xvf /usr/local/src/openssl-1.0.1c.tar.gz
WORKDIR /usr/local/src/openssl-1.0.1c
RUN ./config --prefix=/usr/local/ --openssldir=/usr/local/openssl
RUN make
RUN make install_sw
WORKDIR /
RUN cp -p -r /usr/local/openssl /usr/bin/openssl"""


RUN mkdir /etc/apache2/ssl
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"  
RUN rm /etc/apache2/sites-available/default-ssl.conf

ADD default-ssl /etc/apache2/sites-available/default-ssl.conf

RUN a2enmod ssl
RUN a2ensite default-ssl

EXPOSE 443

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

CMD ["bin/bash"]
