from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout #When you login/registration a user, check their credentials
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost

# Create your views here.
def registration_view(request):
    context = {}
    
    if request.POST:
        form = RegistrationForm(request.POST)

        #this will manage if the credential is valid
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email') #get the email
            raw_password = form.cleaned_data.get('password1') #get the pass
            account = authenticate(email=email, password=raw_password) #It will authenticate that user & create that user object
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    #If it is not a POST req, then it must be a GET req, and they prolly visited the registration page for the first time.
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect('home')
    #If the request of the user is POST, means something entered and requested by the user with some data.
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email= email, password= password)

            #If the user is authenticated, means all the credentials entered by the user is correct.
            if user:
                login(request, user)
                return redirect('home')
    #IF the request of the user is not POST, means somehow user entered the login route directly, then strictly say to just authenticate/login to that user.
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login.html', context)



def account_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=user)
        #We have used instance here, bcz in the form, we referencing instance to get the primary key of the user that is authenticated.
        if form.is_valid():
            form.save() #It commits the changes to the DB, any of the changes that the user updated.
    else:
        form = AccountUpdateForm(
            #When the user go to the, & haven't made any changes then the current mail & username should displayed.
            initial={
                'email': request.user.email,
                'username': request.user.username
            }
        )
    context['account_form'] = form

    #Get the blog post of the authenticated user
    blog_posts = BlogPost.objects.filter(author = request.user)
    context['blog_posts'] = blog_posts
    return render(request, 'account/account.html', context)