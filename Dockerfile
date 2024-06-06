FROM python:3.9-slim

WORKDIR /build

RUN mkdir -p /app/tdlib/natives/linux

RUN apt-get update && apt-get install -y \
    make git zlib1g-dev libssl-dev gperf php-cli cmake g++ \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/tdlib/td.git \
    && cd td \
    && rm -rf build \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/app/tdlib/natives/linux .. \
    && cmake --build . --target install

COPY . /app

RUN pip install /app/requirements.txt

CMD ["python3", "/app/main.py"]