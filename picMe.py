#! /usr/bin/env python3
import os

# import flask and helper libs
from flask import Flask, render_template, request, session, url_for, redirect, flash, abort
from functools import wraps

# import custom form modules to write our html
from forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserPostForm, UserSearchForm, UserFollowForm

# import mysql and cursor module
import pymysql 
from pymysql import cursors

# hasing lib
import hashlib
from hashlib import md5

# time
import time
from time import localtime

# flask app instance
app = Flask(__name__)

# set secret key - helps provide protection against XSS and other stuff
app.config['SECRET_KEY'] = 'bb381f00eaeb7e884001da5621e35fcd'

# connect to databse
picMeDB = pymysql.connect(host="localhost",
							user="root",
							password="root",
							db="picme",
							charset="utf8mb4",
							port=8889,
							cursorclass=cursors.DictCursor,
							autocommit=True)

# salt to be used for hashed user passwords
salt = "cs3083"


# will return SHA256 hashed + salted password string
def saltBae(password, salt):
	hashedPassword = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()
	return hashedPassword


# append random string to user provided filename
def randFileName(filename):
	return "%s_%s" % (md5(str(localtime())).hexdigest(), filename)


# will return all fetched data from query, using "with" automatically closes cursor
def queryFetchAll(query):
	myQuery = query
	with picMeDB.cursor() as cursor:
		cursor.execute(query)
	data = cursor.fetchall()
	return data


# will return single row of fetched data from query, using "with" automatically closes cursor
def queryFetch(query):
	myQuery = query
	with picMeDB.cursor() as cursor:
		cursor.execute(query)
	data = cursor.fetchone()
	return data


# will clean query result of potentialy sensitive data
def dataClean(data):
	for entry in data:
		for key in entry.keys():
			if key == "password":
				entry[key] = ''
	return data


# save user uploaded image to server:
def saveImage(image_form_data, path):
	# create new filename for image and save to static/profile_pics
	newName = randFileName(image_form_data.filename)
	print(image_form_data.filename)
	print(newName)
	imagePath = os.path.join(app.root_path, path, newName)
	image_form_data.save(imagePath)

	return newName


# create dictionary of username:profilePicPath from query result
def makeUsersPicsDict(users_data):
	output = {}
	# loop through users in query result
	for person in users_data:
		output[person["username"]] = person["profilePicPath"]
	return output


# remove profilePicPath column from query result
def removePicCol(users_data):
	output = []
	# loop through users in query result
	for person in users_data:
		del person["profilePicPath"]
	return 0


# create dictionary of username:followstatus from query result
def makeUsersStatus(requests_data):
	output = {}
	# loop through users in query result
	for person in requests_data:
		output[person["username"]] = person["followstatus"]
	return output


# select and return pending requests for user in session
def getRequests(user):
	requests_query = 'SELECT * FROM Follow WHERE username_followed = "{}" AND followstatus = 0;'.format(user)
	requests_data = queryFetchAll(requests_query)
	return requests_data


# require user log in for specific routes, used as decorator
def login_required(f):
	@wraps(f)
	def dec(*args, **kwargs):
		if "username" not in session:
			flash("You must be logged in to view that page.", 'primary')
			return redirect(url_for("login"))
		return f(*args, **kwargs)
	return dec


# general functions end here
#########################################################################
# routes start here


@app.route('/')
@app.route('/index')
def index():
	# check for user session
	if "username" in session.keys():
		return redirect(url_for('home'))

	query = 'SELECT * FROM Person'
	data = queryFetchAll(query)
	
	return render_template('index.html', title='Index', data=dataClean(data))



@app.route('/home', methods=['GET', 'POST'])
def home():
	# check for user session
	if "username" not in session:
		return redirect(url_for("index"))

	# select descending posts from followers, users in groups i own, users in groups i'm in (UNION will remove duplicates)
	posts_query = ''' SELECT Photo.filepath,Photo.postingdate,Photo.photoPoster,Photo.photoID,Photo.caption,Person.firstName,Person.lastName FROM Photo JOIN Person 
				WHERE Photo.photoPoster = Person.username AND Photo.photoPoster IN (
				SELECT username_followed FROM Follow WHERE username_follower = "{}" AND followstatus = 1 UNION
				SELECT member_username FROM BelongTo WHERE owner_username = "{}" UNION
				SELECT member_username FROM belongTo WHERE groupName IN (SELECT groupName FROM belongTo WHERE member_username = "{}")) ORDER BY Photo.postingdate DESC;'''.format(session["username"],  session["username"],  session["username"])
	data = queryFetchAll(posts_query)

	# create form for user requests management
	formFollow = UserFollowForm()

	return render_template('home.html', title='Home', data=data, requests=getRequests(session["username"]), formFollow=formFollow)



