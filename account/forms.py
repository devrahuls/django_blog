from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2') #Fields that I want during the registration of the user.
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user


#Custom form. Similarly, built-in form like 'UserCreationForm', but for the login users instead creating one.
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput) 
    #   widget=forms.PasswordInput -> It hides the characters of the password that is being input in the field.
    class Meta:
        model = Account
        fields = ('email', 'password') #Fields that are required to login the user

    #  The clean function is available to any form that extends the 'forms.ModelForm'.
    #  Its like an interceptor, before the form can do anything this clean method has to run, and any logic that we write inside this 
    # method will get executed before the form do anything.
    #We are writing this method because any credentials before going to login, will get checked here if it is valid or not.
    def clean(self):
        #If the parameters that have been passed to the form is valid or not.
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid credentials!")
            

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username')

    #We can also particularly clean the fields
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            #Check if the new email that user wanna update doesn't relate to the other existing account.
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email) #Basically checks if the user exist.
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" already in use.' % email)
        
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            #Check if the new username that user wanna update doesn't relate to the other existing account.
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username) #Basically checks if the user exist.
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" already in use.' % username)

