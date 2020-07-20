# Define a source image
FROM python:stretch

# Set up app dir
COPY . /app
WORKDIR /app

# Install pip and needed Python packages
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]