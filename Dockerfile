FROM python:2.7-alpine

# Update
RUN apk add --update python py-pip

# Install app dependencies
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt

# Bundle app source
# COPY server.py /src/server.py

EXPOSE  3000
CMD ["python", "-u", "/src/server.py"]
