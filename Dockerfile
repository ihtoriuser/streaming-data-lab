FROM flink:1.17-java11

# Install Python 3.10 and pip
RUN apt-get update -y && \
    apt-get install -y python3.10 python3-pip python3.10-dev && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Install PyFlink
RUN pip install apache-flink==1.17.1 -r requirements-local.txt
