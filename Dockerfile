FROM ubuntu:24.04

# --- install packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y python3 python3-venv python3-pip

WORKDIR /app
ADD AcDump /app/AcDump
ADD AcStorage /app/AcStorage
ADD ActiveCollabAPI /app/ActiveCollabAPI
ADD tests /app/tests

# create virtual environment
RUN python3 -m venv .venv

# add all requirements into the virtual environments
COPY requirements.txt /app/
RUN . .venv/bin/activate && pip3 install -r /app/requirements.txt

COPY acdump.sh /app/acdump.sh
RUN chmod +x /app/acdump.sh


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# docker run --rm -it active-collab-backup --help
ENTRYPOINT ["/app/acdump.sh"]

CMD ["/app/acdump.sh"]
