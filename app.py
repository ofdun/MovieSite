from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jHGKGFkj6TYVIi67VI7F6oiCI76C&KJHvouiyVUyvK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reviews = db.relationship('Review', back_populates='movie')
    
    def __repr__(self):
        return f'{self.title}'
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie', back_populates='reviews')
    
    def __repr__(self):
        return f'Отзыв {self.id}'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    add_movie('213123', '123123132')
    movies: list = Movie.query.all()
    return render_template('index.html',
                           movies=movies)
    
def add_movie(title, desc):
    movie = Movie()
    movie.title = title
    movie.description = desc
    db.session.add(movie)
    db.session.commit()

def add_review(name, text, score, movie_id):
    review = Review()
    review.name = name
    review.text = text
    review.score = score
    review.movie_id = movie_id
    db.session.add(review)
    db.session.commit()

if __name__ == '__main__':
    app.run()