FROM python:3.9.14-slim

RUN mkdir -p /dagster_home /user_code

# Copy your code and workspace to /opt/dagster/app
COPY . /user_code/

RUN cd /user_code/ && pip install -e .

ENV DAGSTER_HOME=/dagster_home/

WORKDIR /user_code/

EXPOSE 3000

ENTRYPOINT ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]