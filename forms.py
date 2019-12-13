from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo


# new user registration
class UserRegistrationForm(FlaskForm):

	# required field, 2 < length < 20
	firstName = StringField('First Name', 
							validators=[DataRequired(), 
							Length(min=2, max=20)
							])

	# required field, 2 < length < 20
	lastName = StringField('Last Name', 
							validators=[DataRequired(), 
							Length(min=2, max=20)
							])

	# required field, 5 < length < 20
	username = StringField('Username', 
							validators=[DataRequired(),
							Length(min=5, max=20)
							])

	# equired field, 8 < length < 64
	password = PasswordField('Password', 
							validators=[DataRequired(),
							Length(min=8, max=64)
							])

	# equired field, 8 < length < 64
	confirmPassword = PasswordField('Confirm Password', 
							validators=[DataRequired(),
							Length(min=8, max=64),
							EqualTo('password')
							])

	# equired field, 10 < length < 1000
	biography = StringField('Biography', 
							validators=[DataRequired(),
							Length(min=10, max=1000)],
							widget=TextArea(),
							)

	# submit buttom
	submit = SubmitField('Register')



# existing user login form
class UserLoginForm(FlaskForm):

	# required field, 5 < length < 20
	username = StringField('Username', 
							validators=[DataRequired(),
							Length(min=5, max=20)
							])

	# equired field, 8 < length < 64
	password = PasswordField('Password', 
							validators=[DataRequired(),
							Length(min=8, max=64)
							])

	# remember user via secure cookie
	remember = BooleanField('Remember Me')

	# submit buttom
	submit = SubmitField('Login')



# existing user update profile form
class UserProfileForm(FlaskForm):

	# required field, 2 < length < 20
	firstName = StringField('First Name', 
							validators=[DataRequired(), 
							Length(min=2, max=20)
							])

	# required field, 2 < length < 20
	lastName = StringField('Last Name', 
							validators=[DataRequired(), 
							Length(min=2, max=20)
							])

	# 10 < length < 255
	biography = StringField('Biography', 
							validators=[
							Length(min=10, max=100)],
							widget=TextArea()
							)

	# must be jpg or png
	image = FileField('Upload new profile picture', validators=[
													FileAllowed(['jpg', 'png'])
													])

	# submit buttom
	submit = SubmitField('Update Profile')



# photo posting form
class UserPostForm(FlaskForm):

	# 0 < length < 20
	caption = StringField('Caption', 
							validators=[DataRequired(),
							Length(max=100)],
							widget=TextArea()
							)

	# 2 < length < 20
	location = StringField('Location',
							validators=[
							DataRequired(),
							Length(min=2, max=20)
							])

	# must be jpg or png
	image = FileField('Upload Image',
						validators=[
						DataRequired(),
						FileAllowed(['jpg', 'png'])
						])

	# boolean, not much to say about it
	followers = BooleanField('Share With Followers')

	# submit buttom
	submit = SubmitField('Post')



# user search form
class UserSearchForm(FlaskForm):

	# 0 < length < 20
	searchQuery = StringField('Username', 
							validators=[DataRequired(),
							Length(max=20)])

	# submit buttom
	submit = SubmitField('Search')



# user search form
class UserFollowForm(FlaskForm):

	# follow buttom
	follow = SubmitField('Follow')

	# unfollow buttom
	unfollow = SubmitField('Unfollow')

	# pending buttom, this button is disabled
	pending = SubmitField('Pending', render_kw={'disabled':''})

	# accept request buttom
	accept = SubmitField('Accept')

	# delete request buttom
	delete = SubmitField('Delete')

