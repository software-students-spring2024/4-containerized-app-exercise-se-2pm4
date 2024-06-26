FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    pkg-config \
    libhdf5-dev \
    gcc

# Set the working directory in the image
WORKDIR /app

# Create the upload folder and set permissions
RUN mkdir -p static/uploads && chmod 777 static/uploads

# install dependencies into the image - doing this first will speed up subsequent builds, as Docker will cache this step
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .

# expose the port that the Flask app is running on... by default 5000
EXPOSE 3000

# Run app.py when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]