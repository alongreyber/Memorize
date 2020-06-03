FROM python:3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        festival \
        espeak-ng \
        git && \
    apt-get clean

# Pytest needs to be installed through pip to make sure we have a recent version
RUN pip3 install pytest pytest-cov

# install phonemizer and run the tests
RUN git clone https://github.com/bootphon/phonemizer.git && \
    cd phonemizer && \
    python setup.py install && \
    phonemize --version
# RUN python -m pytest -v test

RUN git clone https://github.com/dmort27/panphon && \
    cd panphon && \
    python setup.py install

WORKDIR /app
CMD ["python", "main.py"]
