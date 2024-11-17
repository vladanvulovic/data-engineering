FROM openjdk:8-jdk
RUN apt-get update && apt-get install -y python3 python3-pip
# Set the working directory in the container to /app
WORKDIR /job
# Add the current directory contents into the container at /app
ADD . /job
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD ["python3", "jsonl_processing_pipeline.py"]
