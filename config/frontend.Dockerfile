FROM node:17-slim

COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/tsconfig.json /frontend/
WORKDIR /frontend
RUN yarn install --frozen-lockfile
COPY ./frontend/i18next-parser.config.js /frontend
COPY ./frontend/src /frontend/src
COPY ./frontend/public /frontend/public

CMD yarn start
