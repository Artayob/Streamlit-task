import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast
import sys

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
    fig1, ax1 = plt.subplots()
    ax1.scatter(filtered_df['budget'], filtered_df['revenue'], alpha=0.6, color='teal')
    ax1.set_title("💰 Budget vs Revenue")
    ax1.set_xlabel("Budget")
    ax1.set_ylabel("Revenue")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.hist(filtered_df['vote_average'].dropna(), bins=20, color='orange', edgecolor='black')
    ax2.set_title("⭐ Rating Distribution")
    ax2.set_xlabel("Vote Average")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# Show Python executable path
st.write(sys.executable)