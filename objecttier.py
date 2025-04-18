#
# objecttier.py
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author: Ellen Kidane and Prof. Joe Hummel
# Edited by: Jason Insalaco
import datatier

##################################################################
#
# Movie class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
   def __init__(self, movie_id, title, release_year):
      self._Movie_ID = movie_id
      self._Title = title
      self._Release_Year = release_year
   
   @property
   def Movie_ID(self):
      return self._Movie_ID
   
   @property
   def Title(self):
      return self._Title

   @property
   def Release_Year(self):
      return self._Release_Year

##################################################################
#
# MovieRating class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie):
   #inherits movie_id, title, and release_year
   def __init__(self, movie_id, title, release_year, num_reviews, avg_rating):
      super().__init__(movie_id, title, release_year)
      self._Num_Reviews = num_reviews
      self._Avg_Rating = avg_rating
   
   @property
   def Num_Reviews(self):
      return self._Num_Reviews
   
   @property
   def Avg_Rating(self):
      return self._Avg_Rating

##################################################################
#
# MovieDetails class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list
#   Production_Companies: list
#
class MovieDetails(MovieRating):
   #INherits movie_id, title, release_year, num_reviews, and avg_rating
   def __init__(self, movie_id, title, release_year, release_date, runtime, 
                original_language, budget, revenue, num_reviews, avg_rating, 
                tagline, genres, production_companies):
      super().__init__(movie_id, title, release_year, num_reviews, avg_rating)
      self._Release_Date = release_date
      self._Runtime = runtime
      self._Original_Language = original_language
      self._Budget = budget
      self._Revenue = revenue
      self._Tagline = tagline
      self._Genres = genres
      self._Production_Companies = production_companies
   
   @property
   def Release_Date(self):
      return self._Release_Date
   
   @property
   def Runtime(self):
      return self._Runtime
   
   @property
   def Original_Language(self):
      return self._Original_Language

   @property
   def Budget(self):
      return self._Budget
   
   @property
   def Revenue(self):
      return self._Revenue
   
   @property
   def Tagline(self):
      return self._Tagline
   
   @property
   def Genres(self):
      return self._Genres

   @property
   def Production_Companies(self):
      return self._Production_Companies

##################################################################
# 
# num_movies:
#
# Returns: the number of movies in the database, or
#          -1 if an error occurs
# 
def num_movies(dbConn):
   query = "SELECT COUNT(*) FROM Movies;"

   result = datatier.select_one_row(dbConn, query)

   if result:
      return result[0]
   else:
      return -1


##################################################################
# 
# num_reviews:
#
# Returns: the number of reviews in the database, or
#          -1 if an error occurs
#
def num_reviews(dbConn):
   query = "SELECT COUNT(*) FROM Ratings;"

   result = datatier.select_one_row(dbConn, query)

   if result:
      return result[0]
   else:
      return -1

##################################################################
#
# get_movies:
#
# Finds and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all movies.
#
# Returns: list of movies in ascending order by name, or
#          an empty list, which means that the query did 
#          not retrieve any data
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movies(dbConn, pattern):
   query = """
   SELECT Movie_ID, Title, strftime('%Y', Release_Date)
   FROM Movies
   WHERE Title LIKE ?
   ORDER BY Movie_ID ASC;
   """

   data = datatier.select_n_rows(dbConn, query, [pattern])

   movies_list = []
   for c in data:
      individualMovie = Movie(c[0], c[1], c[2])
      movies_list.append(individualMovie)

   return movies_list 

##################################################################
#
# get_movie_details:
#
# Finds and returns details about the given movie.
# The movie ID is passed as a parameter (originally from the user)
# and the function returns a MovieDetails object.
# If no movie was found matching that ID, the function returns
# None.
#
# Returns: a MovieDetails object if the search was successful, or
#          None if the search did not find a matching movie
#          (or an internal error occurred, in which case 
#          an error message is already output).
#

def get_movies(dbConn, pattern):
   query = """
   SELECT Movie_ID, Title, strftime('%Y', Release_Date)
   FROM Movies
   WHERE Title LIKE ?
   ORDER BY Movie_ID ASC;
   """

   data = datatier.select_n_rows(dbConn, query, [pattern])

   movies_list = []
   for c in data:
      individualMovie = Movie(c[0], c[1], c[2])
      movies_list.append(individualMovie)

   return movies_list 

