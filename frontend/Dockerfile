# pull official base image
FROM --platform=linux/amd64 node:16.17.1-alpine3.16 as build

WORKDIR /usr/app
COPY . /usr/app
RUN npm ci
RUN npm run build

FROM --platform=linux/amd64 nginx:1.23.1-alpine
EXPOSE 80
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/app/build /usr/share/nginx/html