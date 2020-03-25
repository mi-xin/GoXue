from django.http import HttpResponse
from django.shortcuts import render
from mi_class.models import mi_class
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage
# Create your views here.
# 返回首页视图
def mi_index(request):
    show_class_all = mi_class.objects.filter(is_active=True,is_release=True)
    paginator = Paginator(show_class_all, 4, 0)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index', '1')
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'page':number,'paginator':paginator})

# 返回首页课程分页视图
# def mi_page(request,index):
#     show_class_all = mi_class.objects.all()
#     paginator = Paginator(show_class_all, 1, 0)
#     try:
#         # 获取index的值，如果没有，则设置使用默认值1
#         num = request.GET.get('index', '1')
#         # 获取第几页
#         number = paginator.page(num)
#     except PageNotAnInteger:
#         # 如果输入的页码数不是整数，那么显示第一页数据
#         number = paginator.page(1)
#     except EmptyPage:
#         number = paginator.page(paginator.num_pages)
#     return render(request, 'index.html', {'page': number, 'paginator': paginator})