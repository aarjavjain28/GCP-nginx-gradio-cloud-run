#
## Stage 1: Build the Go application
#FROM golang:1.17 as builder
#
#RUN apt-get update && apt-get install -y git
#
## Set the Current Working Directory inside the container
#WORKDIR /app
#
## Clone the Vouch Proxy
#RUN git clone https://github.com/vouch/vouch-proxy.git .
#
## Build the Go app
#RUN GO111MODULE=on go build
#
#
#
#FROM python:3.9-slim
#
## Install nginx and supervisord from debian repos
#RUN apt-get update && \
#    apt-get install -y nginx supervisor gettext-base net-tools && \
#    apt-get install -y curl && \
#    rm -rf /var/lib/apt/lists/*
#
#WORKDIR /app
#
## Copy the Vouch Proxy binary from the builder stage
#COPY --from=builder /app/vouch-proxy /app
#
##RUN curl -L https://github.com/vouch/vouch-proxy/releases/download/v0.35.1/vouch-proxy_linux_amd64.tar.gz -o vouch-proxy_linux_amd64.tar.gz && \
##    tar -zxvf vouch-proxy_linux_amd64.tar.gz -C / && \
##    rm vouch-proxy_linux_amd64.tar.gz
##
### Install Vouch Proxy
##RUN curl -L https://github.com/vouch/vouch-proxy/releases/download/v0.35.1/vouch-proxy_linux_amd64.tar.gz -o vouch-proxy_linux_amd64.tar.gz && \
##    tar -zxvf vouch-proxy_linux_amd64.tar.gz -C / && \
##    rm vouch-proxy_linux_amd64.tar.gz
#
#
## Define build arg and environment variable for client secret
##ARG MY_SECRET
##ENV VOUCH_CLIENTSECRET=$MY_SECRET
#
## Install Python dependencies
#COPY requirements.txt /app/
#RUN pip install --no-cache-dir -r /app/requirements.txt
#
## Copy application, NGINX, Vouch and Supervisor configuration files
#COPY app/app.py /app/
#COPY nginx.conf /etc/nginx/nginx.conf
#COPY vouch-config.yml /app/config/config.yml
#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#
#EXPOSE 8080
#
##CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/nginx.conf > /tmp/nginx.conf && mv /tmp/nginx.conf /etc/nginx/nginx.conf && exec /usr/bin/supervisord"
#
#CMD ["/usr/bin/supervisord"]
#
#
## command to build image:
## podman build --build-arg MY_SECRET=mysecret -t my-vouch-proxy .




# Stage 1: Build the Go application
FROM golang:1.17 as builder

RUN apt-get update && apt-get install -y git

# Set the Current Working Directory inside the container
WORKDIR /app

# Clone the Vouch Proxy
RUN git clone https://github.com/vouch/vouch-proxy.git .

# Build the Go app
RUN GO111MODULE=on go build

FROM python:3.9-slim

# Install nginx, supervisor and envsubst from debian repos
RUN apt-get update && \
    apt-get install -y nginx supervisor gettext-base curl  net-tools&& \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the Vouch Proxy binary from the builder stage
COPY --from=builder /app/vouch-proxy /app

# Define build arg and environment variable for client secret


# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application, NGINX, Vouch and Supervisor configuration files
COPY app/app.py /app/
COPY nginx.conf /etc/nginx/nginx.conf
#COPY vouch-config.yml /app/config/config.yml
COPY vouch-config.yml /app/config/config.template.yml
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/nginx.conf > /tmp/nginx.conf && mv /tmp/nginx.conf /etc/nginx/nginx.conf && exec /usr/bin/supervisord"
CMD /bin/bash -c "envsubst < /app/config/config.template.yml > /app/config/config.yml && envsubst '\$PORT' < /etc/nginx/nginx.conf > /tmp/nginx.conf && mv /tmp/nginx.conf /etc/nginx/nginx.conf && exec /usr/bin/supervisord"

# && exec netstat -tuln && exec curl http://127.0.0.1:7860"
#exec /usr/bin/supervisord"  #
# build and run locally:
# build using podman build -t my-vouch-proxy .
# run using   podman run  -e OAUTH_CLIENT_ID= id  -e OAUTH_CLIENT_SECRET= secret -e PORT=8080  -p 8080:8080 -p 7860:7860 -p 9090:9090 my-vouch-proxy