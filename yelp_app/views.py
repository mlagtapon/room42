from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *
from django.contrib import messages
import bcrypt


def index(request):
    if 'user_id' in request.session:
        context = {
            'all_the_restaurants' : Restaurant.objects.all().order_by('name'),
            'user' : request.session['user_id'],
            'recent_rev' : Review.objects.last(),
            'recent_rest' : Restaurant.objects.last()
            }
        return render(request, 'index.html', context)
    else:
        context = {
            'all_the_restaurants' : Restaurant.objects.all(),
            'user': 0,
            'recent_rev' : Review.objects.last(),
            'recent_rest' : Restaurant.objects.last()
        }
        return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')


def addUser(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            for key, value in errors.items():
            
                messages.error(request, value, extra_tags=key)
            return redirect('/')
    
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use.", extra_tags="email")
            return redirect('/')

        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'],
            city = request.POST['city'],
            state = request.POST['state'],
            email=request.POST['email'],
            password=pw
            )

        request.session['user_id'] = User.objects.last().id
        return redirect('/')
    else:
        return redirect('/')

def userlogin(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/login')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password.", extra_tags="login")
            return redirect('/login')

        if not bcrypt.checkpw(request.POST['login_pw'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password.", extra_tags="login")
            return redirect('/login')

        request.session['user_id'] = user[0].id
        request.session['first_name'] = user[0].first_name
        request.session['last_name'] = user[0].last_name
        request.session['city'] = user[0].city
        request.session['state'] = user[0].state
        request.session['email'] = user[0].email

        return redirect('/')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')



#Users

def user(request, user_id):#User Page
    form = User_Form()
    user = User.objects.get(id=user_id)
    context ={
        'user' : user,
        'profile_image': user.profile_image,
        'form' : form,
    }
    return render(request, 'user.html', context)




def edit(request):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        user_id = request.session['user_id']
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect('/user/' + str(user_id))
    

        user_id = request.session['user_id']
        user_to_update = User.objects.get(id = user_id)
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.city = request.POST['city']
        user_to_update.state = request.POST['state']
        user_to_update.save()

        request.session['message'] = "Edit successful, please re-login!"

        return redirect('/user/' + str(user_id))
    else:
        return redirect('/user/' + str(user_id))
        


def upload(request):
    if request.method == "POST":
        user = User.objects.get(id = request.POST['user_id'])
        uploaded_file = request.FILES['profile_image']
        fs = FileSystemStorage()
        user.profile_image = fs.save(uploaded_file.name, uploaded_file)
        user.save()
        return redirect ('/user/'+request.POST['user_id'])
    else:
        return redirect ('/user/'+request.POST['user_id'])




#Restaurants


def add_restaurant(request):
    form = Restaurant_Form()
    context = {
        'form' : form,
    }
    return render(request, 'addrestaurant.html', context)


def uploadRest(request):
    if request.method == "POST":
        restaurant = Restaurant.objects.get(id = 12)
        uploaded_file = request.FILES['restaurant_image']
        fs = FileSystemStorage()
        restaurant.restaurant_image = fs.save(uploaded_file.name, uploaded_file)
        restaurant.save()
        return redirect ('/restaurant/'+str(12))
    else:
        return redirect ('/restaurant/'+str(12))




def makerestaurant(request):
    if request.method == "POST":
        errors = Restaurant.objects.restaurant_validator(request.POST)

        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/add_restaurant')
    uploaded_file = request.FILES['restaurant_image']
    fs = FileSystemStorage()
    restaurant_image = fs.save(uploaded_file.name, uploaded_file)
    restaurant = Restaurant.objects.create(name = request.POST['name'], owner = request.POST['owner'], address= request.POST['address'], city =request.POST['city'], state=request.POST['state'], desc=request.POST['desc'], category=request.POST['category'], restaurant_image = restaurant_image)

    rest_id = restaurant.id
    request.session['rest_id'] = rest_id 

    return redirect('/restaurant/' + str(rest_id))

def restaurant(request, rest_id):
    onerest = Restaurant.objects.get(id=rest_id)
    
    form = Restaurant_Form()

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        revform= Review_Form()
        context = {
            'revform' : revform,
            'user' : User.objects.get(id=user_id),
            'onerest': onerest,
            'all_restaurant': Restaurant.objects.all(),
            'form' : form,
            'review': Review.objects.all()
        }
        return render(request, 'restaurant.html', context)
    else:
        context = {
            'user' : 0,
            'onerest': onerest,
            'all_restaurant': Restaurant.objects.all(),
            'form' : form,
            'review': Review.objects.all()
        }
        return render(request, 'restaurant.html', context)

def all_restaurants(request):
    context = {
        'all_restaurant': Restaurant.objects.all().order_by('name'),
        'all_reviews' : Review.objects.all(),
    }
    return render(request, 'all_restaurants.html', context)








#Reviews



def addreview(request, rest_id, user_id):

    onerest = Restaurant.objects.get(id=rest_id)
    user = User.objects.get(id = request.session['user_id'])
    form = Review_Form()
    context = {
        'onerest': onerest,
        'all_restaurant': Restaurant.objects.all(),
        'user': user,
        'form' : form,
    }

    return render(request, 'addreview.html', context)


def add_review(request, rest_id, user_id):
    onerest = Restaurant.objects.get(id=rest_id)
    user = User.objects.get(id = request.session['user_id'])
    uploaded_file = request.FILES['review_image']
    fs = FileSystemStorage()
    review_image = fs.save(uploaded_file.name, uploaded_file)
    review = Review.objects.create(user = user, restaurant = onerest, rating = request.POST['rating'], review = request.POST['review'], review_image = review_image )

                    
    return redirect('/restaurant/' + str(rest_id))

def delete(request, rest_id, rev_id):

    destroy = Review.objects.get(id=rev_id)
    destroy.delete()
    return redirect('/restaurant/' + str(rest_id))



#test
def filter(request):
    qs = Restaurant.objects.all().order_by('name')
    name_contains_query = request.GET.get('name_contains')
    category_contains_query = request.GET.get('category_contains')

    if name_contains_query != '' and name_contains_query is not None:
        qs = qs.filter(name__icontains=name_contains_query)

    if category_contains_query !='' and category_contains_query is not None:
        qs = qs.filter(category__icontains=category_contains_query)

    
    context = {
        'queryset': qs.order_by('name'),
    }
    return render(request, 'all_restaurants.html',context)
