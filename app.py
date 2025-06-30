import pandas as pd
import numpy as np
import streamlit as st
import pickle
import pkg_resources

def main():
    with open('model.pkl', 'rb') as file:
        pipe = pickle.load(file)

    teams = ['Sunrisers Hyderabad', 'Royal Challengers Bengaluru',
        'Mumbai Indians', 'Punjab Kings', 'Kolkata Knight Riders',
        'Delhi Capitals', 'Rajasthan Royals', 'Chennai Super Kings']

    city = ['Chandigarh', 'Jaipur', 'Chennai', 'Bengaluru', 'Mumbai',
        'Visakhapatnam', 'Kolkata', 'Ahmedabad', 'Durban', 'Hyderabad',
        'Delhi', 'Abu Dhabi', 'Pune', 'Dubai', 'Centurion',
        'Dharamsala']

    st.title('IPL Score Predictor')

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select Batting Team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

    col_city, = st.columns(1)
    with col_city:
        city = st.selectbox('Select City', sorted(city))

    col3,col4,col5 = st.columns(3)

    with col3:
        current_score = st.number_input('Current Score', min_value=0, max_value=1000, format="%d")

    with col4:
        overs = st.number_input('Overs done(works for over>5)', min_value=5, max_value=19, format="%d")

    with col5:
        wickets = st.number_input('Wickets out', min_value=0, max_value=10, format="%d")

    last_five = st.number_input('Last 5 overs score', min_value=0,max_value=500, value=0, format="%d")

    if st.button('Predict Score'):
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs

        input_df = pd.DataFrame({'bat_team': [batting_team],
                                'bow_team': [bowling_team],
                                'balls_left': [balls_left],
                                'wicket_left': [wickets_left],
                                'crr': [crr],
                                'last_five': [last_five],
                                'current_score': [current_score],
                                'city': [city]
                                })
        
        result = pipe.predict(input_df)
        st.header(f'Predicted Score: {int(result[0])-5} - {int(result[0])+5}')

if __name__=='__main__':
    main()