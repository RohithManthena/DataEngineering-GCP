FROM python:3.9-slim

COPY publishToPubSub.py /publishToPubSub.py
COPY requirements.txt /requirements.txt
COPY gcpServiceAccountkey.json /gcpServiceAccountkey.json
WORKDIR /
RUN pip install -r requirements.txt
CMD [ "python", "publishToPubSub.py" ]

