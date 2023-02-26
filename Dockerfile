FROM python:3

WORKDIR /home/ic20b050/app
ADD . /home/ic20b050/app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]