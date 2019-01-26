FROM nginx
ENV TZ=America/Los_Angeles

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yqq update && apt-get -yqq install curl

ADD healthcheck.sh /
ADD conf /etc/nginx
