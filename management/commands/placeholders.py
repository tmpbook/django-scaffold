# coding:utf8
# -------------------- #
# urls.py file section #
# -------------------- #


URL_IMPORTS = """
from django.conf.urls import url
from .models import *
from .views import *

urlpatterns = [
"""
URL_CONFIG = """
    # %(model)s url config
    url(r'%(model)s/create/$', %(modelClass)sCreateView.as_view(),
        name='%(model)s-create'),
    url(r'%(model)s/list/$', %(modelClass)sListView.as_view(),
        name='%(model)s-list'),
    url(r'%(model)s/edit/(?P<pk>\w+)/$', %(modelClass)sUpdateView.as_view(),
        name='%(model)s-edit'),
    url(r'%(model)s/view/(?P<slug>[-\w]+)/$', %(modelClass)sDetailView.as_view(),
        name='%(model)s-detail'),
"""

URL_END = """
]
"""


# --------------------- #
# forms.py file section #
# --------------------- #

FORMS_IMPORTS = """
from django import forms
from .models import *

"""

FORMS_MODELFORM_CONFIG = """
class %(modelClass)sForm(forms.ModelForm):

    class Meta:
        model = %(modelClass)s
        # fields = '__all__'
        exclude = []
        # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(%(modelClass)sForm, self).__init__(*args, **kwargs)

"""


# --------------------- #
# views.py file section #
# --------------------- #

VIEWS_IMPORTS = """
# Create your views here.

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone

# app specific

from .models import *
from .forms import *
"""

VIEWS_CREATE = """
class %(modelClass)sCreateView(CreateView):
    template_name = '%(app)s/create_%(model)s.html'
    model = %(modelClass)s
    fields = '__all__'
    # or ['name', 'description', ]

    def get_success_url(self):
        return reverse_lazy("%(app)s:%(model)s-list")
"""

VIEWS_LIST = """
class %(modelClass)sListView(ListView):
    template_name = '%(app)s/list_%(model)s.html'
    model = %(modelClass)s
    paginate_by = 5
"""

VIEWS_UPDATE = """
class %(modelClass)sUpdateView(UpdateView):
    template_name = '%(app)s/edit_%(model)s.html'
    model = %(modelClass)s
    fields = '__all__'
    # or ['name', 'description', ]

    def get_success_url(self):
        return reverse_lazy("%(app)s:%(model)s-list")
"""

VIEWS_DETAIL = """
class %(modelClass)sDetailView(DetailView):
    template_name = '%(app)s/detail_%(model)s.html'
    model = %(modelClass)s

    def get_context_data(self, **kwargs):
        context = super(%(modelClass)sDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
"""


# ------------------------- #
# templates.py file section #
# ------------------------- #


TEMPLATES_CREATE = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%}
    <h1> %(modelClass)s </h1> <h2> Create </h2>
{%% endblock %%}

{%% block content %%}
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Create"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_LIST = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s List  {%% endblock %%}

{%% block heading %%}
    <h1> %(modelClass)s </h1> <h2> List </h2>
{%% endblock %%}

{%% block content %%}
<table>
<thead>
<tr><th>Record</th><th colspan="3">Actions</th></tr>
{%% for item in object_list %%}
  <tr><td>  {{item}}</td> <td><a href="{%% url "%(app)s:%(model)s-detail" pk=item.id %%}">Show</a> </td> <td><a href="{%% url "%(app)s:%(model)s-edit" pk=item.id %%}">Edit</a></tr>
{%% endfor %%}
<tr><td colspan="3"> <a href="{%% url "%(app)s:%(model)s-create" %%}">Add New</a></td></tr>
</table>

<div align="center">
{%% if page_obj.has_previous %%}
    <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
{%% endif %%}

<span class="current">
    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
</span>

{%% if page_obj.has_next %%}
        <a href="?page={{ page_obj.next_page_number }}">Next</a>
{%% endif %%}

</div>
{%% endblock %%}
"""


TEMPLATES_EDIT = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s Edit {%% endblock %%}

{%% block heading %%}
    <h1> %(modelClass)s </h1> <h2> Edit </h2>
{%% endblock %%}

{%% block content %%}
    <form action="" method="POST"> {%% csrf_token %%}
        {{ form }}
        <input type="submit" value="Save"/>
    </form>
{%% endblock %%}
"""

TEMPLATES_VIEW = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s View {%% endblock %%}

{%% block heading %%}
    <h1> %(modelClass)s </h1> <h2> Detail </h2>
{%% endblock %%}

{%% block content %%}
    <table>
        {{ object }}
    </table>
{%% endblock %%}
"""

TEMPLATES_BASE = """
{% load staticfiles %}
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <!--<meta http-equiv="refresh" content="60">-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->

    {% block title %}
        <title>主页</title>
    {% endblock %}

    {% block css %}
    {% endblock %}
    
    {% block script %}
    {% endblock %}
    
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="http://cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="http://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    {% block content %}
        This is the base.html
    {% endblock %}
  </body>
"""
