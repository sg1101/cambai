import streamlit as st
import requests
import matplotlib.pyplot as plt

# Make a request to the FastAPI service to get current statistics
response = requests.get("http://fastapi:8000/statistics")

st.title("Feedback Analytics Dashboard")

if response.status_code == 200:
    statistics = response.json()

    # Display total tasks processed
    st.subheader("Total Tasks Processed")
    st.write(statistics["total_tasks_processed"])

    # Display average processing time
    st.subheader("Average Processing Time")
    st.write(statistics["average_processing_time"])

    # Display sentiment distribution as a pie chart
    st.subheader("Sentiment Distribution")

    # Create a pie chart using Matplotlib
    labels = list(statistics["sentiment_distribution"].keys())
    sizes = list(statistics["sentiment_distribution"].values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

    # Display the pie chart in Streamlit
    st.pyplot(fig1)

    # Display topic distribution as a pie chart
    st.subheader("Topic Distribution")

    # Create a pie chart for topic distribution using Matplotlib
    labels_topic = list(statistics["topic_distribution"].keys())
    sizes_topic = list(statistics["topic_distribution"].values())
    fig_topic, ax_topic = plt.subplots()
    ax_topic.pie(sizes_topic, labels=labels_topic, autopct='%1.1f%%', startangle=90)
    ax_topic.axis('equal')

    # Display the pie chart in Streamlit
    st.pyplot(fig_topic)

    # Display platform distribution as a pie chart
    st.subheader("Platform Distribution")

    # Create a pie chart for platform distribution using Matplotlib
    labels_platform = list(statistics["platform_distribution"].keys())
    sizes_platform = list(statistics["platform_distribution"].values())
    fig_platform, ax_platform = plt.subplots()
    ax_platform.pie(sizes_platform, labels=labels_platform, autopct='%1.1f%%', startangle=90)
    ax_platform.axis('equal')

    # Display the pie chart in Streamlit
    st.pyplot(fig_platform)
else:
    st.error("Failed to fetch statistics")
