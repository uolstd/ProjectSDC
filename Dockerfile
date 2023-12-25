FROM python:3.9.5
WORKDIR /flask
COPY . /flask
ADD crudo.py .
EXPOSE 8501
EXPOSE 5000
RUN pip install transformers
RUN pip install youtube_transcript_api
RUN pip install flask
RUN pip install streamlit
RUN pip install tensorflow
CMD ["python", "./crudo.py"]