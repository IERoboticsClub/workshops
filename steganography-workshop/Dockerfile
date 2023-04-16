FROM python:3.9.16-slim

# Ref:
# https://docs.docker.com/engine/reference/builder/

# Copy the application's source code.
COPY demos /home/demo

# Pip install the required packages in the container
RUN ["/bin/bash", "-c", "pip install -r /home/demo/requirements.txt"]

#Set working directory
WORKDIR /home/demo

# Expose the port
EXPOSE 5555

# Run the uvicorn command
CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 5555 --reload"]