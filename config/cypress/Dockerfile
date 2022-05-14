FROM cypress/included:9.5.4

RUN yarn global add wait-on

COPY ./config/cypress/run.sh /scripts/run.sh
RUN chmod +x /scripts/run.sh

CMD /scripts/run.sh
ENTRYPOINT []
