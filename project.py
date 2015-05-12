from flask import Flask, render_template, request
import cgi

app = Flask(__name__)

# --- DB Code ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie, Review

engine = create_engine('sqlite:///okmd.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

to_Delete = session.query(Movie).all()
session.delete(to_Delete)

rev_to_delete = session.query(Review).all()
session.delete(rev_to_delete)

session.commit()

@app.route('/')
@app.route('/home')
def HelloWorld():
	movies = session.query(Movie).all()
	# reviews = session.query(Review)
	# if(movies == [] or reviews == []):
	# 	output = 'No movies have been reviewed yet!'
	# else:
	# 	output = ''
	# 	for movie in movies:
	# 		try:
	# 			review = reviews.filter_by(movieId=movie.id).one()
	# 			output+='%s</br>%s</br></br>'%(movie.name, review.reviewText)
	# 		except:
	# 			output += '%s</br>No review yet for %s</br></br>'%(movie.name, movie.name)
	# 	return output
	return render_template('index.html', movies=movies)

@app.route('/reviews/<int:movie_id>/')
def getreview(movie_id):
	moviename = session.query(Movie).filter_by(id=movie_id).one().name
	review = session.query(Review).filter_by(movieId=movie_id).one()
	output = '<h2>%s</h2></br>'%moviename
	output += '%s</br>'%(review.reviewText)
	return output

@app.route('/reviews/<int:movie_id>/edit/')
def editreview(movie_id):
	return "editing movie: %s"%movie_id

@app.route('/reviews/<int:movie_id>/delete/')
def deletereview(movie_id):
	return "deleting movie: %s"%movie_id

@app.route('/reviews/new/', methods=['GET', 'POST'])
def createreview():
	if(request.method == 'POST'):
		print 'posting new review'

			
		moviename = request.form['moviename']
		moviereview = request.form['moviereview']

		newmovie = Movie(name=moviename, year=2012)
		session.add(newmovie)
		session.commit()

		newreview = Review(reviewText=moviereview, friendsList='Rob, Natasha', movie=newmovie)
		session.add(newreview)
		session.commit()

		return HelloWorld()
	else:
		return render_template('newreview.html')


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=5000)