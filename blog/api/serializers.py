from rest_framework import serializers

from blog.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):

    #A field, that holds the username of the blog.
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'date_updated', 'username'] #The reason I dont put author here from BlogPost model, bcz it will return a number.
    
    #A method, responsible for returning the username to the SerializerMethodField, from the blog_post.author
    def get_username_from_author(self, blog_post):
        username = blog_post.author.username
        return username