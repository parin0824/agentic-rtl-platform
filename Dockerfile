FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv make verilator yosys gtkwave git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .
RUN python3 -m pip install --break-system-packages -e '.[dev,verification,mcp]'
CMD ["pytest", "-q"]
