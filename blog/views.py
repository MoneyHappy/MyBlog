import datetime
from django.shortcuts import render
from blog import models
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from readCount.models import ReadNum, ReadDate
from comment.models import Comment
from django.utils import timezone
from django.db.models import Sum



# 分页器模块
def myPaginator(objects, current_page, per_page_items, show_page_nums=5):
    '''
    :param objects: 总的一个数据
    :param current_page: 当前所在页码
    :param per_page_items: 每页显示几条数据
    :param show_page_nums: 显示的页码数，默认显示5个页码,要求传入奇数以方便前后对称
    :return:content
    '''
    paginator = Paginator(objects, per_page_items)
    num_pages = paginator.num_pages
    current_page_list = paginator.get_page(current_page)
    per_page_detailItems = current_page_list.object_list
    if num_pages <= show_page_nums:
        show_page_range = range(1, num_pages + 1)
    else:
        if current_page - (show_page_nums + 1) / 2 <= 0:
            show_page_range = range(1, show_page_nums + 1)
        elif (num_pages + 1) - current_page <= (show_page_nums - 1) / 2:
            show_page_range = range(num_pages + 1 - show_page_nums, num_pages + 1)
        else:
            show_page_range = range(current_page - int((show_page_nums - 1) / 2),
                                    current_page + int((show_page_nums - 1) / 2) + 1)
    content = {}
    content['per_page_detailItems'] = per_page_detailItems  # 在前端显示当前页的数据列表
    content['show_page_range'] = show_page_range  # 在前端展示的页码数
    content['current_page'] = current_page  # 当前页
    content['num_pages'] = num_pages  # 总页数
    content['current_page_list'] = current_page_list  # 当前页这个对象
    return content



# 一周阅读数模块
def oneWeek_readNum(content_type):
    today = timezone.now().date()
    oneWeek_readNumList = []
    oneWeekDate = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        oneWeekDate.append(date.strftime('%m/%d'))
        ReadTimeObj = ReadDate.objects.filter(content_type=content_type, read_date=date)
        result = ReadTimeObj.aggregate(readNumSum=Sum('read_num'))  # 字典{'readNumSum':values}
        oneWeek_readNumList.append(result['readNumSum'] or 0)
    return oneWeek_readNumList, oneWeekDate



def blogHome(request):
    '''博客首页'''
    blogs = models.Blog.objects.all().order_by('-id')
    if request.GET.get('p') == None:
        current_page = 1
    else:
        current_page = int(request.GET.get('p'))
    content = myPaginator(blogs, current_page, 5)
    #一周阅读数统计
    ct = ContentType.objects.get_for_model(models.Blog)
    oneWeek_readNumList, oneWeekDate = oneWeek_readNum(ct)
    #阅读排行版
    hotBlogs = ReadNum.objects.all().order_by('-read_num')[:7]

    content['hotBlogs'] = hotBlogs
    content['blogs'] = blogs
    content['types'] = models.BlogType.objects.all()
    content['oneWeek_readNumList'] = oneWeek_readNumList
    content['oneWeekDate'] = oneWeekDate
    return render(request, 'blogHome.html', content)



def blogWithType(request, type_id):
    '''处理分类'''
    typeName = models.BlogType.objects.filter(id=type_id).first()
    blogs = typeName.blog_set.all().order_by('-id') # 获取这个类下的所有博客(反查)
    if request.GET.get('p') == None:
        current_page = 1
    else:
        current_page = int(request.GET.get('p'))
    content = myPaginator(blogs, current_page, 3)
    # 一周阅读数统计
    ct = ContentType.objects.get_for_model(models.Blog)
    oneWeek_readNumList, oneWeekDate = oneWeek_readNum(ct)
    # 阅读排行版
    hotBlogs = ReadNum.objects.all().order_by('-read_num')[:7]

    content['hotBlogs'] = hotBlogs
    content['types'] = models.BlogType.objects.all()
    content['typeName'] = typeName
    content['blogs'] = blogs
    content['oneWeek_readNumList'] = oneWeek_readNumList
    content['oneWeekDate'] = oneWeekDate
    return render(request, 'blogWithType.html', content)



def blogDetail(request, blog_id):
    '''具体显示某篇博客'''
    content = {}
    blogs = models.Blog.objects.filter(id=blog_id)
    content['blogs'] = blogs
    content['types'] = models.BlogType.objects.all()
    ct = ContentType.objects.get_for_model(models.Blog)
    #处理博客的阅读计数
    if request.COOKIES.get('blog_id:%s' % blog_id) != 'haveRead':
        # ct = ContentType.objects.get_for_model(models.Blog)
        readNumObj, created = ReadNum.objects.get_or_create(content_type=ct, object_id=blog_id)
        readNumObj.read_num += 1
        readNumObj.save()

        read_date = timezone.now().date()
        readDateObj, created = ReadDate.objects.get_or_create(content_type=ct, object_id=blog_id, read_date=read_date)
        readDateObj.read_num += 1
        readDateObj.save()
    # 处理上一篇下一篇
    pre_blogSet = models.Blog.objects.filter(id__lt=blog_id).order_by('id')
    next_blogSet = models.Blog.objects.filter(id__gt=blog_id).order_by('id')
    if pre_blogSet.count() > 0:
        pre_blog = pre_blogSet.last()
    else:
        pre_blog = None
    if next_blogSet.count() > 0:
        next_blog = next_blogSet.first()
    else:
        next_blog = None
    content['pre_blog'] = pre_blog
    content['next_blog'] = next_blog
    # 阅读排行版
    hotBlogs = ReadNum.objects.all().order_by('-read_num')[:7]
    content['hotBlogs'] = hotBlogs
    #评论处理
    comments = Comment.objects.filter(content_type=ct, object_id=blog_id)
    content['comments'] = comments

    response = render(request, 'blogDetail.html', content)
    response.set_cookie('blog_id:%s' % blog_id, 'haveRead', max_age=600)
    return response
