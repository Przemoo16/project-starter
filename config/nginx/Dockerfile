FROM nginx:1.23.2

COPY ./config/nginx/nginx.conf /var/nginx.conf

COPY ./config/scripts/nginx-template-subst.sh ./config/nginx/run.sh /var/scripts/
RUN chmod +x /var/scripts/nginx-template-subst.sh /var/scripts/run.sh

CMD ["/var/scripts/run.sh"]
