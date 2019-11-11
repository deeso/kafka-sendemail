FROM python:3.7-slim

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential apt-utils git \
    && apt-get install -y --no-install-recommends libmagic-dev libpython3-dev



ENV PIP_FORMAT=legacy
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get install -y netcat && apt-get -y autoremove

# Create unprivileged user
RUN adduser --disabled-password --gecos '' kafkaemail

WORKDIR kafka-sendemail

COPY . kafka-sendemail
RUN pip3 install -e kafka-sendemail


COPY ./internal/config.toml .
COPY wait_for_services.sh .
COPY run.sh .
COPY main.py .

RUN chmod a+x wait_for_services.sh run.sh

ENTRYPOINT ["sh", "wait_for_services.sh"]
CMD [ "./run.sh" ]
