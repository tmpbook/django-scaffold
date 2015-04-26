###**What is it?**
-----------------
This app does all the groundwork(`forms.py`, `urls.py`, `templates/appname/*.html`, `views.py`) needed to running a app which you can *create, list, edit, view* a ModelForm.

Usage:

 - Include django-scaffold as a newly created app in your list of installed apps in `settings.py` .
```python
 INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django-scaffold',
    ...
)
```
 - Create the `models.py` file for your app with all the fields specified.

###**How to use?**
-----------------
Run the following command:
```python
$ python manage.py groundwork <projectname> <appname> <modelname1> <modelname2> ..

# you can see it by using the commond below.
$ manage.py help

```
