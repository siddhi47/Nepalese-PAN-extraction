FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:alex-p/tesseract-ocr-devel

RUN apt-get update -y                                           && \
    apt-get install -y python python-dev build-essential        && \
    apt-get install default-libmysqlclient-dev -y               && \
    apt install -y libsm6 libxext6                              && \
    apt-get install ffmpeg   -y                                 && \
    apt-get install -y python3-dev                              && \
    apt-get -y install tesseract-ocr                            && \
    apt install python3-pip -y                                  && \
    apt install libgl1-mesa-glx                                 && \
    apt install -y wget

RUN apt install tesseract-ocr-nep

COPY . /app

WORKDIR /app

RUN pip3 install pillow                                          && \
    pip3 install pytesseract                                     && \
    pip3 install opencv-python                                   && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3","."]