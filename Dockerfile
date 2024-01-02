FROM python:3.9

WORKDIR /code

# Install system packages, including audio dependencies
RUN apt-get update && apt-get install -y \
    alsa-base alsa-utils && \
    apt-get clean

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["chainlit", "run", "app.py", "--port", "7860"]