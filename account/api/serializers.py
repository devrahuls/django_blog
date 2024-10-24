from rest_framework import serializers

from account.models import Account

#Serializer to register/create a new user.
class RegisterSerializer(serializers.ModelSerializer):

    #It creates password field, and style it by showing the password as dots on screen, also encrypts the password when request to the user.
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {

            #password is a write only field so no one can read it while its passing through the request.
            'password': {'write_only': True}
        }

    #Whenver we register a user we have to save it inside the Account model.
    def save(self):
        account = Account(
            #These validated data becomes available after it checks that the data is valid. If you dont check its valid, then you wont get the validated data.
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        #if both pass doesnt match, return a json that says 'Password must match'.
        if password != password2:
            raise serializers.ValidationError({'password': "Password must match"}) 
        account.set_password(password) #If the pass match then save the password in the account
        account.save()
        return account
