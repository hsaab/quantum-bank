# pull official base image
FROM node:16.10-alpine

# add `/Frontend/node_modules/.bin` to $PATH
ENV PATH /node_modules/.bin:$PATH

# install app dependencies
COPY /package.json ./
COPY /package-lock.json ./

RUN npm install

# add app
COPY . ./