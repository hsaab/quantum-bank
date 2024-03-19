# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY ./frontend/package.json /usr/app/package.json
COPY ./frontend/package-lock.json /usr/app/package-lock.json

RUN npm install -g react-scripts
RUN npm install

COPY ./frontend .

CMD ["npm","start"]