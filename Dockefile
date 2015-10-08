FROM java:7

# Update packages
RUN apt-get update -y

# Install Python Setuptools
RUN apt-get install -y python-setuptools git

# Install pip
RUN easy_install pip

# Bundle app source
ADD . /src
WORKDIR /src

# Add and install Python modules
RUN pip install -r requirements.txt

# Expose
EXPOSE  5000

# Run
CMD ["python", "entry.py"]