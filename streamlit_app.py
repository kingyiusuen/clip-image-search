import json

import requests
import streamlit as st

import clip_image_search.utils as utils


intro = """
The database contains 25,000 images from the Unsplash Dataset. You can either

- search them using a natural language description (e.g., animals in jungle), or
- find similar images by providing an image URL (e.g. https://i.imgur.com/KRNOn22.jpeg).

The algorithm will return the ten most relevant images.
"""


def handle_query(query, input_type, max_attempts=3):
    if not query:
        st.sidebar.error("Please enter a query.")
        return

    if input_type == "image":
        st.sidebar.image(query)

    for i in range(max_attempts):
        if i == 0:
            message = "Wait for it..."
        else:
            message = "The server needs some time to warm up..."
        with st.spinner(message):
            response = make_post_request(query, input_type)
            if response.status_code != 503:
                break

    display_results(response)


def make_post_request(query, input_type):
    headers = {
        "Content-type": "application/json",
        "x-api-key": st.secrets["api_key"],
    }
    data = json.dumps({"query": query, "input_type": input_type})
    response = requests.post(st.secrets["api_endpoint"], data=data, headers=headers)
    return response


def display_results(response):
    response = response.json()
    if response.get("status_code") != 200:
        st.error(response["message"])
        return

    cols = st.columns(2)
    col_heights = [0, 0]
    for hit in response["body"]:
        image_url = hit["_source"]["url"]
        image = utils.load_image_from_url(f"{image_url}?w=360")
        col_id = 0 if col_heights[0] <= col_heights[1] else 1
        cols[col_id].image(image)
        col_heights[col_id] += image.height


def main():
    st.set_page_config(page_title="Image Search Engine")

    input_type = st.sidebar.radio("Query by", ("text", "image"))
    query = st.sidebar.text_input("Enter text/image URL here:")
    submit = st.sidebar.button("Submit")

    st.title("Image Search Engine")
    if submit:
        handle_query(query, input_type)
    else:
        st.write(intro)


if __name__ == "__main__":
    main()
