# ==============================================================================
# SemanticFlow Enterprise Cloud Container
# Multi-Stage Distroless / Ultra-Slim Minimal OCI Image
# ==============================================================================

# Stage 1: Build virtual environment and wheels
FROM python:3.12-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install build dependencies
COPY pyproject.toml .
COPY src/ src/

# Create isolated site-packages directory
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefix=/install .

# Stage 2: Distroless Minimal Non-Root Runtime
FROM gcr.io/distroless/python3-debian12:nonroot AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/install/lib/python3.12/site-packages \
    PATH="/install/bin:${PATH}"

WORKDIR /workspace

# Copy installed site-packages and entrypoint from builder
COPY --from=builder /install /install
COPY --from=builder /build/src /app/src

# Set non-root user (UID 65532)
USER nonroot:nonroot

# Default entrypoint executing semanticflow CLI
ENTRYPOINT ["python3", "-m", "src.cli"]
CMD ["--help"]
