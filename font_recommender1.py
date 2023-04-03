import streamlit as st
import pandas as pd
import numpy as np
import random

# Load font data from CSV file
font_data = pd.read_csv('fontswithconnotations_divided.csv')


# Define groups of feels
group_1 = ["modern", "clean", "universal", "open", "informal", "progressive", 
            "simple, minimal", "contemporary", "futuristic", "creative", "eye-catching", 
            "decorative", "bold", "playful",]
group_2 = ["attention-grabbing", "unique", "expressive,unconventional",
            "traditional", "tradition", "elegant", "trustworthy", "formal", "classic", "established",
            "respect", "trust", "reliable", "personal", "friendly", "whimsical",]
group_3 = ["casual", "creative", 
            "expressive", "elegance", "romantic", "personal", "feminine", "technical", "precise", "retro", 
            "futuristic", "minimal", "structured", "unique", "quirky", "unconventional", "experimental", 
            "artistic", "eclectic"]

feels = group_1 + group_2 + group_3

# Define function to get recommended fonts based on user input
def get_recommendations(feels):
    # Filter fonts that match the selected feels
    matches = font_data[(font_data['connotation_1'].isin(feels)) |
                        (font_data['connotation_2'].isin(feels)) |
                        (font_data['connotation_3'].isin(feels)) |
                        (font_data['connotation_4'].isin(feels)) |
                        (font_data['connotation_5'].isin(feels)) |
                        (font_data['connotation_6'].isin(feels)) |
                        (font_data['connotation_7'].isin(feels)) |
                        (font_data['connotation_8'].isin(feels)) |
                        (font_data['connotation_9'].isin(feels)) |
                        (font_data['connotation_10'].isin(feels))]
    # Randomly select 4 fonts from the matches
    num_matches = len(matches)
    if num_matches == 0:
        return ("No matches found. Please select more feels.")
    else: 
        num_recommendations = random.randint(1, min(5, num_matches))
        recommendations = matches.sample(n=num_recommendations)
        return recommendations

# Define function to generate new recommendations
def regenerate_recommendations(prev_recommendations):
    # Filter out previously recommended fonts
    remaining_fonts = font_data[~font_data['id'].isin(prev_recommendations['id'].tolist())]
    # Randomly select 4 fonts from the remaining fonts
    new_recommendations = remaining_fonts.sample(n=4)
    return new_recommendations

# Create user data CSV file if it doesn't exist
try:
    user_data = pd.read_csv('user_data.csv')
except:
    user_data = pd.DataFrame(columns=['Name', 'Feels', 'Regenerations'])
    user_data.to_csv('user_data.csv', index=False)

# Ask user for their name
name = st.text_input('What is your name?')

# Show welcome message and instructions
st.write(f'Welcome {name}! This is a font recommender system.')
st.write('Please select the feels that you want the font to have.')

# Show feel selection buttons
group_1_feels = st.multiselect('Group 1', group_1)
group_2_feels = st.multiselect('Group 2', group_2)
group_3_feels = st.multiselect('Group 3', group_3)

# Combine selected feels into a single list
selected_feels = group_1_feels + group_2_feels + group_3_feels

# Show recommended fonts if at least one feel is selected
if selected_feels and st.button('See the fonts'):
    # Get recommended fonts based on selected feels
    recommendations = get_recommendations(selected_feels)

    # Show recommended fonts
    st.write('Here are some font recommendations based on your selected feels:')
    for i, row in recommendations.iterrows():
        st.write(f'{row["Family"]} ({row["category"]})')

    #Show regenerate button
    if st.button('Regenerate Recommendations'):
        # Increment regenerations count in user data
        user_data.loc[user_data['Name'] == name, 'Regenerations'] += 1
        user_data.to_csv('user_data.csv', index=False)
        # Generate new recommendations and show them
        new_recommendations = regenerate_recommendations(recommendations)
        for i, row in new_recommendations.iterrows():
            st.write(f'{row["Family"]} ({row["category"]})')
