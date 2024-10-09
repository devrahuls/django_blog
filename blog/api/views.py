from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer


@api_view(['GET', ]) #Because we only want to display/view the data.
def api_detail_blog_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug) #Get all the blog post model objects
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #Return the RESTAPI Response with the status & message of 404 not found.
    
    if request.method == 'GET':
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data) #Return the serialized data