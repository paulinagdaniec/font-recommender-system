import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")


# Define the Streamlit app

st.title("Welcome to the Font Recommendation System")
st.subheader("We are here to help you find suitable fonts that support the message and feel you want to convey in your design. No more scrolling through thousands of fonts to find the right one.")

st.write ('Character 1 : modern, clean, open, informal, progressive, simple, minimal, contemporary')
st.write('Character 2 : bold, creative, eye-catching, decorative, playful, attention-grabbing, unique')  
st.write('Character 3 : traditional, elegant, trustworthy, formal, classic, established, reliable') 
st.write('Character 4 : personal, friendly, whimsical, expressive, elegant, romantic, feminine') 
st.write(' Character 5 : technical, precise, retro, futuristic, minimal, structured.') 

st.write("Please select a character and the desired font weights to generate recommendations.")


# Load the dataset
data = pd.read_csv("avfonts.csv")

displayed_fonts = set()


def recommend_fonts(character_id, selected_weights, exclude_indices=set(), n_recommendations=5, displayed_fonts=set()):
    character_data = data[data["character"] == character_id].copy()
    character_data["weights"] = character_data["weights"].apply(lambda x: [int(w) for w in x.split(",")])
    character_data = character_data[
        character_data["weights"].apply(lambda x: any([w in selected_weights for w in x]))
    ]
    character_data = character_data.sort_values("rating", ascending=True)
    character_data = character_data[~character_data.index.isin(exclude_indices)]  # Exclude already displayed fonts
    character_data = character_data[~character_data.index.isin(displayed_fonts)]  # Exclude already displayed fonts
    return character_data[["family", "Category", "connotations", "styles", "rating", "weights"]].head(n_recommendations)


characters = sorted(data["character"].unique())
selected_character = st.selectbox("Select a character:", characters)

st.subheader("Font Weights:")
# Define available font weights
available_weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]

st.write("100: Thin, 400: Regular, 900: Ultra-Bold")

# Font weight range slider
selected_weights = st.slider("Select desired font weights:", min_value=min(available_weights), max_value=max(available_weights), value=(300, 600), step=100)

# Define the text descriptions for each font weight
weight_descriptions = {
    100: 'Thin/Hairline',
    400: 'Regular/Normal',
    900: 'Ultra-Bold'
}

# Get the text description for each selected weight
selected_weight_texts = [weight_descriptions.get(weight) for weight in selected_weights]

# Generate recommendations button
generate_button = st.button("Generate Recommendations", key="generate_button")

def regenerate_recommendations(selected_character, selected_weights, displayed_fonts):
    new_recommendations = recommend_fonts(selected_character, selected_weights, exclude_indices=displayed_fonts, displayed_fonts=displayed_fonts)
    displayed_fonts.update(new_recommendations.index.tolist())
    return new_recommendations, displayed_fonts

if generate_button:
    recommendations, displayed_fonts = regenerate_recommendations(selected_character, selected_weights, displayed_fonts)

    st.subheader("Your choices:")
    st.write(f"Character: {selected_character}")
    st.write(f"Selected font weights: {'- '.join(map(str, selected_weights))}")

    st.subheader("Recommended Fonts:")
    st.write(recommendations)

