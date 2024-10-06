from django.shortcuts import render
from blog.models import BlogPost
from operator import attrgetter
from blog.views import get_blog_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



BLOG_POSTS_PER_PAGE = 1
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
        query = request.GET.get('q', '') #Get the query from the search bar. if it is empty then pass the empty '' to the url.
        context['query'] = str(query) #Display the query in the search bar.

    #Get all the blog post, and then sort it by the date_updated field in the descending order(reverse=True).
    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts

    #Pagination
    page = request.GET.get('page', 1) #Get the page number from the url, if it is not there then set it to 1.
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE) #Show 5 blog posts per page.

    try:
        blog_posts = blog_posts_paginator.page(page) #Get the blog posts for that page.
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE) #If the page is not an integer, then show the first page.
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages) #If the page is empty, then show the last page.
    
    context['blog_posts'] = blog_posts
    return render(request, 'personal/home.html', context)