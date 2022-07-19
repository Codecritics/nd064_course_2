FROM python:3.8

WORKDIR .

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN python -m grpc_tools.protoc -I./app/ --python_out=./app/ --grpc_python_out=./app/ location.proto

EXPOSE 5005

CMD ["python", "app/main.py"]