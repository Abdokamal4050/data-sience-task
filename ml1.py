import pandas as pd
import numpy as np
import operator
import seaborn as sns
import matplotlib.pyplot as plt
import itertools


data = pd.read_csv(r"D:\security\tmdb_movies_data.csv")
print(data.head(7))

print(data.info())
print("number of duplicated data ",data.duplicated().sum(),"\n")
data=data.drop_duplicates()

print(data.columns)
# removing NaN values from cast column, keeping only movies that have casted actors
# also removing rows where revenue_adj and budget_adj is equal to zero
data = data[data["cast"].isnull() == False]
data = data[data["genres"].isnull() == False]
data = data[data.budget_adj != 0]
data = data[data.revenue_adj != 0]


#Question 1 : Count of actors
# count the total number of actor appearances
num_actor_appearances = data['cast'].str.count('|').sum() + len(data)

# print the result
print("Number of actor appearances in the dataset: {}".format(num_actor_appearances))

#Question #2: Exploring the Movie genres through the years of the dataset
year_set = set()
genre_set = []
genres_and_year = data[["genres", "release_year"]]

# create a set of unique years of movies
production_year = genres_and_year["release_year"]
production_year = production_year.drop_duplicates()
for year in production_year:
    if year not in year_set:
        year_set.add(year)

# create a list of unique genres by parsing all the years
for year in year_set:
    genre_dict = {}
    genres_in_year = genres_and_year[genres_and_year.release_year == year]
    genres_in_year = genres_in_year["genres"].values
    for elem in genres_in_year:
        genres_row = elem.split("|")
        for genre in genres_row:
            if genre not in genre_set:
                genre_set.append(genre)

# create a dataframe which contains the sum of movies' genre per year
genre_count_per_year_df = pd.DataFrame(index=list(year_set), columns=genre_set)
genre_count_per_year_df[:] = 0

for year in year_set:
    genre_dict = {}
    genres_in_year = genres_and_year[genres_and_year.release_year == year]
    genres_in_year = genres_in_year["genres"].values
    for elem in genres_in_year:
        genres_row = elem.split("|")
        for genre in genres_row:
            if genre not in genre_dict:
                genre_dict[genre] = 1
            else:
                genre_dict[genre] = genre_dict[genre] + 1
                    
    aux_df = pd.DataFrame(genre_dict, index=[year])
    genre_count_per_year_df.loc[year, aux_df.columns] = genre_count_per_year_df.loc[year, aux_df.columns] + aux_df.loc[year]

# most popular genre of movies from year to year
# convert the data type of the DataFrame to float
genre_count_per_year_df = genre_count_per_year_df.astype(float)

# most popular genre of movies from year to year
most_popular_genre_by_year = pd.DataFrame([genre_count_per_year_df.idxmax(axis=1).values,
                                           genre_count_per_year_df.apply(max, axis=1).values],
                                          columns=genre_count_per_year_df.index,
                                          index=["genre", 'counts'])

print(most_popular_genre_by_year)

#Question3  How many movies based on their genres were produced
temp = genre_count_per_year_df.apply(sum)
temp = temp.sort_values(ascending= False)

print(temp)

#Question #4: How much the movie genres changes from year to year
print(genre_count_per_year_df)


#Question #5: Top Movies based on features
###
#Top Movies based on different features
###

revenue_dict = {}

#fetching different columns with 2 different ways of code
movies_and_revenue = data[["original_title", "revenue_adj"]]
movies_and_budget = data[['original_title','budget_adj']]
movies_and_popularity = data[['original_title','popularity']]
movies_and_votes= data[['original_title','vote_average']]

print("Top Movies based on different features")
print(movies_and_revenue.sort_values(by = "revenue_adj", ascending=False).head(10).original_title)
# print(movies_and_revenue.sort_values(by = "revenue_adj", ascending=False).head(10).revenue_adj)

#Question #6: Top Movies based on their budget
#####
#Top 10 movie with the highest adjusted revenue
#####
print("Top 10 movie with the highest adjusted revenue")
print(movies_and_budget.sort_values(by="budget_adj", ascending=False).head(10).original_title)

#Question7 Top Movies based on their popularity
print("Top Movies based on their popularity")
print(movies_and_popularity.sort_values(by="popularity", ascending=False).head(10).original_title)

#Question8 Top 10 Movies based on their average vote
print("Top 10 Movies based on their average vote")
print( movies_and_votes.sort_values(by="vote_average", ascending=False).head(10).original_title)

#Question9 Average Votes Distribution
print("Average Votes Distribution")
print(data[["vote_average"]])

#Question10 Ratings Distribution by Year
print("Ratings Distribution by Year")
print(data[["release_year", "vote_average"]])

#Question 11 number of movies
# creating a seperate list of revenue and budget column
temp_list=['budget', 'revenue']

