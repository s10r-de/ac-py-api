# Active Collab

FROM ubuntu:24.04

VOLUME /var/log
VOLUME /var/www/html/logs
VOLUME /var/www/html/upload
VOLUME /var/www/html/thumbnails

# --- install packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y curl gpg unzip nginx && \
    apt-get install -y php8.2 php-fpm \
        php-cgi \
        php-cli \
        php-common \
        php-curl \
        php-gd \
        php-gmp \
        php-mysqli \
        php-memcache \
        php-odbc \
        php-opcache \
        php-pspell \
        php-readline \
        php-snmp \
        php-tidy \
        php-xml \
        php-xmlrpc \
        php-bcmath \
        php-bz2 \
        php-dba \
        php-fpm \
        php-imap \
        php-intl \
        php-mbstring \
        php-phpdbg \
        php-soap \
        php-xsl \
        php-zip

# --- install elastic search
RUN curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch |\
    gpg --dearmor -o /usr/share/keyrings/elastic.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" |\
     tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && \
    apt-get install -y elasticsearch

# --- install ActiveCollab
ADD activecollab-7.4.375.zip /tmp
RUN unzip -d /var/www/html/ /tmp/activecollab-7.4.375.zip
RUN rm -f /tmp/activecollab-7.4.375.zip
RUN chown -R www-data:www-data /var/www/html/

# probe script to check dependencies, remove for production!
#RUN curl -L -o /var/www/html/public/probe.php https://raw.githubusercontent.com/activecollab/activecollab-probe/refs/heads/master/probe.php
#RUN chown www-data:www-data /var/www/html/public/probe.php

# mysql admin tool, remove for production!
RUN curl -L -o /var/www/html/public/adminer.php https://github.com/vrana/adminer/releases/download/v4.8.1/editor-4.8.1-mysql.php
RUN chown www-data:www-data /var/www/html/public/adminer.php

# --- configure nginx
EXPOSE 8008

COPY <<nginxconf /etc/nginx/sites-available/active-collab
server {
	listen 8008 default_server;
	listen [::]:8008 default_server;
    server_name _;

    #access_log /var/log/nginx/activecollab.access.log;
    #error_log /var/log/nginx/activecollab.error.log;
    set \$root_path /var/www/html/public;
    root \$root_path;
    index index.html index.htm index.php router.php;
    charset utf-8;

    if (!-e \$request_filename) {
        rewrite ^/assets/(.*)\$ /assets/\$1 last;
        rewrite ^/avatars/(.*)\$ /avatars/\$1 last;
        rewrite ^/wallpapers/(.*)\$ /wallpapers/\$1 last;
        rewrite ^/verify-existence\$ /verify.php last;
        rewrite ^/proxy.php\$ /proxy.php last;
        rewrite ^/api/v([0-9]*)/(.*)\$ /api.php?path_info=\$2&api_version=\$1 last;
        rewrite ^\$ /router.php last;
        rewrite ^(.*) /router.php?path_info=\$1 last;
    }

    location / {
        rewrite ^/verify-existence\$ /verify.php last;
        rewrite ^/proxy.php\$ /proxy.php last;
        rewrite ^/api/v([0-9]*)/(.*)\$ /api.php?path_info=\$2&api_version=\$1 last;
        rewrite ^/\$ /router.php last;
        try_files \$uri \$uri/ /router.php?path_info=\$uri&\$args;
    }

    location ~ ^/(assets|avatars|wallpapers|adminer.php)/ {
        root \$root_path;
    }

    location ~* \.php\$ {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
}
nginxconf
RUN ln -s /etc/nginx/sites-available/active-collab /etc/nginx/sites-enabled/active-collab
RUN rm -f /etc/nginx/sites-enabled/default

# --- cleanup
RUN apt-get -y autoremove && apt-get -y clean

# --- start script
COPY <<eof /start.sh
#!/bin/bash

echo " * starting php-fpm..."
/etc/init.d/php8.3-fpm start

echo " * running nginx in foreground..."
nginx -g "daemon off;"
eof
RUN chmod +x /start.sh

CMD ["/start.sh"]
