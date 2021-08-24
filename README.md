# Image Search using CLIP

Retrieve images based on a query (text or image), using Open AI's pretrained CLIP model.

## How to Use

### Download the Unsplash dataset

```
python scripts/download_unsplash.py --image_width=480 --threads_count=32
```

This will download and extract a zip file that contains the metadata about the photos in the dataset. The script will use the URLs of the photos to download the actual images to `unsplash-dataset/photos`. The download may fail for a few images (see [this issue](https://github.com/unsplash/datasets/issues/37#issuecomment-854711074)). Since CLIP will downsample the images to 224 x 224 anyway, you may want to adjust the width of the downloaded images to reduce storage space. You may also want to increase the `threads_count` parameter to achieve a faster performance.

### Setup an Elasticsearch service in AWS

Download [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html).

Then, configure your security credentials.

```
aws configure
```

Search Elasticsearch Service in AWS Console.

### Create index and upload image feature vectors to Elasticsearch

```
python scripts/ingest_data.py
```

The script will download the pretrained CLIP model and process the images by batch. It will use GPU if there is one. The images will be stored in the following format:

```
image_id: {"url": https://abc.com/xyz, "feature_vector": [0.1, 0.3, ..., 0.2]}
```

### Build Docker image

Log in to Amazon ECR public registry, so that Docker can pull an AWS base image.

```
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

Build Docker image.

```
docker build --build-arg AWS_ACCOUNT_ID=YOUR_AWS_ACCOUNT_ID \
             --build-arg AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID \
             --build-arg AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY \
             --tag clip-image-search \
             --file server/Dockerfile .
```

Run the Docker image as a container.

```
docker run -p 9000:8080 -it --rm clip-image-search
```

Test the container with a POST request.

```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"query": "two dogs", "input_type": "text"}'
```

### AWS Lambda Function

Increase the memory size to 1024MB

Ensure your lambda function has the permission to access parameter store