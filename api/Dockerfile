FROM python:3.10-slim as application


ARG TARGETARCH
ARG GOOGLE_RE2_VERSION="0.2.20220601"
ARG TARGETPLATFORM

RUN if [ "${TARGETARCH}" != "amd64" ]; then apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*; fi;
RUN pip install google-re2==${GOOGLE_RE2_VERSION}

WORKDIR /app
COPY . .

RUN apt update && apt install -y xmlsec1
RUN pip install -r requirements.txt --no-cache-dir --compile
RUN python manage.py collectstatic --no-input

ENV DJANGO_SETTINGS_MODULE=app.settings.production

EXPOSE 8000
USER nobody

ENTRYPOINT ["./scripts/run-docker.sh"]
CMD ["migrate-and-serve"]
