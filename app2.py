from flask import Flask, render_template, request, flash, redirect, url_for
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num-Ratings'].values),
                           rating = list(popular_df['avg_rating'].values)
                           )
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Validation logic
    if not username or len(username) < 3:
        flash('Username must be at least 3 characters long.', 'error')
        return redirect(url_for('home'))

    if not password or len(password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return redirect(url_for('home'))

    # If the validations pass
    flash('Login successful!', 'success')
    return redirect(url_for('index'))

@app.route('/recommend')
def recommend_ui():
    return render_template('Recomend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('Recomend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)