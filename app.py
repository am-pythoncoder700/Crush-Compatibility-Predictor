from flask import Flask, render_template, request, url_for
import pickle

app = Flask(__name__, static_folder="static")

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the form
    common_interests = float(request.form['common_interests'])
    text_frequency = float(request.form['text_frequency'])
    joke_laugh_count = float(request.form['joke_laugh_count'])
    zodiac_compatibility = float(request.form['zodiac_compatibility'])
    outfit_match = float(request.form['outfit_match'])

    # Create a list of input features
    input_features = [common_interests, text_frequency, joke_laugh_count, zodiac_compatibility, outfit_match]

    # Make prediction using the model
    prediction = model.predict([input_features])

    # Ensure score is within 0-100 range
    prediction[0] = max(0, min(100, prediction[0]))

    # Select romantic quote based on the score
    if prediction[0] >= 80:
        quote = "You are made for each other! ❤️"
    elif 50 <= prediction[0] < 80:
        quote = "Love is blossoming between you two. 🌸"
    elif 30 <= prediction[0] < 50:
        quote = "There's a spark; keep nurturing it! ✨"
    else:
        quote = "It might be time to focus on friendship. 💕"

    return render_template('index.html', prediction=f"{prediction[0]:.2f}", quote=quote)

if __name__ == '__main__':
    app.run(debug=True)