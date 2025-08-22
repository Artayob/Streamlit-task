import pandas as pd

url = 'https://github.com/Artayob/Streamlit-task/blob/185bd102357874ccf782d329623db71be3adcd90/tmdb_5000_movies.csv'
df = pd.read_csv(url,index_col=0,parse_dates=[0], delimiter=',')
print(df.head(5))