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

EXPOSE 3005  # Add this line with your app's port

CMD ["uv", "run", "task", "fr"]