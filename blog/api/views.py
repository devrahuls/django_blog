from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer
from django.http import JsonResponse


@api_view(['GET']) #Because we only want to display/view the data.
@permission_classes((IsAuthenticated, )) #No one without the Authentication Token is able to get the view.
def api_detail_blog_view(request, slug):

    #If the blog exist 
    try:
        blog_post = BlogPost.objects.get(slug=slug) #Get all the blog post model objects
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #Return the RESTAPI Response with the status & message of 404 not found.
    
    if request.method == 'GET':
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data) #Return the serialized data


@api_view(['PUT', ]) #Because we want to update the blog.
@permission_classes((IsAuthenticated, )) 
def api_update_blog_view(request, slug):

    #If the blog exist
    try:
        blog_post = BlogPost.objects.get(slug=slug) #Get all the blog post model objects
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #Return the RESTAPI Response with the status & message of 404 not found.
    
    user = request.user
    if blog_post.author != user:
        return Response({'response': "You are not authorize to edit this blog."})
    
    if request.method == 'PUT':
        serializer = BlogPostSerializer(blog_post, data = request.data)
        data = {} #Just like the context

        #Just like we used to do with the django forms
        if serializer.is_valid():
           serializer.save() 
           data['success'] = "updated successfully"
           return Response(data=data) #Return the updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Return the error that why serializer is not valid.
    

@api_view(['DELETE', ]) #Because we want to delete the blog.
@permission_classes((IsAuthenticated, )) 
def api_delete_blog_view(request, slug):
    #If the blog exist
    try:
        blog_post = BlogPost.objects.get(slug=slug) #Get all the blog post model objects
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #Return the RESTAPI Response with the status & message of 404 not found.
    
    user = request.user
    if blog_post.author != user:
        return Response({'response': "You are not authorize to delete this blog."})
    
    if request.method == 'DELETE':
        operation = blog_post.delete() #Delete that blog
        data = {}
        if operation: #if operation was successful
            data['success'] = "Deleted successfully"
        else:
            data["failure"] = "Delete failed"
        return Response(data=data) #Return the respective data
    

@api_view(['POST', ]) #Because we only want to display/view the data.
@permission_classes((IsAuthenticated, ))
def api_create_blog_view(request):
    account = request.user

    #Bcz the model has author field, and we are getting the account above here. Also, BlogPostSerializer doesnt have any account/author field.
    blog_post = BlogPost(author=account)

    if request.method == 'POST':
        serializer = BlogPostSerializer(blog_post, data=request.data) #Passing the blog post that has already an author attached to it.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)