import streamlit as st
import pandas as pd
import requests
import random

# Set the title of the Streamlit app
st.title('Choose your Pokemon!🧐')

# Function to fetch Pokémon data (typical ones + sound + abilities and type)
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

# Display a grid of Pokémon images in the sidebar
num_pokemon = 30 # Adjust this number based on the total number of Pokémon you want to display
columns = 2  # Number of columns for the image grid in the sidebar
selected_pokemon = None


st.sidebar.markdown("### Click on a Pokémon image to see its details")

# Fetch and display Pokémon images in the sidebar grid
for i in range(1, num_pokemon + 1, columns):
    cols = st.sidebar.columns(columns)
    for j in range(columns):
        if i + j <= num_pokemon:
            data = get_pokemon_data(i + j)
            with cols[j]:
                st.image(data['image_url'], use_column_width=True)
                if st.button(data['name'], key=f"btn_sidebar_{i+j}"):
                    selected_pokemon = i + j

# Check if a Pokémon was selected and display its details in the main area
if selected_pokemon:
    data = get_pokemon_data(selected_pokemon)
    st.title(data['name'])
    st.image(data['image_url'])
    st.audio(data['cry_url'], format='audio/mp3')
    st.write(f"Height: {data['height']} meters")
    st.write(f"Weight: {data['weight']} kilograms")
    st.write(f"Types: {', '.join(data['types'])}")
    st.write(f"Abilities: {', '.join(data['abilities'])}")