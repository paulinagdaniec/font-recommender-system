import streamlit as st
import base64
import os
import csv
import random

# Read in the available fonts from the CSV file
font_list = []
with open("availablefonts.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        font_list.append(row[0])

# Define a CSS style with white text color
css = """
    <style>
        .mytext {
            color: white;
            font-size: 40px;
        }
    </style>
"""

# Display the CSS style
st.markdown(css, unsafe_allow_html=True)

# Define a function to generate a random font style
def get_random_font(text=None):
    random_font = random.choice(font_list)
    font_dir = "/Users/paulinagdaniec/Desktop/State of the art tech/collectedttf"
    font_file = os.path.join(font_dir, random_font)
    font_data = open(font_file, "rb").read()
    font_b64 = base64.b64encode(font_data).decode()
    font_style = f"""
        <style>
            @font-face {{
                font-family: myfont;
                src: url('data:application/font-ttf;charset=utf-8;base64,{font_b64}');
            }}
            .mytext {{
                font-family: myfont;
                color: white;
                font-size: 30px;
            }}
        </style>
    """
    if text:
        # Generate a new font style with the input text
        font_style = f"""
            <style>
                @font-face {{
                    font-family: myfont;
                    src: url('data:application/font-ttf;charset=utf-8;base64,{font_b64}');
                }}
                .mytext {{
                    font-family: myfont;
                    color: white;
                    font-size: 30px;
                }}
            </style>
        """
        # Display the input text with the custom font
        html = f'<span class="mytext">{text}</span>'
        return font_style, html, random_font
    
    return font_style, random_font

# Add a button to choose font and save to CSV
def save_to_csv(user, text, font):
    filename = "user_input.csv"
    headers = ["User Name", "Text", "Selected Font"]
    mode = "a" if os.path.exists(filename) else "w"
    with open(filename, mode, newline="") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(headers)
        writer.writerow([user,text, font])
    st.success("Font saved successfully to your library!")

st.header("Random font generator")

# Ask user for name 

user_name = st.text_input("Enter your name")


# Display the user inputted text with a random font
user_text = st.text_input("Enter your text")

if user_text:
    # Generate a random font style and display it
    font_style, text_html, font_name = get_random_font(text=user_text)
    st.markdown(font_style, unsafe_allow_html=True)
    
    # Display the font name and input text with the custom font
    st.write(f"Using font: {font_name}")
    st.markdown(text_html, unsafe_allow_html=True)
    
    # Add a "Refresh" button to select a new font
    if st.button("Refresh"):
    # Generate a new font style and display it with the same input text
      font_style, text_html, font_name = get_random_font(text=user_text)
      st.markdown(font_style, unsafe_allow_html=True)
      # st.write(f"Using font: {font_name}")
      # st.markdown(text_html, unsafe_allow_html=True)

# Add a "Save" button to store the input text and font to a CSV file
    if st.button("Save to library"):
      save_to_csv(user_name, user_text, font_name)


