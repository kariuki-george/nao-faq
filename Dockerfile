FROM python:3.9



RUN pip3 install scikit-learn


ADD . . 

CMD ["python3", "./main.py"]
