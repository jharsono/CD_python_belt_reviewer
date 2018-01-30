from django.shortcuts import render, redirect, HttpResponse

from .models import User, Book, Review
from django.contrib import messages
import bcrypt

#login/reg page
def index(request):
    if "reg_tab_active" not in request.session:
        if "login_tab_active" not in request.session:
            request.session["login_tab_active"] = "active"
    if "logged_in" not in request.session:
        return render(request, 'belt_reviewer/index.html')
    else:
        return redirect('/books')

def login(request):
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            email = request.POST['email']
            if "email" not in request.session:
                request.session['email'] = email

            if "logged_in" not in request.session:
                request.session['logged_in'] = True

            return redirect('/books')

def create_user(request):

    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        if "reg_tab_active" not in request.session:
            request.session["reg_tab_active"] = "active"
            request.session.pop("login_tab_active")

        return redirect('/')
    else:
        email = request.POST['email']
        if "email" not in request.session:
            request.session['email'] = email

        if "logged_in" not in request.session:
            request.session['logged_in'] = True

        User.objects.create(
        first=request.POST['first'],
        last=request.POST['last'],
        email=request.POST['email'],
        hash_pw=hash_pw )
        return redirect('/books')

#homepage / view all user_books
def books(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        email = request.session["email"]
        user = User.objects.get(email=email)
        latest_reviews = Review.objects.order_by("-created_at")[:3]
        all_books = Book.objects.order_by("title")

        context = {
                    "first": user.first,
                    "email": user.email,
                    "reviews_submitted": user.reviews_submitted,
                    "latest_reviews": latest_reviews,
                    "all_books": all_books
                    }
        return render(request, 'belt_reviewer/books.html', context)

def add(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        author_list = Book.objects.values('author').distinct()
        context = {
                    "authors" : author_list
        }
        return render(request, 'belt_reviewer/add.html', context)

#add book to db
def add_book_to_db(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        errors = Book.objects.book_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/add')

        else:
            if request.POST.get("author_list") != "none":
                select_author_from = request.POST.get('author_list')
            else:
                select_author_from = request.POST["author_name"]

            title=request.POST["title"]
            author=select_author_from
            review = request.POST['review']
            rating= request.POST.get('rating')
            this_user = User.objects.get(email=request.session['email'])

            this_book = Book.objects.create(
            title = title,
            author = author,
            submitted_by = this_user
            )
            Review.objects.create(review=review, rating=rating, reviewer=this_user, book=this_book)
            return redirect('/books/'+str(this_book.id))


#view book
def view_book(request, id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        this_book = Book.objects.get(id=id)
        current_user = User.objects.get(email=request.session["email"])
        context = {
            "book" : this_book,
            "reviews": Review.objects.filter(book=this_book).order_by("-created_at"),
            "current_user": current_user,
        }

        return render(request, 'belt_reviewer/view_book.html', context)

#add a Review

def add_review(request, book_id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        errors = Book.objects.review_validator(request.POST)
        print "gets to add review"
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/' + str(book_id))
            print "VALIDATOR ERRORS"
        else:
            review = request.POST["review"]
            rating = request.POST.get("rating")
            reviewer = User.objects.get(email=request.session["email"])
            this_book = Book.objects.get(id=book_id)
            print "SUBMITTING TO DB"

            Review.objects.create(review=review, rating=rating, book=this_book, reviewer=reviewer)

            return redirect('/books/' + str(book_id))


#confirmation page for deleting review
def confirm_delete_review(request, id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        review = Review.objects.get(id=id)
        context = {
                "review": review,
                    }

        return render(request, 'belt_reviewer/confirm_delete.html', context)
#removing review from the db
def delete_review(request, id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        review = Review.objects.get(id=id)
        book_id = review.book.id

        review.delete()

        return redirect('/books/' +str(book_id))

#view a user
def user(request, id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=id)
        reviews = Review.objects.filter(reviewer=id).order_by("-created_at")
        total_reviews = Review.objects.filter(reviewer=id).count()
        context = {
                "user": user,
                "reviews": reviews,
                "total_reviews": total_reviews,
                    }

        return render(request, 'belt_reviewer/user.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
