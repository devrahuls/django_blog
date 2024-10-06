from django.shortcuts import render, redirect, get_object_or_404
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.
def create_blog_view(request):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False) 
        #why not only form.save(), because before saving this form, we also have to consider the author name of the blogpost, that is not coming automatically.
        author = Account.objects.filter(email=user.email).first() #Select the first item from the query set.
        obj.author = author #Get the account object for the author
        obj.save() #And, set the account object. Now the form has been save completely.
        form = CreateBlogPostForm() #Now that we have created our blog using the form, now reset the form as it was initially.
    
    context['form'] = form

    return render(request, 'blog/create_blog.html', context)


def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return render('login')
    
    blog_post = get_object_or_404(BlogPost, slug= slug)

    if blog_post.author != user:
        return HttpResponse('You are not the author of that post.')
    
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Blog has been updated successfully"
            blog_post = obj
    else:
        form = UpdateBlogPostForm(
            initial={
                'title': blog_post.title,
                'body': blog_post.body,
                'image': blog_post.image
            }
        )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ") #Split the query into words. python install 24 => [python, install, 24]
    for q in queries:
        posts = BlogPost.objects.filter(
            # Q lookups, are used to make the query.
            # icontaines removes the case sensitivity of the query.
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct() #distinct() removes the duplicate entries from the query set. All of the posts that comes will be unique.

        for post in posts:
            queryset.append(post)

    return list(set(queryset)) #Return the unique posts that are found by the query.