FROM node:18-slim as build

COPY ./frontend/package.json ./frontend/yarn.lock ./frontend/tsconfig.json /frontend/
WORKDIR /frontend
RUN yarn install --frozen-lockfile
COPY ./frontend/.eslintignore ./frontend/.eslintrc.json ./frontend/.prettierrc.json /frontend/
COPY ./frontend/i18next-parser.config.js /frontend
COPY ./frontend/src /frontend/src
COPY ./frontend/public /frontend/public

RUN yarn build


FROM nginx:1.21.6

COPY --from=build /frontend/build /var/www/html
COPY ./config/proxy/nginx.conf /var/nginx.conf
COPY ./config/proxy/init-config.sh /scripts/init-config.sh
COPY ./config/proxy/init-certs.sh /scripts/init-certs.sh
COPY ./config/scripts/nginx-template-subst.sh /scripts/nginx-template-subst.sh
COPY ./config/proxy/run.sh /scripts/run.sh
RUN chmod +x /scripts/init-config.sh /scripts/init-certs.sh /scripts/nginx-template-subst.sh /scripts/run.sh

CMD /scripts/run.sh
