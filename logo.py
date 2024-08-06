import streamlit as st

def add_logo():
    image_path = "catalytics_logo.png"  # Update this to the correct path to your image file
    with st.sidebar:
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] + div {
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    text-align: center;
                    padding-bottom: 30px;
                    overflow: hidden;
                }
                .sidebar-footer {
                    display: flex;
                    flex-direction: column;
                    text-align: left;
                }
                .sidebar-footer img {
                    max-width: 150px;
                    height: auto;
                    max-height: 100px;
                    align-items: center;
                }
                .sidebar-footer p {
                    margin: 0;
                    font-style: italic; 
                }
            </style>
            <div class="sidebar-footer">
                <p><em>By</em></p>
            """,
            unsafe_allow_html=True,
        )
        st.image(image_path, width=150)  # Display the image
        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True,
        )

# add_logo()
