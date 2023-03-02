FROM node:16.18

WORKDIR /frontend-react-js

COPY . /frontend-react-js/

RUN npm install

ENV PORT=3000

EXPOSE ${PORT}

CMD [ "npm", "start" ]