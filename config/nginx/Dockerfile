FROM nginx:1.21.6

COPY ./config/nginx/nginx.conf /var/nginx.conf

COPY ./config/nginx/nginx-template-subst.sh /bin/nginx-template-subst.sh
RUN chmod +x /bin/nginx-template-subst.sh

CMD /bin/bash -c "/bin/nginx-template-subst.sh && exec nginx -g 'daemon off;'"
