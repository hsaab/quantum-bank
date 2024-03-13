# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .