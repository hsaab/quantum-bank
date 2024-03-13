# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY ./package.json /usr/app/package.json
COPY ./package-lock.json /usr/app/package-lock.json

RUN npm install react-scripts
RUN npm install react
RUN npm install react-dom
RUN npm install @testing-library/jest-dom
RUN npm install @testing-library/user-event
RUN npm install testing-library/react
RUN npm install react-test-renderer