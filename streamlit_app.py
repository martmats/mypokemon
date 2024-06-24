import streamlit as st
import pandas as pd
import requests
import random

# Set the title of the Streamlit app
st.title('Welcome to the Pokemon Wold!🧐')
st.markdown('## Choose your Pokemon!')
st.markdown('### Just choose your favourite Pokemon from the side and all the info will appear here⬇️')

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

# Function to get random Pokémon data for comparison
def get_random_pokemon_data(num_pokemon=10):
    random_pokemon_data = []
    for _ in range(num_pokemon):
        random_number = random.randint(1, 1100)  # Ensure the random number is within the range of available Pokémon
        data = get_pokemon_data(random_number)
        random_pokemon_data.append({
            'name': data['name'],
            'height': data['height'],
            'weight': data['weight']
        })
    return random_pokemon_data

# Display a grid of Pokémon images in the sidebar
num_pokemon = 50 # Adjust this number based on the total number of Pokémon you want to display
columns = 3  # Number of columns for the image grid in the sidebar
selected_pokemon = None


st.sidebar.markdown("### Click on your favourite Pokémon name to see its details")

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


st.markdown('# In the mean time discover curious facts!')

# Function to get random Pokémon data for comparison
def get_random_pokemon_data(num_pokemon=10):
    random_pokemon_data = []
    for _ in range(num_pokemon):
        random_number = random.randint(1, 155)
        url = f"https://pokeapi.co/api/v2/pokemon/{random_number}"
        response = requests.get(url).json()
        name = response['name'].title()
        height = response['height'] / 10  # convert to meters
        weight = response['weight'] / 10  # convert to kilograms
        random_pokemon_data.append((name, height, weight))
    return random_pokemon_data

# Get data for a random selection of Pokémon
random_pokemon_data = get_random_pokemon_data()

# Create a DataFrame for plotting
df = pd.DataFrame(random_pokemon_data, columns=['Name', 'Height', 'Weight'])

# Add the selected Pokémon to the DataFrame
df = df.append({'Name': pokemon_name, 'Height': pokemon_height, 'Weight': pokemon_weight}, ignore_index=True)

# Plot height vs. weight for the selected Pokémon and random Pokémon
fig, ax = plt.subplots()
ax.scatter(df['Height'], df['Weight'])

# Annotate points with Pokémon names
for i, row in df.iterrows():
    ax.annotate(row['Name'], (row['Height'], row['Weight']))

ax.set_xlabel('Height (meters)')
ax.set_ylabel('Weight (kilograms)')
ax.set_title('Height vs. Weight of Selected and Random Pokémon')

# Display the plot
st.pyplot(fig)