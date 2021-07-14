from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index),
    path('addUser', views.addUser),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('logout', views.logout),


#User
    path('user/<int:user_id>', views.user), # A Single User's Home Page
    path('edit', views.edit),
    path('upload', views.upload),

#Restaurants
    path('restaurants', views.all_restaurants), #where all restaurants sit
    path('add_restaurant', views.add_restaurant), #page to make new restaurant
    path('restaurant/<int:rest_id>', views.restaurant), #info of a restaurant
    path('uploadRest', views.uploadRest),
    path('makerestaurant', views.makerestaurant), #Making a new Restaurant(function)
    path('filter', views.filter),


#Reviews
    path('restaurant/<int:rest_id>/<int:user_id>/addreview', views.addreview),
    # path('restaurant/<int:user_id>/addreview', views.addreview2),
    path('add_review/<int:rest_id>/<int:user_id>', views.add_review),
    path('delete/<int:rest_id>/<int:rev_id>', views.delete), 

    # path('search',views.search),
]