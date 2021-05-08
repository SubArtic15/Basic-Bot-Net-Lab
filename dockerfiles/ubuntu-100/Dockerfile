# use the basic ubuntu container
FROM ubuntu:latest

# update container and install ssh
RUN apt-get update
RUN apt-get install -y ssh
RUN apt-get install -y openssh-server

# create new user with a temporary password
RUN useradd -ms /bin/bash puppet
RUN echo "puppet:abc123" | chpasswd
