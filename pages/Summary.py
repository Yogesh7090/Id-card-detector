import streamlit as st
from utils.database_operations import fetch_all_data
import plotly.graph_objects as go
from logo import add_logo

def bar_graph(names, durations):
    """
    Creates and displays a bar graph in Streamlit using Plotly.

    Parameters:
    - names (list): List of names to be displayed on the x-axis.
    - durations (list): List of durations corresponding to each name on the y-axis.
    """
    # Create a bar plot using Plotly
    fig = go.Figure(data=[go.Bar(
        x=names,
        y=durations,
        text=durations,  # Text to display on hover
        marker_color='skyblue',  # Custom color for bars
        textposition='outside',  # Display text outside the bars
    )])
    
    # Update layout with custom settings
    fig.update_layout(
        title='Bar Graph',
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

# Display the title for the Streamlit app
st.markdown('<h1 class="custom-title">ID Card Detector Tool!</h1>', unsafe_allow_html=True)
st.title('Information of Person Stayed Inside Facility')

# Fetch all data from the database
data = fetch_all_data()

# Initialize lists for names and durations
name_list = []
duration_list = []

# Populate the lists with data from the database
for i in data:
    name_list.append(i['name'])
    duration_list.append(i['duration'])

# Create and display the bar graph
bar_graph(name_list, duration_list)

# Add the logo to the app
add_logo()
