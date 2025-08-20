import streamlit as st
import pandas as pd
import ast
import sys

st.set_page_config(layout="wide")
st.title("TMDB Movies Dashboard")

# Load data from local CSV
df = None
try:
    df = pd.read_csv("C:/Users/sakit/Desktop/Streamlit task/tmdb_5000_movies.csv")
except FileNotFoundError:
    st.error("CSV file not found. Please make sure 'tmdb_5000_movies.csv' is in the same folder as this script.")

if df is not None:

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
        st.markdown("**💰 Budget vs Revenue**")
        chart_data = filtered_df[['budget', 'revenue']].dropna()
        st.line_chart(chart_data)

    with col2:
        st.markdown("**⭐ Rating Distribution**")
        rating_counts = filtered_df['vote_average'].value_counts().sort_index()
        rating_df = pd.DataFrame({'vote_average': rating_counts.index, 'count': rating_counts.values})
        st.bar_chart(rating_df.set_index('vote_average'))

st.write(sys.executable)