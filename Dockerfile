FROM python:3.8-slim

#set the working directory in the conatiner
WORKDIR /usr/src/app

#copy the current directory contents into the container at usr/src/app
COPY App .
COPY requirements.txt .

#installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Setting the main app
ENV FLASK_APP=app.py

#Run the app.py file when the container launches
CMD ["python", "./app.py"]
