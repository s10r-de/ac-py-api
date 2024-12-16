FROM ubuntu:24.04

# --- install packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade --no-install-recommends -y && \
  apt-get install -y \
  python3=3.12.3-0ubuntu2 \
  python3-venv=3.12.3-0ubuntu2 \
  python3-pip=24.0+dfsg-1ubuntu1.1

WORKDIR /app
COPY active_collab_app /app/active_collab_app
COPY active_collab_storage /app/active_collab_storage
COPY active_collab_api /app/active_collab_api
COPY css /app/css

# create virtual environment
RUN python3 -m venv .venv

# add all requirements into the virtual environments
COPY requirements.txt /app/
RUN . .venv/bin/activate && pip3 install --no-cache-dir -r /app/requirements.txt

COPY acdump.sh /app/acdump.sh
RUN chmod +x /app/acdump.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME /data
VOLUME /var/www/html/cache
VOLUME /var/www/html/logs
VOLUME /var/www/html/thumbnails
VOLUME /var/www/html/uploads
VOLUME /var/www/html/work
VOLUME /var/www/html/static-html

# docker run --rm -it active-collab-backup --help
ENTRYPOINT ["/app/acdump.sh"]

CMD ["/app/acdump.sh"]
