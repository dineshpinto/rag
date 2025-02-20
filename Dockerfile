# Stage 1: Build Backend
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder
WORKDIR /flare-ai-rag
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Stage 2: Final Image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
# Install OS-level dependencies needed for Qdrant
RUN apt-get update && \
    apt-get install -y \
    wget \
    tar \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=backend-builder /flare-ai-rag/.venv ./.venv
COPY --from=backend-builder /flare-ai-rag/src ./src
COPY --from=backend-builder /flare-ai-rag/pyproject.toml .
COPY --from=backend-builder /flare-ai-rag/README.md .

# Download and install Qdrant binary
RUN wget https://github.com/qdrant/qdrant/releases/download/v1.13.4/qdrant-x86_64-unknown-linux-musl.tar.gz && \
    tar -xzf qdrant-x86_64-unknown-linux-musl.tar.gz && \
    mv qdrant /usr/local/bin/ && \
    rm qdrant-x86_64-unknown-linux-musl.tar.gz

# Allow workload operator to override environment variables
LABEL "tee.launch_policy.allow_env_override"="OPEN_ROUTER_API_KEY"
LABEL "tee.launch_policy.log_redirect"="always"

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]