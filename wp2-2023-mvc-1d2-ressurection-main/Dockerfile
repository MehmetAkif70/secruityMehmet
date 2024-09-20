# syntax=docker/dockerfile:1
FROM ubuntu:latest

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt



# final configuration
ENV FLASK_APP=website.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]