import streamlit as st
from PIL import Image
def main_abt():
    c2 = st.container()
    c2.header("About Us")
    img=Image.open(r"D:\abtus.jpg")
    c2.image(img,width=1200)

    img2=Image.open(r"D:\pic1.jpg")
    c2.image(img2,width=1200)

    img3 = Image.open(r"D:\pic2.jpg")
    c2.image(img3, width=1200)

    c2.markdown("""
        <style>
        .big-font {
            font-size:22px !important;
            text-align: justify;
            font-family: Georgia, serif ;
        }

        </style>
        """, unsafe_allow_html=True)

    c2.markdown(
        '<p class="big-font">  </p>', unsafe_allow_html=True)

