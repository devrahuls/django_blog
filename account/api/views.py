# from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from account.api.serializers import RegisterSerializer

@api_view(['POST', ])
def api_registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save() #It saves the new user via the RegisterSerializer.
            data['response'] = "Successfully created a new user!"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


# @api_view(['GET', ])
# def account_detail_view(request):

#     #If the account exists
#     try:
#         account = Account.objects.get(pk=1)
#     except Account.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = AccountSerializer(account)
#         return Response(serializer.data)
