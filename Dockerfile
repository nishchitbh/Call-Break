
FROM python:3.10-slim

ADD ./app_new.py .
ADD ./Cards.py .
ADD ./training.py .
ADD ./Logic.py .
ADD ./dataset1.py .
ADD ./requirements.txt .
#RUN apk add py3-numpy py3-pandas py3-scikit-learn
# RUN apk add build-base
#RUN conda install numpy==1.14.3
RUN pip3 install -r requirements.txt
#RUN pip3 install pandas==0.23.0rc2
#RUN pip3 install scikit-learn==0.19.1

EXPOSE 7000

CMD ["python3", "app_new.py"]
