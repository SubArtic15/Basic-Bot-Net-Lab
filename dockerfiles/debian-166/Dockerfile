# use the basic debian container
FROM debian:latest

# update container and install ssh
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y openssh-server

# create new user with a temporary password
RUN useradd -ms /bin/bash sys-admin
RUN echo "sys-admin:oksana" | chpasswd
