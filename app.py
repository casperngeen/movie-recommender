from flask import Flask, render_template
import json
import requests
import api as api #import the api.py file

#app = Flask(__name__, template_folder="C:/Personal/Movie App/templateFiles", static_folder="C:/Personal/Movie App/staticFiles")
app = Flask(__name__, template_folder="templateFiles", static_folder="staticFiles")

api_key = 'k_ck108nll'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help/')
def need_help():
    return render_template('help.html')

@app.route('/aboutus/')
def about_us():
    return render_template('about_us.html')

@app.route('/recommendations/<id>')
def recommendations(id):
    #get JSON for the user's movie and write it into our local JSON file
    userMovieUrl = f"https://imdb-api.com/en/API/Title/{api_key}/" + id + "/FullActor,FullCast,Ratings,Wikipedia"
    response = requests.get(userMovieUrl)
    userMovie = response.json()
    directory = '/Users/caspe2/Personal/Movie App 3 2/staticFiles/user_movie.json'
    with open(directory, "w") as file:
        json.dump(userMovie, file)
    
    movies = api.suggest_movie(directory=directory)

    return render_template("reco.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)