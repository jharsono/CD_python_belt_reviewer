from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        get_email = User.objects.filter(email=postData['email'])
        print '**email**'
        print get_email
        print '**pw**'

        if len(postData['email']) == 0:
            errors["no_email"] = "Please enter your email"
        if (len(get_email) == 0):
            errors["email_does_not_exist"] = "Email does not exist."
            return errors
        else:
            get_stored_pw = get_email.first().hash_pw

            if len(postData['password']) == 0:
                errors["no_password"] = "Please enter your password."
            if bcrypt.checkpw(postData['password'].encode(), get_stored_pw.encode()) == False:
                errors["wrong_password"] = "Incorrect password."
            return errors


    def reg_validator(self, postData):
        errors = {}
        get_email = User.objects.filter(email=postData['email'])

        #email exists:
        if len(get_email) > 0:
            errors["email_exists"] = "Email already exists."

        #LENGTHS
        if len(postData['first']) == 2:
            errors["first_length"] = "First name must be longer than 2 characters"
        if len(postData['last']) == 2:
            errors["last_length"] = "Last name must be longer than 2 characters"
        if len(postData['email']) == 0:
            errors["no_email"] = "Please enter your email"
        if len(postData['password']) < 8:
            errors["no_password"] = "Your password must be greater than 8 characters."
        if len(postData['confirm-password']) == 0 :
            errors["no_confirm"] = "Please confirm your password."

        #FORMAT
        if all(letter.isalpha() for letter in postData['first']) == False:
            errors["first_format"] = "Your name must only contain letters."
        if all(letter.isalpha() for letter in postData['last']) == False:
            errors["first_format"] = "Your name must only contain letters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email_format"] = "Please enter a valid email."
        #Password
        if (postData['password'] != postData['confirm-password']):
            errors['password_confirm'] = "Your password confirmation does not match."

        return errors


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        title = postData["title"]
        review = postData["review"]
        rating = postData.get("rating")
        try:
            author_check_unique = Book.objects.get(author=postData["author_name"])
        except Book.DoesNotExist:
            author_check_unique = True

        if len(title) == 0:
            errors["title"] = "Please enter a title."
            print "title error"
        if len(review) == 0:
            errors["review"] = "Please enter your review"
            print "review error"

        if postData.get("author_list") == 'none' and len(postData["author_name"])  == 0:
            errors["author"] = "Please enter an author's name or select from list."
            print "author error"
        if author_check_unique != True:
            errors["author"] = "Author already exists, please select from list."
            print "duplicate author"
        if postData.get('rating') == "none":
            errors["rating"] = "Please select a rating."
        return errors

    def review_validator(self, postData):
        errors={}
        review = postData["review"]
        rating = postData.get("rating")

        if len(review) == 0:
            errors["review"] = "Please enter your review"
            print "ERRORS review"
        if rating == "none":
            errors["rating"] = "Please select a rating."
            print "ERRORS rating"
        return errors

class User(models.Model):
    first = models.CharField(max_length=255)
    last = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __unicode__(self):
        return "first: " + self.first + ", Last: " + self.last +  ", Email: " + self.email + ", Date Added: "\
        + str(self.created_at) + ", Submitted books: " + str(self.books_submitted) + ", Submitted Reviews: " + str(self.reviews_submitted)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True)
    submitted_by = models.ForeignKey(User, related_name="books_submitted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "ID: " + str(self.id) + ", Title: " + self.title + ", Author: " + self.author +  ", Submitted By: " + str(self.submitted_by) + ", Date Added: "\
        + str(self.created_at) + str(self.reviews)

    objects = BookManager()


class Review(models.Model):
    review = models.TextField()
    rating = models.CharField(max_length=1)
    book = models.ForeignKey(Book, related_name="reviews")
    reviewer = models.ForeignKey(User, related_name="reviews_submitted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Book: " + str(self.book) + ", Reviewer: " + str(self.reviewer) +  ", Rating: " + str(self.rating) + ", Date Added: "\
        + str(self.created_at) + ", Review: " + self.review

    objects = BookManager()
