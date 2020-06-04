FROM python:3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        festival \
        espeak-ng \
        git && \
    apt-get clean

# Pytest needs to be installed through pip to make sure we have a recent version
WORKDIR /app
COPY requirements.txt .
RUN pip install numpy
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
