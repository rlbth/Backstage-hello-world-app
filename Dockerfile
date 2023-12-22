FROM python:3.8-slim

#set the working directory in the conatiner
WORKDIR /usr/src/app

#copy the current directory contents into the container at usr/src/app
COPY App .

#Run the app.py file when the container launches
CMD ["python", "./app.py"]