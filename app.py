import streamlit as st
import pickle
import pandas  as pd
from PIL import Image
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="Game Recommender",layout='wide')
st.title(':green[Game Recommendation System]')

game_list=pickle.load(open('games.pkl','rb'))
similarity_list=pickle.load(open('similarities.pkl','rb'))
games=pd.DataFrame(game_list)

def game_recommender(game):
    game_index=games[games['name']==game].index[0]
    distances=sorted(list(enumerate(similarity_list[game_index])),reverse=True, key=lambda x:x[1])[1:10]
    game_recs=[]
    for i in distances:
        game_recs.append(games.iloc[i[0]]['name'])
    return game_recs
    

game_selected=st.selectbox('',(games['name']))


if st.button('Recommend'):
   
    game_recs=game_recommender(game_selected)
    for i in game_recs:
        word = f'latest {i} video game cover photo'
        url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
        content = requests.get(url).content
        soup = BeautifulSoup(content,'lxml')
        images = soup.findAll('img')
        c=0
        img_link=''
        for image in images:
            if c==1:
                img_link=image.get('src')
                break
            c+=1

        im = Image.open(requests.get(img_link, stream=True).raw)
        st.header(i)
        st.image(im)
        


