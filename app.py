from flask import Flask, render_template, request
import requests
import numpy as np
from scipy.spatial.distance import cityblock, euclidean, minkowski
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Function to calculate Manhattan Distance
def manhattan_distance(point1, point2):
    return cityblock(point1, point2)

# Function to calculate Euclidean Distance
def euclidean_distance(point1, point2):
    return euclidean(point1, point2)

# Function to calculate Minkowski Distance
def minkowski_distance(point1, point2, p):
    return minkowski(point1, point2, p)

# Function to calculate Pearson Correlation
def pearson_correlation(point1, point2):
    return pearsonr(point1, point2)[0]

# Function to calculate Cosine Similarity
def cosine_similarity_calculation(point1, point2):
    return cosine_similarity([point1], [point2])[0, 0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    movie_id1 = int(request.form.get('movie_id1'))
    movie_id2 = int(request.form.get('movie_id2'))

    # Call your API to get ratings for movie_id1 and movie_id2
    api_url = f'http://ip172-18-0-15-cla0vessnmng00e3fg80-5000.direct.labs.play-with-docker.com/ratings'
    response = requests.get(api_url)
    data = response.text.split('\n')[1:-1]  # Skip header and split rows
    ratings_data = [list(map(float, line.split(',')[0:4:2])) for line in data if line]

    # Extract ratings for the specified movie ids
    points_movie_id1 = [(user_id, rating) for user_id, m_id, rating, _ in ratings_data if m_id == movie_id1]
    points_movie_id2 = [(user_id, rating) for user_id, m_id, rating, _ in ratings_data if m_id == movie_id2]

    # Calculate distances and similarities
    manhattan = manhattan_distance(points_movie_id1[0], points_movie_id2[0])
    euclidean_dist = euclidean_distance(points_movie_id1[0], points_movie_id2[0])
    minkowski_dist = minkowski_distance(points_movie_id1[0], points_movie_id2[0], 3)  # Example with p=3 for Minkowski distance
    pearson_corr = pearson_correlation(points_movie_id1[1], points_movie_id2[1])
    cosine_sim = cosine_similarity_calculation(points_movie_id1[1], points_movie_id2[1])

    result = {
        'manhattan': manhattan,
        'euclidean': euclidean_dist,
        'minkowski': minkowski_dist,
        'pearson': pearson_corr,
        'cosine': cosine_sim
    }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
