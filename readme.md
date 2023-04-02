# passwordShare
TODO:

 - Add functionality:
     - User registration
     - Implement password reset
 - Add error handling
 - Add comments
 - Add Tests
 - Refactor code as I learn new techniques
 - Ready for deployment
     - Add support for hosting files on Amazon S3 bucket

I got the idea for this project from my day job.  I saw the company that just acquired us had this simple webapp that let you share passwords with users.  It would encrypt the password and generate a link to share.  The link would expire after a set time.  Since I'm still fairly new to Django, I wondered if I could recreate this.  This is my attempt.

The functionality is simple.  You enter some text in the text box, set the time to live (in clicks), and encrypt.  You can also email it from the app. Once the user receives the email, the user was the set amount of times they can access the secret before it is deleted from the database.  The secret is stored encrypted in the database.

Note:  I'm still new to Django so the coding can be a bit crude as I'm learning.  I know Django supplies some functionality but since I'm learning, I wanted to implement some of it on my own.  Such as user functionality.  I'm also a pretty trash at frontend so the website uses Bootstrap and looks very basic.

This project uses Django, Bootstrap and HTMX.

Run the app with Docker:

```
docker compose up -d --build
```

Make and apply migrations:

```
docker compose run app python3 manage.py makemigrations
```

then

```
docker compose run app python3 manage.py migrate
```

You'll need a superuser to login.  I haven't implemented a registration since testing is currently by invite only.

```
docker compose run app python3 manage.py createsuperuser
```


***Outdated.  Use docker to run the project***
~~~To run the app:~~~

Create your virtual environment (optional but recommended):

```
mkvirtualenv passwordshare
```

Install the dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
py manage.py runserver
```
