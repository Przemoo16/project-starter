FROM node:18-slim as build

WORKDIR /frontend

COPY ./frontend/package.json ./frontend/yarn.lock /frontend/
RUN yarn install --frozen-lockfile
COPY ./frontend/tsconfig.json ./frontend/tsconfig.node.json ./frontend/vite.config.ts /frontend/
COPY ./frontend/.babelrc ./frontend/jest.config.js ./frontend/jest.setup.ts /frontend/
COPY ./frontend/.eslintignore ./frontend/.eslintrc.json ./frontend/.prettierrc.json ./frontend/i18next-parser.config.js /frontend/
COPY ./frontend/index.html /frontend
COPY ./frontend/src /frontend/src
COPY ./frontend/public /frontend/public

RUN yarn build


FROM nginx:1.21.6

COPY --from=build /frontend/dist /var/www/html
COPY ./config/proxy/nginx.conf /var/nginx.conf
COPY ./config/proxy/init-config.sh /var/scripts/init-config.sh
COPY ./config/proxy/init-certs.sh /var/scripts/init-certs.sh
COPY ./config/scripts/nginx-template-subst.sh /var/scripts/nginx-template-subst.sh
COPY ./config/proxy/run.sh /var/scripts/run.sh
RUN chmod +x /var/scripts/init-config.sh /var/scripts/init-certs.sh /var/scripts/nginx-template-subst.sh /var/scripts/run.sh

CMD /var/scripts/run.sh
