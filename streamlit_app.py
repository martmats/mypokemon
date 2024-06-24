import streamlit as st
import pandas as pd
import requests
import random

# Set the title of the Streamlit app
st.title('Choose your Pokemon!🧐 ')

# Function to fetch Pokémon data (typical ones + sound + abilites and type)
def get_pokemon_data(pokemon_number):
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
    response = requests.get(pokemon_url).json()
    return {
        'name': response['name'].title(),
        'height': response['height'] / 10,  # height is given in decimetres
        'weight': response['weight'] / 10,  # weight is given in hectograms
        'image_url': response['sprites']['front_default'],
        'types': [t['type']['name'].title() for t in response['types']],
        'abilities': [a['ability']['name'].title() for a in response['abilities']],
        'cry_url': f"https://pokemoncries.com/cries/{pokemon_number}.mp3"  # URL for the Pokemon sound
    }

# Display a grid of Pokémon images
num_pokemon = 20  # I can adjust the number of pokemon to display (there are like 1000ish)
columns = 10  # Number of columns for the images
selected_pokemon = None

st.markdown("### Click on a Pokémon image to see its details")

# Fetch and display Pokémon images inside the columns
for i in range(1, num_pokemon + 1, columns):
    cols = st.columns(columns)
    for j in range(columns):
        if i + j <= num_pokemon:
            data = get_pokemon_data(i + j)
            with cols[j]:
                if st.button("", key=f"btn_{i+j}"):
                    selected_pokemon = i + j
                st.image(data['image_url'], use_column_width=True)
                st.caption(data['name'])