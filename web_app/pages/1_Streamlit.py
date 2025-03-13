import streamlit as st

# Page Title
st.title("🚀 Explore Streamlit's Capabilities")

# Introduction
st.markdown(
    """
    Welcome to this demonstration of what you can achieve with **Streamlit**! 
    This page will show you some basic components and functionalities you can easily integrate into your applications.
    
    For those who are eager to dive deeper, check out the [Streamlit documentation](https://docs.streamlit.io).
    """
)

# Example: Slider Widget
st.subheader("🔢 Interactive Widgets")
st.markdown("Try out the slider below to see how Streamlit can handle user input in real-time.")

x = st.slider('Select a number', min_value=1, max_value=100, value=25)
st.write(f"The square of {x} is {x * x}")

# Example: Button
st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

# Example: Text Input
st.subheader("💻 Text Input")
st.markdown("Enter your name to see how Streamlit can handle and display user input.")

name = st.text_input("Your name", key="name")
if name:
    st.write(f"Hello, {name}! Welcome to this Streamlit demo.")

# Example: Selectbox
st.subheader("📦 Selectbox Example")
st.markdown("Pick an option from the dropdown to see how easy it is to handle selections in Streamlit.")

option = st.selectbox(
    'Choose a number',
    [1, 2, 3, 4])
st.write('You selected:', option)

# Example: Progress Bar
st.subheader("📊 Progress Bar")
st.markdown("Use the progress bar to give users feedback on long-running processes.")

progress_bar = st.progress(0)
for i in range(1, 101):
    progress_bar.progress(i)

# Example: File Uploader
st.subheader("📂 File Uploader")
st.markdown("Let users upload files and process them easily.")

file = st.file_uploader("Pick a file")
if file:
    st.write(f"File uploaded: {file.name}")

# Example: Color Picker
st.subheader("🎨 Color Picker")
st.markdown("Allow users to select colors for customizing UI elements or for data visualization.")

color = st.color_picker("Pick a color")
st.write(f"Selected color: {color}")

# Sidebar with Documentation Link
with st.sidebar:
    st.header("📚 Learn More")
    st.markdown(
        """
        This sidebar contains links to additional resources:
        
        - [Streamlit Documentation](https://docs.streamlit.io)
        - [Langchain Documentation](https://langchain.readthedocs.io)
        - [FastAPI Documentation](https://fastapi.tiangolo.com)
        
        Explore these to expand your knowledge and improve your applications!
        """
    )

st.markdown("For more examples and detailed explanations, check out the [Streamlit documentation](https://docs.streamlit.io). Happy coding!")
