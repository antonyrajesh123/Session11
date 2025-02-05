# Use official Python 3.10 image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Create the cache directory and ensure it's writable
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Install dependencies
RUN pip install --no-cache-dir gradio tokenizers huggingface_hub transformers

# Expose port for Gradio
EXPOSE 7860

# Run the Gradio app
CMD ["python", "app.py"]