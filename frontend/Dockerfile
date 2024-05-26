FROM node:22

EXPOSE 3000

WORKDIR /usr/hackithon2024

COPY ./ ./

RUN npm install

RUN npm run build

CMD [ "npm", "start" ]