from django.shortcuts import render
from blog.models import BlogPost
from operator import attrgetter
from blog.views import get_blog_queryset

# Create your views here.
def home_screen_view(request):
    print(request.headers)
    context = {}
    # context['a_cool_variable'] = 'hello this is a string babe'

    # context = {
    #     'a_cool_variable': 'hello this is a string babe',
    #     'nice_variable': 'hello this is a text bro'
    # }

    # list_of_vars = []
    # list_of_vars.append('1')
    # list_of_vars.append('2')
    # list_of_vars.append('3')
    # list_of_vars.append('4')

    # context['list_of_vars'] = list_of_vars

    # questions = Question.objects.all()
    # context['questions'] = questions

    query = ""
    if request.GET:
        query = request.GET['q'] #Get the query from the search bar.
        context['query'] = str(query) #Display the query in the search bar.

    #Get all the blog post, and then sort it by the date_updated field in the descending order(reverse=True).
    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts

    return render(request, 'personal/home.html', context)