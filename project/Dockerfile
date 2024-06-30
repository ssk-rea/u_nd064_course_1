FROM python:3.8
LABEL maintainer="Shree K"

ADD ./techtrends/requirements.txt .
RUN pip install -r requirements.txt

COPY ./techtrends/ /app
WORKDIR /app

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
