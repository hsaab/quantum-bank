# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY . /usr/app

RUN npm install