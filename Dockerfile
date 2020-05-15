FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc g++

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN pip3 install os
#RUN pip3 install sys

COPY . /app

#ADD download_data.py ../src/download_data.py 
#ADD upload_data.py ../src/upload_data.py
#ADD sql/db_create.py ../src/sql/db_create.py

EXPOSE 5000

#CMD ["../src/download_data.py","../src/upload_data.py", "../src/sql/db_create.py"]
#ENTRYPOINT ["python3"]
