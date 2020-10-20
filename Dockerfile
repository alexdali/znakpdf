FROM python:3.7

RUN apt-get update && \
	apt-get install libdmtx0b && \
	pip install fastapi uvicorn pylibdmtx numpy PyMuPDF Pillow python-multipart



EXPOSE 9990

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9990"]