FROM amazoncorretto:8 as build-stage

RUN yum -y update
RUN yum -y install yum-utils
RUN yum -y groupinstall development

RUN yum list python3*
RUN yum -y install python3 python3-dev python3-pip python3-virtualenv git

RUN python -V
RUN python3 -V

ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3

RUN pip3 install --upgrade pip

RUN pip3 install pex pyspark==3.0.2 pandas tweepy

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN rm -rf dist

RUN pip3 freeze > requirements.txt

RUN pip3 install -r requirements.txt

RUN pex -r requirements.txt . -v --disable-cache -D twitter_ingestion/docs --ignore-errors -o twitter_ingestion.pex

RUN ./twitter_ingestion.pex -m twitter_ingestion.main --retrieveTweets run

FROM scratch AS result
COPY --from=build-stage /app/twitter_ingestion.pex .
COPY --from=build-stage /app/result/ .