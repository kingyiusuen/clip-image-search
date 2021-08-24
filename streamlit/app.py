import json

import requests

import streamlit as st


def search(query, input_type):
    headers = {
        "Content-type": "application/json",
        "x-api-key": st.secrets["api_key"],
    }
    data = json.dumps({"query": query, "input_type": input_type})
    response = requests.post(st.secrets["api_endpoint"], data=data, headers=headers)
    return response.json()


def display_results(response):
    print(response)
    if response["status_code"] != 200:
        st.error(response["message"])
        return

    cols = st.columns(2)
    for i, hit in enumerate(response["body"]):
        col_id = i % 2
        image_url = hit["_source"]["url"]
        cols[col_id].image(f"{image_url}?w=480")


def main():
    st.set_page_config(page_title="CLIP Image Search")

    input_type = st.sidebar.radio("Query by", ("text", "image"))
    if input_type == "text":
        query = st.sidebar.text_input("Enter text query here:")
    else:
        query = st.sidebar.text_input("Enter image URL here:")
    submit = st.sidebar.button("Submit")

    if not submit:
        st.title("Image Search")
    else:
        if not query:
            st.sidebar.error("Please enter a query.")
        else:
            if input_type == "image":
                st.sidebar.image(query)

            st.title("Search Results")
            with st.spinner("Wait for it..."):
                response = search(query, input_type)
            display_results(response)


if __name__ == "__main__":
    main()
