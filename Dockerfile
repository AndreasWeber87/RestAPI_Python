FROM python:3.11.4-alpine

# set Workdir inside the image
WORKDIR /home/ic20b050/app
# copy the current dir from the host in the image dir
ADD . /home/ic20b050/app

# install the libs from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# release the port to the host
EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
