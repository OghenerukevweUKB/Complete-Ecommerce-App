from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage

# from django.http import HttpResponse
# from django.db.models import Q , F
# from django.db.models.aggregates import Count, Max, Min, Avg
# from django.db.models import Value , ExpressionWrapper
# from django.db import transaction
# from store.models import Product, OrderItem, Order, Customer , Collection
# from tags.models import TaggedItem
# from django.contrib.contenttypes.models import ContentType


def say_hello(request):
    try:
        message= BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Oghenerukevwe'}
        )
        message.send(['precious@gmail.com'])
    except BadHeaderError:
        pass    
    return render(request, 'hello.html', {'name': 'Rukky'})
    