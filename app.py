import pickle
import pandas as pd  # Import pandas for handling the DataFrame
from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load movie data and similarity matrix
try:
    # Load movie data
    with open('movies.data.pkl', 'rb') as f:
        movie_data = pickle.load(f)
    if not isinstance(movie_data, pd.DataFrame):
        raise ValueError("The loaded movie data is not a pandas DataFrame.")

    # Display the type and preview for debugging purposes
    print(type(movie_data))  # Should print <class 'pandas.core.frame.DataFrame'>
    print(movie_data.head())  # Preview the first few rows

    # Load similarity matrix
    with open('similarity.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)
except FileNotFoundError as e:
    print(f"Error loading files: {e}")
    exit()
except Exception as e:
    print(f"An error occurred while loading data: {e}")
    exit()

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for Recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form.get('movie')  # Get movie name from the form input

    try:
        # Call the recommendation function
        recommendations = recommend_movies(movie_name)
        print(f"Movie: {movie_name}, Recommendations: {recommendations}")  # For debugging
        return jsonify({'status': 'success', 'movies': recommendations})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred. Please try again.'})

# Recommendation function
def recommend_movies(movie_name):
    # Check if the movie exists in the dataset
    if movie_name not in movie_data['title'].values:
        raise ValueError(f"Movie '{movie_name}' not found in the dataset.")

    # Get the index of the movie
    movie_index = movie_data[movie_data['title'] == movie_name].index[0]

    # Retrieve similarity scores for the movie
    similarity_scores = similarity_matrix[movie_index]

    # Get indices of the top 5 similar movies (excluding the input movie itself)
    similar_movie_indices = sorted(
        list(enumerate(similarity_scores)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]  # Skip the first one (the movie itself)

    # Fetch the movie titles
    recommended_movies = [movie_data.iloc[i[0]]['title'] for i in similar_movie_indices]
    return recommended_movies

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
