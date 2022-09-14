FROM python:3.10.0-alpine3.14

WORKDIR /~

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./nutanix-prometheus-exporter.py" ]
