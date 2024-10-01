from django.shortcuts import render
from account.models import Account

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

    accounts = Account.objects.all()
    context['accounts'] = accounts

    return render(request, 'personal/home.html', context)