FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y python3-pip python3-dev git gcc g++

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

RUN chmod +x ../app/boot.sh
ADD download_data.py /
ADD upload_data.py /
ADD sql/db_create.py /

EXPOSE 5000

CMD ["python3","download_data.py","upload_data.py", "sql/db_create.py"]
