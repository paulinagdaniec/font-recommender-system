import json
from collections import defaultdict

import streamlit as st
import pandas as pd
import base64
import os
import csv
import random

# Load font data from CSV file
data = pd.read_csv('avfonts.csv')

# streamlit intro 

st.title("Welcome to the Font Recommendation System")
st.subheader(
    "We are here to help you find suitable fonts that support the message and feel you want to convey in your design. No more scrolling through thousands of fonts to find the right one.")

# Ask user for name
user_name = st.text_input("Please enter your name")

# characteristic selection
st.subheader("Please select words that suit desired feel of your project.")

feels_all = {
    'sans-serif': 'modern, clean, open, informal, progressive, simple, minimal, contemporary',
    'display': 'bold, creative, eye-catching, decorative, playful, attention-grabbing, unique',
    'serif': 'traditional, elegant, trustworthy, formal, classic, established, reliable',
    'handwriting': 'personal, friendly, whimsical, expressive, elegant, romantic, feminine',
    'monospace': 'technical, precise, retro, futuristic, minimal, structured',
}

feels = ['modern', 'clean', 'open', 'informal', 'progressive', 'simple', 'minimal', 'contemporary', 'bold', 'creative',
         'eye-catching', 'decorative', 'playful', 'attention-grabbing', 'unique', 'traditional', 'elegant',
         'trustworthy', 'formal', 'classic', 'established', 'reliable', 'personal', 'friendly', 'whimsical',
         'expressive', 'elegant', 'romantic', 'feminine', 'technical', 'precise', 'retro', 'futuristic', 'minimal',
         'structured']


def assign_character(selected_feels):
    max_matches = 0
    best_character = 'Sans serif'

    for character, character_feels in feels_all.items():
        # Tokenize character_feels
        character_feels_set = set(character_feels.split(', '))

        # Find the intersection between selected_feels and character_feels_set
        matches = len(character_feels_set.intersection(selected_feels))

        # Check if the current character has more matching feels
        if matches > max_matches:
            max_matches = matches
            best_character = character

    return best_character


# User input: multi-select widget
selected_feels = st.multiselect("Select feels:", feels)

# Match input with character
matched_character = assign_character(selected_feels)

# Display matched character
st.write(f"Most suitable typeface category is: {matched_character}")

# Load the CSV file
csv_file = "avfonts_full.csv"
df = pd.read_csv(csv_file)

font_list = []

# Allow the user to select a font weight using a checkbox
st.subheader("Please select font weights you want to consider.")
st.write("100 is Thin, 400 is Regular whereas 900 responds to Black")
font_weights = ['100', '200', '300', '400', '500', '600', '700', '800', '900']
selected_weights = [st.checkbox(weight, key=weight) for weight in font_weights]

# Create a list of selected font weights
selected_weights_list = [weight for weight, selected in zip(font_weights, selected_weights) if selected]

# Filter the DataFrame based on the 'Category' column, the selected character, and the selected weights
filtered_df = df[(df['Category'] == matched_character) & (
    df['weights'].apply(lambda x: any(weight in x.split(',') for weight in selected_weights_list)))]

# Store the available fonts in font_list
font_list = filtered_df['available_fonts'].tolist()

# Add ".ttf" to each font in the 'available_fonts' column
df['available_fonts'] = df['available_fonts'].apply(lambda fonts: fonts.split(",")[0] + ".ttf")

# Filter the DataFrame based on the 'Category' column and the selected character
filtered_df = df[df['Category'] == matched_character]

# Store the available fonts in font_list
font_list = filtered_df['available_fonts'].tolist()

st.subheader("Let's see.")
st.write(
    "Here you can input a piece of text or simply a word you would like to try out. You can like, dislike and save fonts to your library. We will use your feedback to recommend fonts that you will like.")

