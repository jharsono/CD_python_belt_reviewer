from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^register$', views.create_user),
  url(r'^books$', views.books),
  url(r'^books/(?P<id>\d+)$', views.view_book),
  url(r'^books/confirm_delete_review/(?P<id>\d+)$', views.confirm_delete_review),
  url(r'^books/delete_review/(?P<id>\d+)$', views.delete_review),
  url(r'^books/add$', views.add),
  url(r'^books/add_book_to_db$', views.add_book_to_db),
  url(r'^books/(?P<book_id>\d+)/add_review$', views.add_review),
  url(r'^users/(?P<id>\d+)$', views.user),
]
