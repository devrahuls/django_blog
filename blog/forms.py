from django import forms
from blog.models import BlogPost

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image'] #Fields that I'm intreseted in, and to play with in this form, from BlogPost model.


class UpdateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'image')
    
    #A custom save method for the blog update form. This function only called if the commit is true.
    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        #If the form has a new image
        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']
        
        if commit:
            blog_post.save()

        return blog_post