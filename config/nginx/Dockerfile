FROM nginx:1.21.6

COPY ./config/nginx/nginx.conf /var/nginx.conf

COPY ./config/scripts/nginx-template-subst.sh /scripts/nginx-template-subst.sh
COPY ./config/nginx/run.sh /scripts/run.sh
RUN chmod +x /scripts/nginx-template-subst.sh /scripts/run.sh

CMD /scripts/run.sh
