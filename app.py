import streamlit as st
import re
import requests

def get_address():
    url = st.text_input("Site to scrape:")
    return url.strip()

def parse_address(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            addys = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', html)
            st.write(addys)
        else:
            st.write(f"Cannot retrieve URL: HTTP Error Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"Cannot retrieve URL: {str(e)}")

def main():
    st.title("Email Scraper")
    url = get_address()
    if url:
        parse_address(url)

if __name__ == "__main__":
    main()
