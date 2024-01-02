FROM python:3.9.14-slim

RUN mkdir -p /dagster_home /user_code

RUN pip install dagster-webserver dagster-postgres dagster-aws

# Copy your code and workspace to /opt/dagster/app
COPY . /user_code/

ENV DAGSTER_HOME=/dagster_home/

WORKDIR /user_code

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]