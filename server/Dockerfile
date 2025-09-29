FROM python:3.12-slim AS builder

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY server/ ./server
COPY src/ ./src
COPY models/ ./models
COPY data/ ./data
COPY config/ ./config

RUN python -m venv ./venv
ENV PATH="/backend/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install --no-cache-dir -r server/requirements.txt


FROM python:3.12-slim

WORKDIR /backend

COPY --from=builder /backend/venv ./venv
COPY --from=builder /backend/server ./server
COPY --from=builder /backend/src ./src
COPY --from=builder /backend/models ./models
COPY --from=builder /backend/data ./data
COPY --from=builder /backend/config ./config

ENV PATH="/backend/venv/bin:$PATH"
ENV APP_ENV=prod

RUN mkdir -p /backend/logs

ENTRYPOINT ["/bin/bash", "/backend/server/server-entrypoint.sh"]