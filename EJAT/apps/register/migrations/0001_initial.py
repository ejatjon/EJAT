# Generated by Django 3.2.5 on 2021-09-11 08:20

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile_phone', models.CharField(blank=True, max_length=11, verbose_name='mobile_phone')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'index_together': {('username', 'email', 'date_joined', 'mobile_phone', 'id', 'last_login', 'first_name')},
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='user_data/moments/%Y/%m/%d')),
            ],
            options={
                'index_together': {('id',)},
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('introduce', models.TextField(blank=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('user_image', models.ImageField(default='user_data/user_head_portrait/default.jpg', upload_to='user_data/user_head_portrait/%Y/%m/%d')),
                ('user_background_image', models.ImageField(default='user_data/user_background_images/default.jpg', upload_to='user_data/user_background_images/%Y/%m/%d')),
                ('Country', models.CharField(blank=True, max_length=120)),
                ('nationality', models.CharField(blank=True, max_length=120)),
                ('mother_tongue', models.CharField(blank=True, max_length=120)),
                ('language_learned_list', models.CharField(blank=True, max_length=350)),
                ('company', models.CharField(blank=True, max_length=220)),
                ('religion', models.CharField(blank=True, max_length=220)),
                ('education', models.CharField(blank=True, max_length=120)),
                ('gender', models.CharField(choices=[('Male', 'male'), ('female', 'female'), ('unknown', 'unknown')], default='unknown', max_length=120)),
                ('grade', models.CharField(choices=[('lv1', 'lv1'), ('lv2', 'lv2'), ('lv3', 'lv3'), ('lv4', 'lv4'), ('lv5', 'lv5'), ('lv6', 'lv6')], default='lv1', max_length=120)),
                ('points_earned', models.IntegerField(default=0)),
                ('images', models.ManyToManyField(blank=True, to='register.Images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'index_together': {('nationality', 'mother_tongue', 'religion', 'education', 'points_earned')},
            },
        ),
        migrations.CreateModel(
            name='Moments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('images', models.ManyToManyField(blank=True, to='register.Images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'index_together': {('id', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Fans',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('on_time', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL, verbose_name='from_user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='to_user')),
            ],
            options={
                'index_together': {('id', 'from_user', 'to_user', 'on_time')},
            },
        ),
    ]