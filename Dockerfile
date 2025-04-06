FROM python:3.11-slim

# Install curl for UV installation
RUN apt-get update && apt-get install -y curl

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

# Install dependencies
RUN uv sync

CMD ["uv", "run", "task", "fr"]