FROM node:18-slim

WORKDIR /frontend

COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/tsconfig.json /frontend/
RUN yarn install --frozen-lockfile
COPY ./frontend/.eslintignore ./frontend/.eslintrc.json ./frontend/.prettierrc.json ./frontend/i18next-parser.config.js /frontend/
COPY ./frontend/src /frontend/src
COPY ./frontend/public /frontend/public

CMD yarn start
