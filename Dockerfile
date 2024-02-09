FROM python:slim
COPY . /app
RUN pip install -r /app/requirements.txt
# CMD [ "tail", "-f", "/dev/null"]
WORKDIR /app
CMD [ "python", "/app/main.py" ]
