# Stage 1: Build Backend
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder
WORKDIR /flare-ai-rag
COPY pyproject.toml README.md ./
COPY src ./src
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install -e . && \
    rm -rf /root/.cache/uv

# Stage 2: Final Image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app

# Install OS-level dependencies and Qdrant in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        tar \
        curl \
    && wget https://github.com/qdrant/qdrant/releases/download/v1.13.4/qdrant-x86_64-unknown-linux-musl.tar.gz \
    && tar -xzf qdrant-x86_64-unknown-linux-musl.tar.gz \
    && mv qdrant /usr/local/bin/ \
    && rm qdrant-x86_64-unknown-linux-musl.tar.gz \
    && apt-get purge -y wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary files from builder
COPY --from=backend-builder /flare-ai-rag/.venv ./.venv
COPY --from=backend-builder /flare-ai-rag/src ./src
COPY --from=backend-builder /flare-ai-rag/pyproject.toml ./
COPY --from=backend-builder /flare-ai-rag/README.md ./

# Set labels and entrypoint
LABEL "tee.launch_policy.allow_env_override"="OPEN_ROUTER_API_KEY" \
      "tee.launch_policy.log_redirect"="always"

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]