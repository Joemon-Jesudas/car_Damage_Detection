import streamlit as st
from PIL import Image
def main_how():
    c=st.container()
    c.header("How it works")

    c.markdown("""
    <style>
    .big-font {
        font-size:22px !important;
        text-align: justify;
        font-family: Georgia, serif ;
    }

    </style>
    """, unsafe_allow_html=True)

    c.markdown('<p class="big-font"> The Car Damage Recognition system is a set of ML algorithms with an API that utilizes '
                'computer vision. Based on deep learning, the algorithms automatically detect a'
                'vehicles body and analyze the extent of the damage. Automatic car damage detection in the insurance industry can be used to'
                'devise the claim process for faster processing with an advanced level of accuracy.'
                'The use of AI in insurance claims is only possible if the model is well-trained with annotated damaged cars'
                ' with a huge amount and variety of training data sets. This is to detect the level of damage for accurate claims.'
                'This web app provides training data for AI in insurance with precisely annotated images of different types of damaged vehicles'
                'that help Computer Vision to train the machine learning algorithms. </p>', unsafe_allow_html=True)

    image = Image.open("D:\cd.jpg")
    c.image(image)