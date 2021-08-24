import logging
import time

import clip_image_search.utils as utils
from clip_image_search import CLIPFeatureExtractor, Searcher


logger = logging.getLogger()
logger.setLevel(logging.INFO)

feature_extractor = CLIPFeatureExtractor()
searcher = Searcher()


def lambda_handler(event, context):
    try:
        input_type = event["input_type"]
        if input_type == "text":
            text = event["query"]
            query_features = feature_extractor.get_text_features(text)
        elif input_type == "image":
            image_url = event["query"]
            image = utils.load_image_from_url(image_url)
            query_features = feature_extractor.get_image_features(image)
        else:
            raise ValueError(f"Unrecognized input type: {input_type}")
    except Exception as e:
        logger.error(e)
        return {
            "status_code": 400,
            "message": "Error when processing input.",
        }

    try:
        start = time.time()
        response = searcher.knn_search(query_features[0])
        end = time.time()
        time_elapsed = end - start
        logger.info(f"Search completed in {time_elapsed}s.")
        results = response["hits"]["hits"]
        return {
            "status_code": 200,
            "message": "Success",
            "body": results,
        }
    except Exception as e:
        logger.error(e)
        return {
            "status_code": 500,
            "message": "Search engine error.",
        }
