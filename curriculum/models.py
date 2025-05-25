from django.db import models
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from embed_video.fields import EmbedVideoField


class Session(models.Model):
    name = models.CharField(max_length=50)

    first_term = 'First Term'
    second_term = 'Second Term'
    third_term = 'Third Term'
    others = 'Others'

    term_status = [
        (first_term, 'First Term'),
        (second_term, 'Second Term'),
        (third_term, 'Third Term'),
        (others, 'Others'),

    ]

    term = models.CharField(max_length=15, choices=term_status, blank=True, null=True, default='First Term')
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    desc = models.TextField(max_length=100, blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        unique_together = ['name', 'term']

    def __str__(self):
        return f"{self.name} - {self.term}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# school departments e.g pre-nursery, nursery, junior sec, senior sec

class Dept(models.Model):
    id = models.CharField(primary_key='True', max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# academic subjects
class Subject(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    id = models.CharField(primary_key='True', max_length=50)
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50, default='X')

    def __str__(self):
        return self.name


class Class(models.Model):
    # courses = models.ManyToManyField(Course, default=1)
    id = models.CharField(primary_key='True', max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    sem = models.IntegerField()

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        d = Dept.objects.get(name=self.dept)
        return '%s : %d %s' % (d.name, self.sem, self.section)
    


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get file name
    if instance.lesson_id:
        filename = 'lesson_files/{}.{}'.format(instance.lesson_id,instance.lesson_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(instance.lesson_id,new_name, ext)
    
    return os.path.join(upload_to, filename)



class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    # video = models.FileField(upload_to=save_lesson_files, verbose_name="video", blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True)
    # video = models.CharField(max_length=500, blank=True)
    # video_url = EmbedVideoField(null=True,blank=True)
    # ppt = models.FileField(upload_to='save_lesson_files', verbose_name="Presentation", blank=True)
    Notes = models.FileField(upload_to='save_lesson_files', verbose_name="Notes", blank=True)
    #comment = RichTextField(blank=True, null=True)
    comment = CKEditor5Field('Text', config_name='extends')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lesson_list', kwargs={'slug':self.subject.slug, 'standard':self.standard.slug})

    @property
    def html_stripped(self):
       
       return strip_tags(self.comment)
            

# comment module
class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models. CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("comment", null=True, blank=True, on_delete=CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']


class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to" + str(self.comment_name.comm_name)