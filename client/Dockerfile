FROM python:3.12-slim AS builder
WORKDIR /client

RUN apt-get update && apt-get install -y --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY client/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY client/ .

FROM python:3.12-slim
WORKDIR /client

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /install /usr/local
COPY --from=builder /client .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]