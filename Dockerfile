FROM circleci/python:3.6.8

COPY webapp/requirements*.txt /opt/bh/webapp/

WORKDIR /opt/bh

ARG GIT_TOKEN
ARG PIP_REQUIREMENTS

# Killian: I don't know why we need these? Commenting because they take a long time.
# RUN sudo apt-get update 
# RUN sudo apt-get install libxmlsec1-dev

# install Python modules needed by the Python app
RUN sudo pip install --upgrade pip
RUN pip install --no-cache-dir --no-warn-script-location -r /opt/bh/webapp/$PIP_REQUIREMENTS --user

COPY . /opt/bh/

# tell the port number the container should expose
EXPOSE 8100

# run the application
ENTRYPOINT ["python3"]
CMD /opt/bh/webapp/src/manage.py runserver 0.0.0.0:8100
