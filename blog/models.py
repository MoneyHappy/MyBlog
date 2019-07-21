from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.contrib.contenttypes.models import ContentType
from readCount.models import ReadNum



class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='题目')
    blogType = models.ForeignKey("BlogType", on_delete=models.DO_NOTHING, verbose_name='分类') #加引号就不必担心关联顺序
    # content = models.TextField()
    content = UEditorField(u'内容	',width=1000, height=300, toolbars="full", imagePath="",
                           filePath="", upload_settings={"imageMaxSize":1024000},
                           settings={},command=None,blank=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') #第一次创建时
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最后更新时间') #最后修改时

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)  # <ContentType: blog>
            readNumObj = ReadNum.objects.filter(content_type=ct, object_id=self.id).first() #<ReadNum: ReadNum object (1)>
            return readNumObj.read_num
        except:
            return 0
    get_read_num.short_description='阅读数' #admin中显示的列标题

    def __str__(self):
        return self.title



class BlogType(models.Model):
    typeName = models.CharField(max_length=20)

    def __str__(self):
        return self.typeName
