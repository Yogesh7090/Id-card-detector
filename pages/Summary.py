import streamlit as st

from utils.database_operations import fetch_all_data
import streamlit as st
import plotly.graph_objects as go
from logo import add_logo

def bar_graph(names,durations):
    # Create a bar plot using plotly
    fig = go.Figure(data=[go.Bar(
        x=names,
        y=durations,
        text=durations,  # Text to display on hover
        marker_color='skyblue',  # Custom color for bars
        textposition='outside',  # Display text outside the bars
    )])
    
    fig.update_layout(
        title='Bar Graph ',
        xaxis_title='Name',
        yaxis_title='Duration',
        plot_bgcolor='white',  # Set background color
        bargap=0.2,  # Gap between bars
        font=dict(family='Arial', size=12),  # Font style
    )

    # Customize hover information
    fig.update_traces(hovertemplate='Name: %{x}<br>Duration: %{y} seconds')

    # Display the plot in Streamlit
    st.plotly_chart(fig)



st.markdown('<h1 class="custom-title">ID Card Detector Tool!</h1>', unsafe_allow_html=True)
st.title('Information of person stayed inside Facility')
# image_base64 = img_to_base64("catalytics_logo.png")  
# st.sidebar.markdown(
#     f'''<div class="sidebar-footer">
#     <img src="data:image/png;base64,{image_base64}" width ="200px" 
#     height ="200px" 
#     style="position: fixed; margin-top: 250px; margin-left: 40px;"></div>''',
#     unsafe_allow_html=True
#     )

data = fetch_all_data() 
name_list = []
duration_list = []
for i in data:
    name_list.append(i['name'])
    duration_list.append(i['duration'])
bar_graph(name_list,duration_list)
 
add_logo()