# Generated by Django 3.2.5 on 2021-09-04 06:53

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Show_picture', models.URLField()),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('is_reprint', models.BooleanField()),
                ('creation_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('Likes_num', models.PositiveIntegerField(default=0)),
                ('Forwarded', models.PositiveIntegerField(default=0)),
                ('reply_num', models.PositiveIntegerField(default=0)),
                ('views_num', models.PositiveIntegerField(default=0)),
                ('collect_num', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Article_excerpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_excerpt', models.TextField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article_htmlField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_html', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('index', models.IntegerField(default=999)),
            ],
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('references_id', models.AutoField(primary_key=True, serialize=False)),
                ('references_name', models.CharField(max_length=120)),
                ('references_link', models.URLField()),
            ],
            options={
                'ordering': ['references_id'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('reply_id', models.AutoField(primary_key=True, serialize=False)),
                ('to_reply_id', models.IntegerField(verbose_name='to_reply_id')),
                ('reply', tinymce.models.HTMLField(verbose_name='reply')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='creation_time')),
            ],
            options={
                'ordering': ['reply_id'],
            },
        ),
        migrations.CreateModel(
            name='Reprint',
            fields=[
                ('reprint_id', models.AutoField(primary_key=True, serialize=False)),
                ('reprint_mas', models.CharField(max_length=120)),
                ('reprint_link', models.URLField()),
            ],
            options={
                'ordering': ['reprint_id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='UserArticleData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.article')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
