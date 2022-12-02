import glob
import pandas as pd
import os
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import joblib
from regress_predit import predictr
from model import predict
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from PIL import  Image
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from about import main_abt
from contact import main_con
from howit import main_how

st.set_page_config(page_title="Car Damage detection",page_icon=":car:",layout="wide")
feature_cols=joblib.load("features.joblib")



#adding allianz logo to the side bar
with st.sidebar.container():
    logo=Image.open(r"D:\Front end\logo.jpeg")
    st.image(logo,use_column_width=True)

#hiding menu bar and watermark of streamlit
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



#Removing white space on top of the screen
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


# set sidebar width
st.markdown(
"""
<style>
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 300px;
}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    width: 300px;
    margin-left: -300px;
}
</style>
""",
unsafe_allow_html=True,
)



#create navigation buttons
with st.sidebar:
    selected = option_menu("Main Menu", ["HOME","HOW IT WORK" ,'ABOUT US','CONTACT'],
        icons=['house','info-circle','person-bounding-box', 'telephone-inbound'], menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "blue", "font-size": "15px"},
            "nav-link": {"font-size": "10px", "text-align": "left", "margin": "1px", "--hover-color": "#78fff8"},
            "nav-link-selected": {"background-color": "#1c2d9c","icon": "white"}
        }
        )




#title of the app
#title="Car Damage Detection"
#title_icon=":oncoming_automobile:"
#st.title(title+""+title_icon)


display = Image.open('title_logo.jpg')
display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
col1, col2 = st.columns(2)
col1.image(display, width = 820)

#col2.title("Car Damage Detection")

#styling buttons and adding events
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1c2d9c;
    color:#ffffff;
    font-size:16px;
}
div.stButton > button:hover {
    background-color: #78fff8;
    color:#1c2d9c;
    }
</style>""", unsafe_allow_html=True)


# Remove whitespace from the top of the page and sidebar
BACKGROUND_COLOR = 'white'
COLOR = 'black'



#add background images to the app
def set_bg_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
set_bg_url()


# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-hxt7ib  {
                    padding-top: 3rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


def format_Impact(option):
    return impact_choice[option]
def format_sever(option):
    return sever_choice[option]

impact_choice={0:"All around",1:"Front",3:"Rear",4:"Side"}
sever_choice={0:"High",1:"Minor",2:"Moderate"}

tab1, tab2 = st.tabs(["Damage Detection", "Cost Estimation"])

dirc=r"D:\Front end\pred_mask"
img_list=[]
for fn in glob.glob(r"D:\Front end\pred_mask\*"):
        img_list.append(cv2.imread(fn, 0))

l3=[]
l4=[]
l5=[]
df=pd.DataFrame()

for i,j in zip(os.listdir(dirc),img_list):
   l3.append(i)
   l4.append(cv2.countNonZero(j))
   height, width = j.shape
   n_total = height * width
   l5.append(n_total)
df['Filename']=l3
df['Count of damaged pixels']=l4
df['Total image size']=l5
df['Percentage of damaged pixels']=df['Count of damaged pixels']/df['Total image size']


per_dam_pxl=df.iloc[0]['Percentage of damaged pixels']


with tab1:
    st.header("Car Damage Detection")
    file = st.file_uploader("Please select an Image:", type=["jpg", "png"])
    button = st.button("Predict")
    if button == True:
        if file is not None:
            image = Image.open(file)
            predicted_image=predict(image)
            col1, col2 = st.columns(2)
            with col1:
                st.header("Original")
                st.image(image.resize((400,300)), channels="RGB")
            with col2:
                st.header("Prediction")
                st.image(predicted_image.resize((400,300)), channels="RGB")

        else:
            st.warning("Please select an Image to process.......")



# main_how()
# main_abt()
# main_con()




with tab2:
    with st.form("cost"):
        dam_pixel=st.number_input(label="Area of Damage ",value=per_dam_pxl,disabled=True)
        impact=st.selectbox("Select the Impact Area:",options=list(impact_choice.keys()),format_func=format_Impact)
        sever=st.selectbox("Select the Severity:",options=list(sever_choice.keys()),format_func=format_sever)
        submit_val = st.form_submit_button("Estimate cost to repair")
    if submit_val:
        attributes = np.array([dam_pixel,impact,sever])
        price = predictr(attributes.reshape(1, -1))
        if price > 0:
            st.success(f"The cost for repair is : ₹{price.round(2)}")
