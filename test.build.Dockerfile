# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY ./package.json /usr/app/package.json
COPY ./package-lock.json /usr/app/package-lock.json

RUN npm install

COPY . .

CMD ["npm","start"]