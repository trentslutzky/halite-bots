FROM python:3.11
RUN mkdir /opt/app
COPY Trent.py /opt/app
CMD ["python", "/opt/app/Trent.py"]
