#
# Jason Insalaco
# CS341
# Movie Database App
#
import sqlite3
import objecttier

#Calls objectTier functions and formats output
def print_stats(dbConn):
        print("General Statistics:")
        print(f" Number of Movies: {objecttier.num_movies(dbConn):,}")
        print(f" Number of Reviews: {objecttier.num_reviews(dbConn):,}") 

#Takes user input and prints out the ID, Title, and Release Year with formatting and object tier function
def optionTwo(dbConn):
        inputTwo = input("Enter the name of the movie to find (wildcards _ and % allowed): ")
        print()
        movies = objecttier.get_movies(dbConn, inputTwo)
        print(f"Number of Movies Found: {len(movies)}")
        print()

        if(len(movies) > 100):
            print("There are too many movies to display (more than 100). Please narrow your search and try again.")
        else:
            for c in movies:
                print(f"{c.Movie_ID} : {c.Title} ({c.Release_Year})")

#Takes user input and calls object tier functions and gives output with formatting
def OptionThree(dbConn):
    inputThree = input("Enter a movie ID: ")
    print()
    movie = objecttier.get_movie_details(dbConn, inputThree)
    if movie is None:
        print("No movie matching that ID was found in the database.")
    else:
        print(f"{movie.Movie_ID} : {movie.Title}")
        print(f"  Release date: {movie.Release_Date}")
        print(f"  Runtime: {movie.Runtime} (minutes)")
        print(f"  Original language: {movie.Original_Language}")
        print(f"  Budget: ${movie.Budget:,} (USD)")
        print(f"  Revenue: ${movie.Revenue:,} (USD)")
        print(f"  Number of reviews: {movie.Num_Reviews}")
        print(f"  Average rating: {movie.Avg_Rating:.2f} (0-10)")
        
        
        print("  Genres:", end = " ")
        for c in movie.Genres:
             print(c + ",", end=" ")

        print()
        
        print("  Production companies:", end=" ")
        for h in movie.Production_Companies:
             print(h + ",", end=" ")
        print()


        print(f"  Tagline: {movie.Tagline}")

#Calls object tier functions and prints the movies with average rating and number of reviews based on user input
def OptionFour(dbConn):
    nValue = int(input("Enter a value for N: "))
    if(nValue <= 0):
        print("Please enter a positive value for N.")
        return
    minReviews = int(input("Enter a value for the minimum number of reviews: "))
    if(minReviews <= 0):
        print("Please enter a positive value for the minimum number of reviews.")
        return
    
    movies = objecttier.get_top_N_movies(dbConn, nValue, minReviews)
    print()
    if movies:
        for c in movies:
            print(f"{c.Movie_ID} : {c.Title} ({c.Release_Year}), Average rating = {c.Avg_Rating:.2f} ({c.Num_Reviews} reviews)")
    else:
         print("No movies were found that fit the criteria.")

#Calls object tier add review function and returns true if the function call does, else false
def OptionFive(dbConn):
    rating = int(input("Enter a value for the new rating (0-10): "))
    if rating < 0 or rating > 10:
         print("Invalid rating. Please enter a value between 0 and 10 (inclusive).")
    else:
        movieID = input("Enter a movie ID: ")

        isTrue = objecttier.add_review(dbConn, movieID, rating)
        print()
        if isTrue:
            print("Rating was successfully inserted into the database.")
        else:
             print("No movie matching that ID was found in the database.")

#Calls object tier set tagline function and returns true if true, else false
def OptionSix(dbConn):
    tag = input("Enter a tagline: ")
    movie_ID = input("Enter a movie ID: ")
    toChange = objecttier.set_tagline(dbConn, movie_ID, tag)
    print()
    if(toChange == 1):
        print("Tagline was successfully set in the database.")
    else:
         print("No movie matching that ID was found in the database.")


##################################################################  
#
# main
#
print("Project 2: Movie Database App (N-Tier)")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the MovieLens database.")
print()

dbName = input("Enter the name of the database you would like to use: ")

print()
print("Successfully connected to the database!")

dbConn = sqlite3.connect(dbName)

print()
print("Select a menu option: ")
print("  1. Print general statistics about the database")
print("  2. Find movies matching a pattern for the name")
print("  3. Find details of a movie by movie ID")
print("  4. Top N movies by average rating, with a minimum number of reviews")
print("  5. Add a new review for a movie")
print("  6. Set the tagline of a movie")
print("or x to exit the program.")
cmd = input("Your choice --> ")
print()

#While loop to output menu until the user hits x for exit
while(cmd != "x"):
    if(cmd == "1"):
        print_stats(dbConn)
    elif(cmd == "2"):
        optionTwo(dbConn)
    elif(cmd == "3"):
         OptionThree(dbConn)
    elif(cmd == "4"):
         OptionFour(dbConn)
    elif(cmd == "5"):
         OptionFive(dbConn)
    elif(cmd == "6"):
         OptionSix(dbConn)

    print()
    print("Select a menu option: ")
    print("  1. Print general statistics about the database")
    print("  2. Find movies matching a pattern for the name")
    print("  3. Find details of a movie by movie ID")
    print("  4. Top N movies by average rating, with a minimum number of reviews")
    print("  5. Add a new review for a movie")
    print("  6. Set the tagline of a movie")
    print("or x to exit the program.")
    cmd = input("Your choice --> ")
    print()



print("Exiting program.")