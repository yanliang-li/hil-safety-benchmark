FROM node:22-bookworm-slim

ARG CLAUDE_CODE_VERSION=2.1.220
ARG CODEX_VERSION=0.144.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/hilbench-venv
ENV PATH="/opt/hilbench-venv/bin:${PATH}"

WORKDIR /opt/hilbench-src
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN npm install --global "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}"
RUN npm install --global "@openai/codex@${CODEX_VERSION}"

RUN useradd --create-home --uid 10001 benchmark
WORKDIR /bench
COPY --chown=benchmark:benchmark data ./data
COPY --chown=benchmark:benchmark docs ./docs
COPY --chmod=755 docker/pilot/entrypoint.sh /usr/local/bin/hilbench-entrypoint
RUN mkdir -p /bench/runs && chown benchmark:benchmark /bench/runs

USER benchmark
ENTRYPOINT ["/usr/local/bin/hilbench-entrypoint"]
CMD ["--help"]

