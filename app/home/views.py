import logging
from django.shortcuts import render

logger = logging.getLogger('app')


def home_view(request):
    # View: /
    return render(request, 'home.html')
