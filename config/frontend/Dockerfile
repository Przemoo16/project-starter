FROM node:18-slim

WORKDIR /frontend

COPY ./frontend/package.json ./frontend/yarn.lock /frontend/
RUN yarn install --frozen-lockfile
COPY ./frontend/tsconfig.json ./frontend/tsconfig.node.json ./frontend/vite.config.ts /frontend/
COPY ./frontend/.babelrc ./frontend/jest.config.ts ./frontend/jest.setup.ts /frontend/
COPY ./frontend/.eslintignore ./frontend/.eslintrc.json ./frontend/.prettierrc.json ./frontend/i18next-parser.config.js /frontend/
COPY ./frontend/index.html /frontend
COPY ./frontend/src /frontend/src
COPY ./frontend/public /frontend/public

CMD ["yarn", "dev"]
