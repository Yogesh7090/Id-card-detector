import streamlit as st
# import base64
# from streamlit_extras.app_logo import add_logo
from logo import add_logo


st.set_page_config(
    page_title="VIDEO ANALYTICS",
    
)
add_logo()
st.markdown(
    """
    <style>
    .custom-title {
        color: #005F7B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom class in the title
st.markdown('<h1 class="custom-title">ID Card Detector Tool!</h1>', unsafe_allow_html=True)

# st.write("# Welcome to E-Commerce Watch!")


st.markdown(
    """
    **Overview:**  
    The ID Card Detector Tool is designed to streamline and automate the process of tracking the in-time and out-time of individuals using their ID cards. This application leverages advanced image recognition technology to detect and process ID cards, ensuring accurate and efficient attendance management.

    **Features:**
    1. **ID Card Detection:**
        - Utilizes high-precision image recognition algorithms to detect and authenticate ID cards.
        - Supports various types of ID cards to cater to a diverse range of users.

    2. **In-Time and Out-Time Calculation:**
        - Automatically records the in-time when an ID card is scanned upon entry.
        - Similarly, records the out-time when the ID card is scanned upon exit.
        - Provides real-time tracking and updates of attendance records.

    3. **User Interface:**
        - Simple and intuitive interface with three main sections: Home, Detector, and Summary.
        - The Home section provides an overview and instructions for using the tool.
        - The Detector section is where the ID card scanning and processing take place.
        - The Summary section presents detailed reports and analytics on attendance.
    """,
unsafe_allow_html=True
)
# st.markdown(
#     """
#     - Check out [Ecommerce](https://catalyticsdatum.com/Home/ECommerce)
#     - Check out our other [products](https://catalyticsdatum.com/Home/Solution)
# """
# )

# Add custom CSS to hide the full-screen button
st.markdown(
    """
    <style>
    button[title="View fullscreen"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# st.sidebar.markdown(
#         """
#         <style>
#         .sidebar-footer {
#             position: absolute;
#             bottom: 10px;
#             left: 0;
#             width: 100%;
#             text-align: center;
#         }
#         </style>
#         """
#     )

# with st.sidebar:
# st.sidebar.markdown(
#     """
#     <style>
#     .sidebar-footer {
#         position: absolute;
#         bottom: 10px;
#         left: 0;
#         width: 100%;
#         text-align: center;
#     }
#     </style>
#     """
# )


# image_base64 = img_to_base64("catalytics_logo.png")  
# st.sidebar.markdown(
# f'''<div class="sidebar-footer">
# <img src="data:image/png;base64,{image_base64}" width ="200px" 
# height ="200px" 
# style="position: fixed; margin-top: 250px; margin-left: 40px;"></div>''',
# unsafe_allow_html=True
# )