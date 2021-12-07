FROM ubuntu:21.10

RUN apt-get update
RUN apt-get install -y build-essential \
 	checkinstall \ 
 	zlib1g-dev \ 
 	apt-utils \
	wget \ 
	nano
	


WORKDIR /usr/local/src/
RUN wget -P /usr/local/src/ https://www.openssl.org/source/old/1.0.1/openssl-1.0.1c.tar.gz
RUN apt-get purge openssl --auto-remove -y
RUN tar -xvf /usr/local/src/openssl-1.0.1c.tar.gz
WORKDIR /usr/local/src/openssl-1.0.1c
RUN ./config
RUN make
RUN make install_sw


WORKDIR /usr/local/src/
RUN wget -P /usr/local/src/ http://archive.apache.org/dist/httpd/httpd-2.2.22.tar.gz
RUN tar -xvf /usr/local/src/httpd-2.2.22.tar.gz
WORKDIR /usr/local/src/httpd-2.2.22
RUN ./configure --build=aarch64-unknown-linux-gnu --enable-shared=max
RUN make && make install


WORKDIR /


#RUN mkdir /etc/apache2
#RUN mkdir /etc/apache2/ssl
#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"  
#RUN rm /etc/apache2/sites-available/default-ssl.conf

#ADD default-ssl /etc/apache2/sites-available/default-ssl.conf

#RUN a2enmod ssl
#RUN a2ensite default-ssl

EXPOSE 443

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

CMD ["bin/bash"]
