FROM python:3.6
RUN git clone https://github.com/sandeepdoodigani/jobportal-application.git
WORKDIR /jobportal-application
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ibm_db
EXPOSE 8080
CMD ["python","app.py"]
