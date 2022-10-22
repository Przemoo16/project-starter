FROM node:19-slim

RUN apt-get update && apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

ENV TERM=xterm

WORKDIR /e2e

COPY ./e2e/package.json ./e2e/yarn.lock ./e2e/tsconfig.json /e2e/
RUN yarn install --frozen-lockfile
COPY ./e2e/cypress.config.ts /e2e
COPY ./e2e/cypress /e2e/cypress

ENTRYPOINT yarn run cypress
