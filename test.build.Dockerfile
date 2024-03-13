# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY ./package.json /usr/app/package.json
COPY ./package-lock.json /usr/app/package-lock.json

RUN npm install -g react-scripts
RUN npm install -g react
RUN npm install -g react-dom
RUN npm install -g @testing-library/jest-dom
RUN npm install -g @testing-library/user-event
RUN npm install -g @testing-library/react
RUN npm install -g react-test-renderer