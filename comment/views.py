from django.shortcuts import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
import json
from django.views.decorators.csrf import csrf_exempt

def submitComment(request):
    showComment = {}
    comment_user = request.user
    comment_text = request.POST.get('comment_text').strip()
    if comment_text == '':
        showComment['status'] = 0
        return HttpResponse(json.dumps(showComment))
    content_type = request.POST.get('content_type')
    object_id = int(request.POST.get('object_id'))
    model_class = ContentType.objects.get(model=content_type).model_class()#得到Blog这个模型

    #评论存入数据库
    comment = Comment()
    comment.comment_user = comment_user
    comment.comment_text = comment_text
    comment.content_object = model_class.objects.get(id=object_id)
    comment.save()
    #ajax提交评论
    showComment['comment_user'] = comment.comment_user.username
    showComment['comment_text'] = comment_text
    showComment['comment_time'] = comment.comment_time.now().strftime('%Y-%m-%d %H:%M')
    showComment['commentID'] = comment.id
    return HttpResponse(json.dumps(showComment))

@csrf_exempt
def removeComment(request):
    commentID = request.POST.get('commentID')
    Comment.objects.filter(id=commentID).delete()
    return HttpResponse()
