import streamlit as st
from PIL import Image
def main_con():
    c2 = st.container()
    c2.header("Contact")
    img = Image.open(r"D:\pic3.jpg")
    c2.image(img, width=1200)