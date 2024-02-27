FROM python:slim
COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
CMD [ "python", "/app/main.py" ]
# CMD [ "tail", "-f", "/dev/null"]