@app.route('/404', methods=['GET'])
def not_found():
	return  render_template('404.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
	# check if user is logged in
	if "username" in session.keys():
		return redirect(url_for('home'))

	# create user reg form 
	form = UserRegistrationForm()

	# if valid
	if form.validate_on_submit():

		# extract data from user registration form
		username = form.username.data
		password = form.password.data
		firstName = form.firstName.data
		lastName = form.lastName.data
		bio = form.biography.data

		# hash and salt plaintext password before insertion
		hashed_password = saltBae(password, salt)
		
		# try to register user
		try:
			query = 'INSERT INTO Person (username, password, firstName, lastName, bio, profilePicPath) VALUES ("{}", "{}","{}", "{}", "{}", "{}");'.format(username, hashed_password, firstName, lastName, bio, 'default.png')
			queryFetch(query)
		except pymysql.err.IntegrityError:
			flash("Username already taken!, please try again.", 'danger')
			return redirect(url_for('register'))
		
		flash("Account created successfully for {}, you may now login!".format(username), 'success')
		return redirect(url_for('login'))

	# if not valid just return to register page and flash warning
	return  render_template('register.html', title='Register', form=form)



@app.route('/login',  methods=['GET', 'POST'])
def login():
	# check if user is logged in
	if "username" in session.keys():
		return redirect(url_for('home'))

	# create user login form 
	form = UserLoginForm()

	# if valid input
	if form.validate_on_submit():

		# get data from user registration form
		username = form.username.data
		password = form.password.data
		remember = form.remember.data

		# salt and hash plaintext password before loopup
		hashed_password = saltBae(password, salt)

		print(password + " " + salt + " " + hashed_password)

		# construct and execute query
		query = 'SELECT * FROM Person WHERE username = "{}" AND password = "{}";'.format(username, hashed_password)
		data = queryFetch(query)

		# check for existing user
		if data:
			# store user data for current session
			session["username"] = username
			session["firstName"] = data["firstName"]
			session["lastName"] = data["lastName"]
			session["biography"] = data["bio"]
			session["profilePicPath"] = data["profilePicPath"]
			session.permanent = remember
			flash("Login Successful", 'success')
			return redirect(url_for('home'))

		# no user found	
		flash("Wrong username or password, please try again.", 'danger')

	return  render_template('login.html', title='Login', form=form)



@app.route("/logout", methods=["GET"])
@login_required
def logout():
	session.pop("username")
	return redirect(url_for("index"))



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
	# user profile form 
	form = UserProfileForm()

	# if valid input
	if form.validate_on_submit():

		# check for new profile image date, remove old
		if form.image.data:
			old = session["profilePicPath"]
			savedImage = saveImage(form.image.data, 'static/profile_pics')
			if old != 'default.png':
				os.remove(os.path.join(app.root_path, 'static/profile_pics', old))
		else:
			# contruct query for fetching user profile
			query = 'SELECT * FROM Person WHERE username = "{}";'.format(session["username"])
			data = queryFetch(query)
			savedImage = data["profilePicPath"]

		# extract data from user profile form
		firstName = form.firstName.data
		lastName = form.lastName.data
		biography = form.biography.data

		# try to update user
		try:
			# query database and update user info
			query = 'UPDATE Person SET firstName = "{}", lastName = "{}", bio = "{}", profilePicPath = "{}" WHERE Person.username = "{}";'.format(firstName, lastName, biography, savedImage, session["username"])
			queryFetch(query)
		except Exception as err:
			print(err)
			flash("Information not updated!, databse error occured.", 'danger')
			return redirect(url_for('profile'))

		# update session info with new data
		session["firstName"] = firstName
		session["lastName"] = lastName
		session["biography"] = biography
		session["profilePicPath"] = savedImage

		flash("Profile updated successfully for user {}".format(session["username"]), 'success')
		return redirect(url_for('profile'))

	elif request.method == "GET":
		# populate form with user session data
		form.firstName.data = session["firstName"]
		form.lastName.data = session["lastName"]
		form.biography.data = session["biography"]

	# get all user posts and return
	query = 'SELECT * FROM Photo WHERE photoPoster = "{}";'.format(session["username"])
	data = queryFetchAll(query)

	# create form for user requests management
	formFollow = UserFollowForm()

	return  render_template('profile.html', title='Profile', form=form, userPosts=data, requests=getRequests(session["username"]), formFollow=formFollow)



@app.route('/post', methods=['GET','POST'])
@login_required
def postPhoto():
	# user post form 
	form = UserPostForm()

	# check for GET
	if request.method == "GET":

		# create form for user requests management
		formFollow = UserFollowForm()

		return render_template('new_post.html', title='Update Post', form=form, requests=getRequests(session["username"]), formFollow=formFollow)

	# if valid input
	if form.validate_on_submit():

		# extract data from user post form
		caption = form.caption.data
		location = form.location.data
		image = saveImage(form.image.data, 'static/post_pics')
		followers = int(form.followers.data)

		# try to insert user post
		try:
			# query database and insert user post
			query = 'INSERT INTO Photo (photoID, postingdate, filepath, allFollowers, caption, photoPoster) VALUES (NULL, CURRENT_TIMESTAMP, "{}", {}, "{}", "{}");'.format(image, followers, caption, session["username"])
			queryFetch(query)
			flash("Post successful!", 'success')
		except Exception as err:
			print(err)
			flash("Could not post! Databse error occured.", 'danger')

	return redirect(url_for('home'))



@app.route('/post/<int:post_id>', methods=['GET'])
@login_required
def viewPost(post_id):
	# retrive photo post data with given id
	query = 'SELECT * FROM Person, Photo WHERE Person.username = Photo.photoPoster AND Photo.photoID = {};'.format(post_id)
	data = queryFetch(query)

	# check result
	if data:
		# create form for user requests management
		formFollow = UserFollowForm()

		return render_template('post.html', title='View Post', imgSource=data["filepath"], userPost=data, requests=getRequests(session["username"]), formFollow=formFollow)

	return redirect(url_for('not_found'))



@app.route('/discover',  methods=['GET', 'POST'])
@login_required
def discover():
	# create user search form 
	form = UserSearchForm()

	# create user follow form
	formFollow = UserFollowForm()

	# if valid input
	if form.validate_on_submit():

		# get data from user search form
		searchUser = form.searchQuery.data

		# construct and execute query
		users_query = 'SELECT username,firstName,lastName,bio,profilePicPath FROM Person WHERE username LIKE "%{}%";'.format(searchUser)
		requests_query = 'SELECT Person.username,Follow.followstatus FROM Person JOIN Follow ON Person.username = Follow.username_followed WHERE Follow.username_follower = "{}";'.format(session["username"])
		users_x_requests = 'SELECT Person.username,Person.firstName,Person.lastName,Person.bio FROM Person WHERE Person.username in (SELECT Person.username from Person join Follow on Person.username = Follow.username_followed WHERE Follow.username_follower = "{}");'.format(session["username"])

		# fetch
		users_data = queryFetchAll(users_query)
		requests_data = queryFetchAll(requests_query)
		uxr_data = queryFetchAll(users_x_requests)

		# create dictionary with username:profile pic from users_data
		users_pics = makeUsersPicsDict(users_data)

		# remove profile pic path column from query result (for comparison with rows from the other queries)
		users_data_no_profilePicPath = removePicCol(users_data)

		# create dictionary with username:follow status from requests_data
		users_status = makeUsersStatus(requests_data)

		# check for existing user
		if users_query:
			return render_template('discover.html', title='discover', form=form, formFollow=formFollow, requests=getRequests(session["username"]), users=users_data, userPics=users_pics, usersStatus=users_status, uxr=uxr_data)

		# no user found	
		flash("No users found.", 'info')

	# create form for user requests management
	formFollow = UserFollowForm()

	return  render_template('discover.html', title='discover', form=form, requests=getRequests(session["username"]), formFollow=formFollow)



@app.route('/follow/<user>/<requestTo>',  methods=['POST'])
@login_required
def follow(user, requestTo):
	# try to follow user, except when they already sent the request
	try:
		# construct query
		query = 'INSERT INTO Follow (username_followed, username_follower, followstatus) VALUES ("{}", "{}", 0);'.format(requestTo, user)
		queryFetch(query)
	except pymysql.err.IntegrityError:
		flash("Follow request already sent.", 'info')
		return redirect(url_for('discover'))
	
	flash("Follow request sent sucessfully to "+requestTo, 'success')
	return redirect(url_for('discover'))



@app.route('/unfollow/<user>/<requestTo>',  methods=['POST'])
@login_required
def unfollow(user, requestTo):
	# construct query
	query = 'DELETE FROM Follow WHERE username_followed = "{}" AND username_follower = "{}"'.format(requestTo, user)
	queryFetch(query)
	flash("Unfollowed "+requestTo+" successfully.", 'success')
	return redirect(url_for('discover'))



@app.route('/accept/<user>/<requestTo>',  methods=['POST'])
@login_required
def accept(user, requestTo):
	# construct query
	query = 'UPDATE Follow SET followstatus = 1 WHERE Follow.username_followed = "{}" AND Follow.username_follower = "{}";'.format(user, requestTo)
	queryFetch(query)
	flash(requestTo+" is now following you.", 'success')
	return redirect(url_for('home'))



@app.route('/delete/<user>/<requestTo>',  methods=['POST'])
@login_required
def delete(user, requestTo):
	# construct query
	query = 'DELETE FROM Follow WHERE username_followed = "{}" AND username_follower = "{}"'.format(user, requestTo)
	queryFetch(query)
	flash("Deleted follow request from user "+requestTo, 'success')
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)