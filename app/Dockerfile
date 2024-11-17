FROM openjdk:8-jdk
RUN apt-get update && apt-get install -y python3 python3-pip
# Set the working directory in the container to /app
WORKDIR /app
# Add the current directory contents into the container at /app
ADD . /app
RUN pip3 install --no-cache-dir -r requirements.txt
# Set the PYTHONPATH to the app directory
ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD ["python3", "run.py"]