#this will replace all the value from '0' to NAN in the list
data[temp_list] = data[temp_list].replace(0, np.NAN)

#Removing all the row which has NaN value in temp_list 
data.dropna(subset = temp_list, inplace = True)

rows, col = data.shape
print("number of movies")
print(rows-1)

#Question 12 Movies which had most and least profit
# calculate profit for each movie
data['profit'] = data['revenue'] - data['budget']

# find the movie with the highest profit
max_profit_movie = data.loc[data['profit'].idxmax()]

# find the movie with the lowest profit
min_profit_movie = data.loc[data['profit'].idxmin()]

# print the results
print("Movie with highest profit:")
print("Title: {} \nProfit: ${:,.2f}".format(max_profit_movie['original_title'], max_profit_movie['profit']))
print("\n")
print("Movie with lowest profit:")
print("Title: {} \nProfit: ${:,.2f}".format(min_profit_movie['original_title'], min_profit_movie['profit']))

#Question 13 Get Most Genre Has Profit
# calculate profit for each movie
data['profit'] = data['revenue'] - data['budget']

# split genres into separate rows
genres = data['genres'].str.split('|', expand=True).stack().reset_index(level=1, drop=True).rename('genre')

# merge genres with original data
genres_data = data.drop(columns=['genres']).join(genres)

# group by genre and sum the profits
genre_profits = genres_data.groupby('genre')['profit'].sum()

# find the genre with the highest profit
most_profitable_genre = genre_profits.idxmax()

# print the results
print("Most profitable genre: {}".format(most_profitable_genre))

#Question 14 Get Most Genre Has Profit
# calculate profit for each movie
data['profit'] = data['revenue'] - data['budget']

# split genres into separate rows
genres = data['genres'].str.split('|', expand=True).stack().reset_index(level=1, drop=True).rename('genre')

# merge genres with original data
genres_data = data.drop(columns=['genres']).join(genres)

# group by genre and sum the profits
genre_profits = genres_data.groupby('genre')['profit'].sum()

# find the genre with the lowest profit
least_profitable_genre = genre_profits.idxmin()

# print the results
print("Least profitable genre: {}".format(least_profitable_genre))

#Question 15 Best movie profit for top 5 actors
# calculate profit for each movie
data['profit'] = data['revenue'] - data['budget']

# get the top 5 actors by number of movie appearances
top_actors = data['cast'].str.split('|', expand=True).stack().value_counts().head(5).index.tolist()

# initialize an empty dictionary to store the best movie for each actor
best_movies = {}

# loop over each actor and find their best movie
for actor in top_actors:
    # filter the data to include only movies with the current actor
    actor_movies = data[data['cast'].str.contains(actor)]
    if len(actor_movies) > 0:
        # find the movie with the highest profit for the actor
        best_movie = actor_movies.loc[actor_movies['profit'].idxmax()]
        # store the title of the best movie for the actor in the dictionary
        best_movies[actor] = best_movie['original_title']

# print the results
for actor, movie in best_movies.items():
    print("{}: {}".format(actor, movie))
    
#Question 16  Production company with the most movies
# count the number of movies for each production company
company_counts = data['production_companies'].str.split('|', expand=True).stack().value_counts()

# find the company with the most movies
most_movies_company = company_counts.idxmax()

# print the result
print("Production company with the most movies: {}".format(most_movies_company))

#Question 17 Worst 5 actors by average rating
# group the data by actor and calculate the average rating for each actor
actor_ratings = data.groupby('cast')['vote_average'].mean()

# sort the actors by their average rating (ascending order) and get the 5 worst actors
worst_actors = actor_ratings.sort_values().head(5)

# print the result
print("Worst 5 actors by average rating:")
for actor, rating in worst_actors.items():
    print("- {}: {:.2f}".format(actor, rating))
    
#Question 18 Least watched genre
# count the number of movies in each genre
genre_counts = data['genres'].str.split('|', expand=True).stack().value_counts()

# sort the genres by their count (ascending order) and get the 5 least watched genres
least_watched_genres = genre_counts.sort_values().head(5)

# print the result
print("Least watched 5 genres:")
for genre, count in least_watched_genres.items():
    print("- {}: {}".format(genre, count))
    
#Question 19 most rated year
# group the data by release year and count the number of ratings for each year
year_counts = data.groupby('release_year')['vote_count'].sum()

# find the year with the most ratings
most_ratings_year = year_counts.idxmax()

# print the result
print("Year with the most ratings: {}".format(most_ratings_year))

#Question the least year rated
# group the data by release year and count the number of ratings for each year
year_counts = data.groupby('release_year')['vote_count'].sum()

# find the year with the least ratings
least_ratings_year = year_counts.idxmin()

# print the result
print("Year with the least ratings: {}".format(least_ratings_year))