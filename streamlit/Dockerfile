# running python version
FROM python:3.10-slim

# set a directory for the app
WORKDIR /home

# copy all the files to the container
COPY . .

# install dependencies
RUN \
pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 8501

# run the command
CMD ["streamlit", "run", "credit-streamlit.py"]