import streamlit as st
import pandas as pd
import requests
import random
import plotly.express as px

st.title('Welcome, Pokémon Adventurer!🧭')

# Welcome message and instructions
st.markdown("""
    ## Discover the amazing world of Pokémon! 
    Use the sidebar to choose your favourite Pokémon and explore detailed information about it. 
    You'll find its height, weight, types, abilities, and even hear its unique cry! 
    Compare your chosen Pokémon with a random selection of other Pokémon in terms of height and weight.
    Enjoy your adventure! 
    ### ⬅️ Choose your favourite Pokémon in the sidebar to get started!(If it shows an error, please refresh the page till It works.)
""")

# Function to fetch Pokémon data (typical ones + sound + abilities and type)
def get_pokemon_data(pokemon_number):
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
    try:
        response = requests.get(pokemon_url)
        response.raise_for_status()
        data = response.json()
        return {
            'name': data['name'].title(),
            'height': data['height'] / 10,  # height is given in decimetres
            'weight': data['weight'] / 10,  # weight is given in hectograms
            'image_url': data['sprites']['front_default'],
            'types': [t['type']['name'].title() for t in data['types']],
            'abilities': [a['ability']['name'].title() for a in data['abilities']],
            'cry_url': f"https://pokemoncries.com/cries/{pokemon_number}.mp3"  # URL for the Pokemon sound
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for Pokémon number {pokemon_number}: {e}")
        return None

# Function to get random Pokémon data for comparison
def get_random_pokemon_data(num_pokemon=10):
    random_pokemon_data = []
    for _ in range(num_pokemon):
        random_number = random.randint(1, 1025)  # Ensure the random number is within the range of available Pokémon
        data = get_pokemon_data(random_number)
        if data:
            random_pokemon_data.append({
                'name': data['name'],
                'height': data['height'],
                'weight': data['weight']
            })
    return random_pokemon_data

# Display a grid of Pokémon images in the sidebar
num_pokemon = 50  # Adjust this number based on the total number of Pokémon you want to display
columns = 3  # Number of columns for the image grid in the sidebar
selected_pokemon = None

st.sidebar.markdown("### Click on your favourite Pokémon name to see its details")

# Fetch and display Pokémon images in the sidebar grid
for i in range(1, num_pokemon + 1, columns):
    cols = st.sidebar.columns(columns)
    for j in range(columns):
        if i + j <= num_pokemon:
            data = get_pokemon_data(i + j)
            if data:
                with cols[j]:
                    st.image(data['image_url'], use_column_width=True)
                    if st.button(data['name'], key=f"btn_sidebar_{i+j}"):
                        selected_pokemon = i + j

# Check if a Pokémon was selected and display its details in the main area
if selected_pokemon:
    data = get_pokemon_data(selected_pokemon)
    if data:
        st.title(data['name'])
        st.image(data['image_url'])
        st.audio(data['cry_url'], format='audio/mp3')
        st.write(f"Height: {data['height']} meters")
        st.write(f"Weight: {data['weight']} kilograms")
        st.write(f"Types: {', '.join(data['types'])}")
        st.write(f"Abilities: {', '.join(data['abilities'])}")

        # Get random Pokémon data for comparison
        random_pokemon_data = get_random_pokemon_data(num_pokemon=10)
        random_pokemon_data.append({
            'name': data['name'],
            'height': data['height'],
            'weight': data['weight']
        })
        
        st.markdown('# Discover curious facts!🧐')
        # Convert data to a DataFrame
        df = pd.DataFrame(random_pokemon_data)

        # Plotting
        fig = px.scatter(df, x='height', y='weight', text='name', title='Height vs Weight of your Pokemon compared to Others')
        st.plotly_chart(fig)
