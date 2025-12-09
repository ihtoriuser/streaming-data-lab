# flink/Dockerfile

FROM flink:1.17-java11

# Install Python and PyFlink
RUN apt-get update -y && \
    apt-get install -y python3.10 python3-pip python3.10-dev && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    pip install --no-cache-dir apache-flink==1.17.1

