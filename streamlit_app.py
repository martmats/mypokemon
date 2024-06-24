import streamlit as st
import pandas as pd
import requests

st.title('Pokemon Explorer!!!')


### element to pick the pokemon number!!
pokemon_number = st.slider("Choose a pokemon!!!", 1, 1100)

## element to get the latest data on that pokemon!
pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
response = requests.get(pokemon_url).json() 

#element to isolate specific facts about that pokemon!
pokemon_name = response['name']
pokemon_height = response['height']

#code to display it! 
st.title(pokemon_name.title())
st.write(f"This pokemon is {pokemon_height} meters tall!")