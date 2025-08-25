FROM public.ecr.aws/lambda/python:3.12

# Copy dependencies first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Set CMD to your handler function (file.function_name)
CMD ["app.handler"]
