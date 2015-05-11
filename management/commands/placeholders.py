# -------------------- #
# urls.py file section #
# -------------------- #


URL_IMPORTS = """
from django.conf.urls import patterns, include, url
from .models import *
from .views import *

urlpatterns = patterns('',
"""

URL_CRUD_CONFIG = """
    url(r'%(model)s/create/$', %(modelClass)sCreateView.as_view(), name='%(model)s-create'),
    url(r'%(model)s/list/$', %(modelClass)sListView.as_view(), name='%(model)s-list'),
    url(r'%(model)s/edit/(?P<pk>[^/]+)/$', %(modelClass)sUpdateView.as_view(), name='%(model)s-edit'),
    url(r'%(model)s/view/(?P<pk>[^/]+)/$', %(modelClass)sDetailView.as_view(), name='%(model)s-detail'),
    """ 

URL_END = """
)
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
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(%(modelClass)sForm, self).__init__(*args, **kwargs)

"""        





# --------------------- #
# views.py file section #
# --------------------- #

VIEWS_IMPORTS = """
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

# app specific files

from .models import *
from .forms import *
"""

VIEWS_CREATE = """
class %(modelClass)sCreateView(CreateView):
    template_name = '%(app)s/create_%(model)s.html'
    model = %(modelClass)s
    # fields = ['name', 'salutation'] #your choice
    
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
    
    def get_success_url(self):
        return reverse_lazy("%(app)s:%(model)s-list")
        
def edit_%(model)s(request, pk):

    %(model)s_instance = %(modelClass)s.objects.get(id=pk)

    form = %(modelClass)sForm(request.POST or None, instance = %(model)s_instance)

    if form.is_valid():
        form.save()

    t=get_template('%(app)s/edit_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""

VIEWS_DETAIL = """

class %(modelClass)sDetailView(DetailView):
    template_name = '%(app)s/detail_%(model)s.html'
    model = %(modelClass)s

    
def view_%(model)s(request, pk):
    %(model)s_instance = %(modelClass)s.objects.get(id = pk)

    t=get_template('%(app)s/view_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""


# ------------------------- #
# templates.py file section #
# ------------------------- #



TEMPLATES_CREATE = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%} <h1>%(modelClass)s </h1> <h2> Create </h2> {%% endblock %%}
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

{%% block heading %%} <h1> %(modelClass)s </h1> <h2> List </h2> {%% endblock %%}
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

{%% block heading %%} <h1> %(modelClass)s </h1> <h2> Edit </h2>  {%% endblock %%}
{%% block content %%} 
<table>
<form action="" method="POST"> {%% csrf_token %%}
  {{form}}
  <tr>
    <td colspan="2" align="right"><input type="submit" value="Save"/></td>
  </tr>
</form>
</table>
{%% endblock %%}
"""

TEMPLATES_VIEW = """
{%% extends "base.html" %%}

{%% block title %%} %(modelClass)s View {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s </h1> <h2> Detail </h2> {%% endblock %%}
{%% block content %%} 
<table>
{{ object }}
</table>
{%% endblock %%}
"""

TEMPLATES_BASE = """
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="" />
    <meta name="keywords" content="" />
    <meta name="author" content="tmpbook" />
    <title>
        {% block title %} {% endblock %}
    </title>
      <style type="text/css"> 
        html * { padding:0; margin:0; }
        body * { padding:10px 20px; }
        body * * { padding:0; }
        body { font:small sans-serif; }
        body>div { border-bottom:1px solid #ddd; }
        h1 { font-weight:normal; }
        h2 { margin-bottom:.8em; }
        h2 span { font-size:80% ; color:#666; font-weight:normal; }
        h3 { margin:1em 0 .5em 0; }
        h4 { margin:0 0 .5em 0; font-weight: normal; }
        td {font-size:1em;  padding:3px 17px 2px 17px;}
        ul { margin-left: 2em; margin-top: 1em; }
        #summary { background: #e0ebff; }
        #summary h2 { font-weight: normal; color: #666; }
        #explanation { background:#eee; }
        #content { background:#f6f6f6; }
        #summary table { border:none; background:transparent; }
      </style> 
</head>
<body>


<div id="summary">
{% block heading %}  
{% endblock %}
</div>

<div id="content">
{% block content %} 


{% endblock %}
</div>

<div id="explanation" align="center">
  https://github.com/tmpbook/django-scaffold.git
</div>

</body>
</html>
"""

