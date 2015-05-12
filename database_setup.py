# CONFIGURATION SECTION
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

####

# CLASS SECTION

class Movie(Base):
	# TABLE INFORMATION
	__tablename__ = 'movie'

	# MAPPER INFORMATION
	name = Column(
		String(80),
		nullable = False )

	id = Column(
		Integer,
		primary_key = True )

	year = Column(
		Integer)

	#review = relationship("Review", uselist=False, backref="movie")

class Review(Base):
	# TABLE INFORMATION
	__tablename__ = 'review'

	# MAPPER INFORMATION
	id = Column(
		Integer,
		primary_key = True )

	reviewText = Column(
		Text,
		nullable = False)

	friendsList = Column(
		Text)

	movieId = Column(
		Integer,
		ForeignKey('movie.id'))

	movie = relationship(Movie)

# End of File Stuffz

engine = create_engine(
	'sqlite:///okmd.db')

# Creates all the classes as new tables in the db
Base.metadata.create_all(engine)
