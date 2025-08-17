import streamlit as st
import pandas as pd
import plotly.express as px
import ast

st.set_page_config(layout="wide")
st.title("TMDB Movies Dashboard")

# Load data
df = pd.read_csv("C:/Users/sakit/Desktop/Streamlit task/archive/tmdb_5000_movies.csv")

# Preprocess genres column
def extract_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return [g['name'] for g in genres]
    except:
        return []

df['genres_list'] = df['genres'].apply(extract_genres)
all_genres = sorted(set(g for sublist in df['genres_list'] for g in sublist))

# Sidebar filters
st.sidebar.header("Filter Movies")
selected_genres = st.sidebar.multiselect("Select genres", all_genres)
year_range = st.sidebar.slider("Select release year range", 1916, 2017, (2000, 2017))

# Apply filters
filtered_df = df.copy()
filtered_df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
filtered_df = filtered_df[
    filtered_df['release_year'].between(year_range[0], year_range[1])
]

if selected_genres:
    filtered_df = filtered_df[
        filtered_df['genres_list'].apply(lambda x: any(g in x for g in selected_genres))
    ]

# Show filtered data
st.subheader("🎬 Filtered Movies")
st.dataframe(filtered_df[['title', 'release_year', 'vote_average', 'budget', 'revenue']].head(20))

# Charts
st.subheader("📊 Visual Insights")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.scatter(
        filtered_df,
        x='budget',
        y='revenue',
        hover_name='title',
        title="💰 Budget vs Revenue"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.histogram(
        filtered_df,
        x='vote_average',
        nbins=20,
        title="⭐ Rating Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)
import sys
st.write(sys.executable)