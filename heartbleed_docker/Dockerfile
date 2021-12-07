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
RUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
RUN make
RUN make install_sw


WORKDIR /usr/local/src/
RUN wget -P /usr/local/src/ http://archive.apache.org/dist/httpd/httpd-2.2.22.tar.gz
RUN tar -xvf /usr/local/src/httpd-2.2.22.tar.gz
WORKDIR /usr/local/src/httpd-2.2.22
RUN ./configure --build=aarch64-unknown-linux-gnu --enable-ssl --enable-so --with-ssl=/usr/local/openssl/
RUN make 
RUN make install


WORKDIR /

RUN mkdir /usr/local/apache2/ssl
#RUN /usr/local/bin/openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /usr/local/apache2/ssl/apache.key -out /usr/local/apache2/ssl/apache.crt -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"

ENV PATH "/usr/local/apache2/bin:$PATH"
ADD default-conf /usr/local/apache2/conf/httpd.conf
ADD default-ssl /usr/local/apache2/conf/extra/httpd-ssl.conf

#RUN a2enmod ssl
#RUN a2ensite default-ssl

EXPOSE 443

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log


CMD ["bin/bash"]
