FROM node:alpine
RUN apk update
RUN apk upgrade
RUN apk add ca-certificates && update-ca-certificates
RUN apk add --no-cache --update \
    curl \
    unzip \
    bash \
    git

RUN rm /var/cache/apk/*

RUN mkdir -p /var/task
VOLUME /var/task
WORKDIR /var/task
COPY . /var

COPY ./2-build.sh /usr/local/bin
RUN chmod a+x /usr/local/bin/2-build.sh \
  && ln -s /usr/local/bin/2-build.sh / # Needed for backwards compatability
# TODO: Speed up
# WHY: Too slow, takes over an hour
# WHEN: We need the build to be dockerised
ENTRYPOINT ["2-build.sh", "/var/task"]  
ENV NODE_PATH=/var
EXPOSE 3000

