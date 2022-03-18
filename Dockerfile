FROM python:3.8.1

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8000
WORKDIR /app

COPY . ./
RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]