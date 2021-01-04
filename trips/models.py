# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Manager(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager'


class Post(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post = models.CharField(max_length=45, blank=True, null=True)
    rainfall = models.ForeignKey('TestRainfall', models.DO_NOTHING, db_column='rainfall_ID', blank=True, null=True)  # Field name made lowercase.
    table1 = models.ForeignKey('Table1', models.DO_NOTHING, db_column='table1_ID', blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class Report(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post = models.CharField(max_length=200, blank=True, null=True)
    table1 = models.ForeignKey('Table1', models.DO_NOTHING, db_column='table1_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'report'


class Table1(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    text = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table1'


class TestRainfall(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_rainfall'


class Tmp(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp'


class Tmp2(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    rainfall = models.FloatField(db_column='Rainfall', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp2'


class Tmp3(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    rainfall = models.FloatField(db_column='Rainfall', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp3'


class Tmp4(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    rainfall = models.FloatField(db_column='Rainfall', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp4'


class Tmp5(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month', blank=True, null=True)  # Field name made lowercase.
    rainfall = models.FloatField(db_column='Rainfall', blank=True, null=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tmp5'


class TripsPost(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'trips_post'
