import json
from math import log
import requests
from collections import Counter

def suggest_movie(directory):
    #Loads JSON file as python dictionary
    #userMovie = json.load(open(r"C:\Personal\Movie App (3)\Movie App\staticFiles\user_movie.json"))
    userMovie = json.load(open(directory))
    api_key = 'k_ck108nll'
    #api_key = 'k_vi7lamw2'
    #api_key = 'k_bmbkh4qr'

    userStarList = []
    userDirectorList = []
    userGenreList = []
    userKeywordList = userMovie["keywordList"]

    directorList = userMovie["directorList"]
    for director in directorList:
        userDirectorList.append(director["id"])

    starList = userMovie["starList"]
    for star in starList:
        userStarList.append(star["id"])

    genreList = userMovie["genreList"]
    for genre in genreList:
        userGenreList.append(genre["key"])


    #API CALLS BASED ON USER INPUT
    #GENRES (FULL)
    base_genre_url = f"https://imdb-api.com/API/AdvancedSearch/{api_key}/?genres="
    genres_suffix = ','.join(userGenreList)
    full_genre_url = base_genre_url + genres_suffix 
    response = requests.get(full_genre_url)
    genre_dict = response.json()
    genre_movie_list = []
    #print(genre_dict)
    for movie in genre_dict["results"]:
        genre_movie_list.append(movie["id"])
    #print(genre_movie_list)

    # with open('genre_test.json', 'w') as f:
    #     # Write genre JSON
    #     json.dump(response.json(), f)

    #DIRECTOR
    base_cast_url = f"https://imdb-api.com/en/API/Name/{api_key}/"
    director_movie_dict = {}
    for id in userDirectorList:
        full_director_url = base_cast_url + id
        response = requests.get(full_director_url)
        director_dict = response.json()
        d_list = []
        #print(director_dict)
        for movie in director_dict["castMovies"]:
            if (movie["role"] == "Director"):
                d_list.append(movie["id"])  
        director_movie_dict[id] = d_list
    #print(director_movie_dict)

    #STARS
    star_movie_dict = {}
    base_cast_url = f"https://imdb-api.com/en/API/Name/{api_key}/"
    for id in userStarList:
        full_star_url = base_cast_url + id
        response = requests.get(full_star_url)
        star_dict = response.json()
        s_list = []
        #print(star_dict)
        for movie in star_dict["castMovies"]:
            if (movie["role"] == "Actor"):
                s_list.append(movie["id"])
        star_movie_dict[id] = s_list
    #print(star_movie_dict)

    #KEYWORDS
    base_keyword_url = f"https://imdb-api.com/API/Keyword/{api_key}/"
    keyword_suffix = ','.join(userKeywordList)
    full_keyword_url = base_keyword_url + keyword_suffix
    response = requests.get(full_keyword_url)
    keyword_dict = response.json()
    keywords_movie_list = []
    for movie in keyword_dict["items"]:
        keywords_movie_list.append(movie["id"])
    #print(keywords_movie_list)

    movieList = []
    for director in director_movie_dict:
        movieList.extend(director_movie_dict[director])
    for star in star_movie_dict:
        movieList.extend(star_movie_dict[star])
    movieList.extend(genre_movie_list)
    movieList.extend(keywords_movie_list)

    frequencyDict = Counter(movieList)

    #print(frequencyDict)

    overlapList = []
    for movie in frequencyDict:
        if frequencyDict[movie] > 1 and movie != userMovie["id"]:
            overlapList.append(movie)
    #print(overlapList)

    # Comparison Algorithm
    def compare(movie):
        url = f"https://imdb-api.com/en/API/Title/{api_key}/" + movie +"/Ratings"
        response = requests.get(url)
        movieDict = response.json()
        if movieDict['title'] == None: return
        
        averageRating = (
        (float(movieDict["ratings"]["imDb"]) * 10 if movieDict["ratings"]["imDb"] else 0) +
        (float(movieDict["ratings"]["metacritic"]) if movieDict["ratings"]["metacritic"] else 0) +
        (float(movieDict["ratings"]["theMovieDb"]) * 10 if movieDict["ratings"]["theMovieDb"] else 0) +
        (float(movieDict["ratings"]["rottenTomatoes"]) if movieDict["ratings"]["rottenTomatoes"] else 0) +
        (float(movieDict["ratings"]["filmAffinity"]) * 10 if movieDict["ratings"]["filmAffinity"] else 0)) / 50.0
        cleaned_box_value = movieDict["boxOffice"]["cumulativeWorldwideGross"].replace('$', '').replace(',', '')
        boxOffice = (log(float(cleaned_box_value), 10) if movieDict["boxOffice"]["cumulativeWorldwideGross"] else 0)
        
        keywordMatch = 0
        for keyword in movieDict["keywordList"]:
            if (keyword in userKeywordList):
                keywordMatch += 1
        
        genreMatch = 0
        for genre in movieDict["genreList"]:
            if (genre["key"] in userGenreList):
                genreMatch += 1
        
        recommendationLevel = averageRating + boxOffice + keywordMatch + keywordMatch + genreMatch

        if recommendationLevel == None:
            recommendationLevel = 0.0
            
        return recommendationLevel

    recommendation = {}
    for movie in overlapList:
        recommendation[movie] = [frequencyDict[movie], compare(movie)]
    
    sorted_recommendation = sorted(
        recommendation.items(),
        key=lambda x: (x[1][0], x[1][1]),
        reverse=True
    )
    print(sorted_recommendation)

    sorted_recommendation_dict = {k: v for k, v in sorted_recommendation}   

    top_5_keys = list(sorted_recommendation_dict.keys())[:5]
    movie_list = []
    for id in top_5_keys:
        url = f'https://imdb-api.com/en/API/Title/{api_key}/{id}'
        response = requests.get(url)
        movie_list.append(response.json())

    return(movie_list)

# directory = '/Users/hojunhan/Downloads/Movie App 3/staticFiles/user_movie.json'
# print(suggest_movie(directory=directory))