# Define a CSS style with white text color
css = """
    <style>
        .mytext {
            color: white;
            font-size: 50px;
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


def show_font(font, text):
    font_dir = "/Users/paulinagdaniec/Desktop/State of the art tech/collectedttf"
    font_file = os.path.join(font_dir, font)
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
    # Display the input text with the custom font
    html = f'<span class="mytext">{text}</span>'
    return font_style, html


def save_to_csv(user, text, font, liked, disliked, feedback=False):
    filename = "user_input.csv"
    headers = ["User Name", "Text", "Selected Font", "Liked", "Disliked"]
    mode = "a" if os.path.exists(filename) else "w"
    with open(filename, mode, newline="") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(headers)
        writer.writerow([user, text, font, liked, disliked])

    if feedback:
        st.success("Thanks for the feedback!")
    else:
        st.success("Font saved successfully to your library!")


# Display the user inputted text with a random font
user_text = st.text_input("Enter your text")

# Now let's start font recommendations
# df = pd.read_csv("avfonts_full.csv")
df = filtered_df


def parse_designer(designer):
    try:
        return json.loads(designer.replace("'", '"'))
    except:
        return None


replace = str.maketrans("", "", "{}'")
df["keywords"] = df["keywords"].apply(lambda x: set(x.translate(replace).split(", ")))
df["weights"] = df["weights"].apply(lambda x: x.split(","))
df["styles"] = df["styles"].apply(lambda x: json.loads(x.replace("'", '"')))
df["connotations"] = df["connotations"].apply(lambda x: x.split(", "))
df["designer"] = df["designer"].astype(str).apply(parse_designer)


def rate_fonts(df, liked, disliked):
    keyword_ratings_factor = 10
    designer_ratings_factor = 1
    connotation_ratings_factor = 0.5
    year_factor = 0.1

    keyword_ratings = defaultdict(int)
    for entry in liked["keywords"]:
        for kw in entry:
            keyword_ratings[kw] += 1

    for entry in disliked["keywords"]:
        for kw in entry:
            keyword_ratings[kw] -= 1

    designer_ratings = defaultdict(int)
    for entry in liked["designer"]:
        if entry is None:
            continue
        for d in entry:
            designer_ratings[d] += 1

    for entry in disliked["designer"]:
        if entry is None:
            continue
        for d in entry:
            designer_ratings[d] -= 1

    connotation_ratings = defaultdict(int)
    for entry in liked["connotations"]:
        for c in entry:
            connotation_ratings[c] += 1

    for entry in disliked["connotations"]:
        for c in entry:
            connotation_ratings[c] -= 1

    liked_year_avg = liked["year"].mean()
    disliked_year_avg = disliked["year"].mean()
    middle_year = (liked_year_avg + disliked_year_avg) / 2

# diviiding by 1000 to make the ratings more reasonable and take into account user preferences rather than popularity of the font
    def rate_font(row):
        rating = 0
        for kw in row["keywords"]:
            rating += keyword_ratings[kw] * keyword_ratings_factor
        for d in row["designer"] if row["designer"] is not None else []:
            rating += designer_ratings[d] * designer_ratings_factor
        for c in row["connotations"]:
            rating += connotation_ratings[c] * connotation_ratings_factor

        rating += (row["year"] - middle_year) * year_factor

        rating -= row["rating"] / 1000
        return rating

    df["rating"] = df.apply(rate_font, axis=1)

    return df.sort_values("rating", ascending=False)


# Load ratings from the CSV file
user_input = pd.read_csv("user_input.csv")
liked = user_input[user_input[" Liked"] == "True"][" Selected Font"].str.replace(".ttf", "")
disliked = user_input[user_input[" Disliked"] == "True"][" Selected Font"].str.replace(".ttf", "")

liked_entries = pd.DataFrame(columns=df.columns)
for font in liked:
    liked_entries = liked_entries.append(df.loc[df["available_fonts"].str.contains(font)])

disliked_entries = pd.DataFrame(columns=df.columns)
for font in disliked:
    disliked_entries = disliked_entries.append(df.loc[df["available_fonts"].str.contains(font)])

r = rate_fonts(df, liked_entries, disliked_entries)

# Remove elements of r that are already in liked or disliked
if not liked_entries.empty:
    r = r[~r["family"].isin(liked_entries["family"])]
if not disliked_entries.empty:
    r = r[~r["family"].isin(disliked_entries["family"])]



print(r["available_fonts"][r["available_fonts"].first_valid_index()])
next_font = r["available_fonts"][r["available_fonts"].first_valid_index()].split(",")[0]
font_name = next_font.replace(".ttf", "")

if user_text:
    # Generate a random font style and display it
    font_style, text_html = show_font(next_font, user_text)
    st.markdown(font_style, unsafe_allow_html=True)

    # Display the font name and input text with the custom font
    st.write(f"Using font: {font_name}")
    st.markdown(text_html, unsafe_allow_html=True)

    # Create columns for the buttons
    col1, col2, col3 = st.columns(3)

    # Add the "Like" button in the first column
    liked = col1.button("Like")

    # Add the "Dislike" button in the second column
    disliked = col2.button("Dislike")

    # If either "Like" or "Dislike" button is clicked, save the font to the CSV file
    if liked or disliked:
        save_to_csv(user_name, user_text, font_name, liked, disliked, feedback=True)

    # Add a "Save" button to store the input text and font to a CSV file in the third column
    if col3.button("Save to library"):
        save_to_csv(user_name, user_text, font_name, False, False)