##################################################################
#
# get_movie_details:
#
# Finds and returns details about the given movie.
# The movie ID is passed as a parameter (originally from the user)
# and the function returns a MovieDetails object.
# If no movie was found matching that ID, the function returns
# None.
#
# Returns: a MovieDetails object if the search was successful, or
#          None if the search did not find a matching movie
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movie_details(dbConn, movie_id):
   queryMovie = """
   SELECT Movies.Movie_ID, Title, strftime('%Y', Release_Date), 
   strftime('%Y-%m-%d', Release_Date), Runtime, Original_Language, 
   Budget, Revenue, Tagline
   FROM Movies
   LEFT JOIN Movie_Taglines
   ON Movies.Movie_ID = Movie_Taglines.Movie_ID
   WHERE Movies.Movie_ID = ?;
   """
   movieStats = datatier.select_one_row(dbConn, queryMovie, [movie_id])

   if not movieStats:
      return None
   
   movie_id = movieStats[0]
   title = movieStats[1]
   release_year = movieStats[2]
   release_date = movieStats[3]
   runtime = movieStats[4]
   original_language = movieStats[5]
   budget = movieStats[6]
   revenue = movieStats[7]
   if movieStats[8] is not None:
      tagline = movieStats[8]
   else:
      tagline = ""

   queryRatings = """
   SELECT COUNT(*), AVG(Rating)
   FROM Ratings
   WHERE Movie_ID = ?;
   """

   ratingStats = datatier.select_one_row(dbConn, queryRatings, [movie_id])

   if not ratingStats or ratingStats[0] == 0:
      num_reviews = 0
      avg_rating = 0.0
   else:
      num_reviews = ratingStats[0]
      avg_rating = ratingStats[1]

   queryGenre = """
   SELECT Genres.Genre_Name 
   FROM Movie_Genres
   JOIN Genres ON Movie_Genres.Genre_ID = Genres.Genre_ID
   WHERE Movie_Genres.Movie_ID = ?
   ORDER BY Genres.Genre_Name ASC;
   """

   genreStats = datatier.select_n_rows(dbConn, queryGenre, [movie_id])

   queryProduction = """
   SELECT Companies.Company_Name 
   FROM Movie_Production_Companies
   JOIN Companies ON Movie_Production_Companies.Company_ID = Companies.Company_ID
   WHERE Movie_Production_Companies.Movie_ID = ?
   ORDER BY Companies.Company_Name ASC;
   """

   productionStats = datatier.select_n_rows(dbConn, queryProduction, [movie_id])

   genres = []
   production_companies = []

   if genreStats:
      for c in genreStats:
         genres.append(c[0])

   if productionStats:
      for c in productionStats:
         production_companies.append(c[0])
   
   movie_details = MovieDetails(movie_id, title, release_year, release_date, runtime,
                                original_language, budget, revenue, num_reviews, avg_rating,
                                tagline, genres, production_companies)
   return movie_details        

##################################################################
#
# get_top_N_movies:
#
# Finds and returns the top N movies based on their average 
# rating, where each movie has at least the specified number of
# reviews.
# Example: get_top_N_movies(10, 100) will return the top 10 movies
#          with at least 100 reviews.
#
# Returns: a list of 0 or more MovieRating objects
#          note that if the list is empty, it may be because the 
#          minimum number of reviews was too high
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
   query = """
   SELECT Movies.Movie_ID, Title, strftime('%Y', Release_Date),
   COUNT(Ratings.rating) AS Revs, AVG(Ratings.Rating) AS Rating
   FROM Movies
   JOIN Ratings on Movies.Movie_ID = Ratings.Movie_ID
   GROUP BY Movies.Movie_ID
   HAVING Revs >= ?
   ORDER BY Rating DESC
   LIMIT ?;
   """
   input = [min_num_reviews, N]

   data = datatier.select_n_rows(dbConn, query, input)

   movieList = []

   for c in data:
      id = c[0]
      title = c[1]
      year = c[2]
      reviews = c[3]
      ratings = c[4]

      individualMovie = MovieRating(id, title, year, reviews, ratings)

      movieList.append(individualMovie)
   
   return movieList

##################################################################
#
# add_review:
#
# Inserts the given review (a rating value between 0 and 10) into
# the database for the given movie.
# It is considered an error if the movie does not exist, and 
# the review is not inserted.
#
# Returns: 1 if the review was successfully added, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
   query = """
   SELECT Movie_ID
   FROM Movies
   WHERE Movie_ID = ?;
   """
   checkMovie = datatier.select_one_row(dbConn, query, [movie_id])

   if not checkMovie:
      return 0
   
   queryInsert = """
   INSERT INTO Ratings (Movie_ID, Rating)
   VALUES (?, ?);
   """


   changes = datatier.perform_action(dbConn, queryInsert, [movie_id, rating])

   if changes == 1:
      return 1
   else:
      return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline, i.e. summary, for the given movie.
# If the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline.
# It is considered an error if the movie does not exist, and 
# the tagline is not set.
#
# Returns: 1 if the tagline was successfully set, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
   MovieCheckQuery = """
   SELECT Movie_ID
   FROM Movies
   WHERE Movie_ID = ?;
   """

   MovieCheck = datatier.select_one_row(dbConn, MovieCheckQuery, [movie_id])

   if not MovieCheck:
      return 0
   
   CheckTagQuery = """
   SELECT Tagline
   FROM Movie_Taglines
   WHERE Movie_ID = ?;
   """
   TaglineCheck = datatier.select_one_row(dbConn, CheckTagQuery, [movie_id])

   #Tagline exists in database
   if TaglineCheck:
      if tagline == "":
         DeleteQuery = """
         DELETE FROM Movie_Taglines
         WHERE Movie_ID = ?;
         """
         changes = datatier.perform_action(dbConn, DeleteQuery, [movie_id])

         if changes == 1:
            return 1
         else:
            return 0
      else:
         ChangeQuery = """
         UPDATE Movie_Taglines
         SET Tagline = ?
         WHERE Movie_ID = ?;
         """
         
         changesTwo = datatier.perform_action(dbConn, ChangeQuery, [tagline, movie_id])

         if changesTwo == 1:
            return 1
         else:
            return 0
         
   else:
      if tagline == "":
         return 1
      else:
         TaglineQuery = """
         INSERT INTO Movie_Taglines (Movie_ID, Tagline)
         Values (?, ?);
         """
         changesThree = datatier.perform_action(dbConn, TaglineQuery, [movie_id, tagline])

         if changesThree == 1:
            return 1
         else:
            return 0