from django.http import HttpResponse
from django.shortcuts import render
from mi_user.models import mi_class
# Create your views here.
def mi_index(request):
    show_class_all = mi_class.objects.all()[:8]
    show_class = []
    for i in show_class_all:
        show_class.append(i)
    return render(request, 'index.html', {'show_class':show_class})