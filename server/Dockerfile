FROM public.ecr.aws/lambda/python:3.8

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG MODEL_DIR=./models
RUN mkdir $MODEL_DIR

ENV TRANSFORMERS_CACHE=$MODEL_DIR \
    TRANSFORMERS_VERBOSITY=error

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

COPY clip_image_search clip_image_search
COPY server/requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir -f https://download.pytorch.org/whl/torch_stable.html

COPY server/lambda_function.py lambda_function.py
RUN python lambda_function.py
RUN chmod -R 0755 $MODEL_DIR

CMD ["lambda_function.lambda_handler"]