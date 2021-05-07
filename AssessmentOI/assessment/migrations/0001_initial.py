# Generated by Django 3.2.1 on 2021-05-04 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=600)),
                ('question_type', models.CharField(blank=True, choices=[('Single Selection', 'Single Selection'), ('Multi Selection', 'Multi Selection'), ('Essay', 'Essay')], max_length=20, null=True)),
                ('number_of_selection', models.CharField(blank=True, choices=[('Single Selection', 'Single Selection'), ('Multi Selection', 'Multi Selection'), ('Essay', 'Essay')], max_length=20, null=True)),
                ('answer_1', models.CharField(blank=True, max_length=600, null=True)),
                ('answer_1_value', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True)),
                ('answer_2', models.CharField(blank=True, max_length=600, null=True)),
                ('answer_2_value', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True)),
                ('answer_3', models.CharField(blank=True, max_length=600, null=True)),
                ('answer_3_value', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True)),
                ('answer_4', models.CharField(blank=True, max_length=600, null=True)),
                ('answer_4_value', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True)),
                ('answer_5', models.CharField(blank=True, max_length=600, null=True)),
                ('answer_5_value', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20, null=True)),
                ('image', models.ImageField(default='default.jpg', upload_to='questions_pics')),
            ],
        ),
    ]
