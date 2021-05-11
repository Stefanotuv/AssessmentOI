

# Create your models here.

from django.db import models
# from PIL import Image

class Question(models.Model):


    # question = models.CharField(max_length=600)
    question = models.TextField(default="", null=True)

    QUESTION_TYPES = (
            ('Single Selection', 'Single Selection'),
            ('Multi Selection', 'Multi Selection'),
            ('Essay', 'Essay'),
    )

    NUMBER_OF_SELECTIONS = (
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
    )

    YES_NO = (
            ('Yes', 'Yes'),
            ('No', 'No'),
    )

    question_type = models.CharField(max_length=20, blank=False, null=False, choices=QUESTION_TYPES)

    number_of_selection = models.CharField(max_length=20, blank=False, null=False, choices=NUMBER_OF_SELECTIONS)

    answer_1 = models.TextField(default="", null=True)
    answer_1_value = models.CharField(max_length=3, blank=True, null=True, choices=YES_NO)

    answer_2 = models.TextField(default="", blank=True,null=True)
    answer_2_value = models.CharField(max_length=3, blank=True, null=True, choices=YES_NO)

    answer_3 = models.TextField(default="", blank=True, null=True)
    answer_3_value = models.CharField(max_length=3, blank=True, null=True, choices=YES_NO)

    answer_4 = models.TextField(default="",blank=True, null=True)
    answer_4_value = models.CharField(max_length=3, blank=True, null=True, choices=YES_NO)

    answer_5 = models.TextField(default="", blank=True, null=True)
    answer_5_value = models.CharField(max_length=20, blank=True, null=True, choices=YES_NO)

    # image = models.ImageField(default='default.jpg', upload_to='questions_pics')



    def __str__(self):
        return '%s' % (self.pk)

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
    #
    #     img = Image.open(self.image.path )
    #
    #     if img.height > 300 or img.weight >300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img = Image.open(self.image.path)

class Assessment(models.Model):

    YES_NO = ( ('Yes', 'Yes'), ('No', 'No'),)
    assessment_name = models.CharField(max_length=20, blank=True, null=True, unique=True)
    # candidate basic info
    candidate_name = models.CharField(max_length=20, blank=True, null=True)
    candidate_surname = models.CharField(max_length=20, blank=True, null=True)
    candidate_email = models.EmailField(max_length=254, null=True, blank=True)
    slug = models.SlugField(max_length=40,null=True, blank=True)
    token = models.CharField(max_length=256, null=True, blank=True)

    # team member's email (who created the assessment)
    creator_email = models.EmailField(max_length=254, null=True, blank=True)

    date_creation = models.DateTimeField(blank=True, null=True,)
    date_sent = models.DateTimeField(blank=True, null=True,)
    date_first_opened = models.DateTimeField(blank=True, null=True,)
    date_complete = models.DateTimeField(blank=True, null=True,)

    questions_selected = models.ManyToManyField(Question,null=True,blank=True)

    completed = models.CharField(max_length=3, blank=True, null=True, choices=YES_NO)

    answers = models.JSONField()

    def __str__(self):
        return '%s' % (self.assessment_name)


