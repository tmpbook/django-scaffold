# coding:utf8
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from placeholders import *
import os


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('project_name', type=str)
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name_list', nargs='+', type=str)
        # nargs='+' means that argument is a list.

    def handle(self, *args, **options):
        print "start"
        project = options['project_name']
        # Project name is the first parameter
        app = options['app_name']
        # App name is the second parameter
        model_list = options['model_name_list']
        # Models which need to be scaffolded will follow
        print 'PROJECT:' + str(project)
        print 'APP:' + str(app)
        print 'MODELS:{0}'.format(model_list)
        PROJECT_ROOT = os.getcwd()
        TEMPLATE_DIR = os.path.join(PROJECT_ROOT, app, 'templates')

        model_instances = []
        for model in model_list:
            try:
                model_instances.append(models.get_model(app, model))
            except:
                raise CommandError('"%s" model does not exist' % model)
            # url config
            urls = URL_IMPORTS

            # Generate CRUD urls for each model
            for model_instance in model_instances:
                urls += URL_CONFIG % {
                    'model': model_instance._meta.object_name.lower(),
                    'modelClass': model_instance._meta.object_name,
                }

        urls += URL_END

        # write the app's urls.py
        f = open(os.path.join(PROJECT_ROOT, app, 'urls.py'), 'w')
        f.write(urls)
        f.close()

        # append to root urlconf
        f = open(os.path.join(PROJECT_ROOT, project, 'urls.py'), 'a')
        f.write("\n\n# Added by django-scaffold")
        f.write("\nurlpatterns += [\n    url(r'^%(app)s/', include('%(app)s.urls', namespace='%(app)s')),\n]" % {'app': app})
        f.close()

        # forms.py
        forms_content = FORMS_IMPORTS
        for model_instance in model_instances:
            forms_content += FORMS_MODELFORM_CONFIG % {
                'modelClass': model_instance._meta.object_name
            }

        formspath = os.path.join(PROJECT_ROOT, app, 'forms.py')
        f = open(formspath, 'w')
        f.write(forms_content)
        f.close()

        # views.py
        views_content = VIEWS_IMPORTS

        for model_instance in model_instances:
            views_content += VIEWS_CREATE
            views_content += VIEWS_LIST
            views_content += VIEWS_DETAIL
            views_content += VIEWS_UPDATE

            views_content = views_content % {
                'model': model_instance._meta.object_name.lower(),
                'modelClass': model_instance._meta.object_name, 'app': app
            }

        # write to views.py
        viewspath = os.path.join(PROJECT_ROOT, app, 'views.py')
        f = open(viewspath, 'w')
        f.write(views_content)
        f.close()

        # Templates
        template_dir = os.path.join(TEMPLATE_DIR, app)
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)

        print "Generate base template? [Y/N]?"
        yn = raw_input()
        if yn.lower() == 'y':
            f = open(os.path.join(TEMPLATE_DIR, 'base.html'), 'w')
            f.write(TEMPLATES_BASE)
            f.close()
        else:
            return

        for model_instance in model_instances:
            f = open(os.path.join(TEMPLATE_DIR, app, 'create_%s.html' % (
                model_instance._meta.object_name.lower())), 'w')
            f.write(TEMPLATES_CREATE % {
                'modelClass': model_instance._meta.object_name
                }
            )
            f.close()

            f = open(os.path.join(TEMPLATE_DIR, app, 'list_%s.html' % (
                model_instance._meta.object_name.lower())), 'w')
            f.write(TEMPLATES_LIST % {
                'modelClass': model_instance._meta.object_name,
                'model': model_instance._meta.object_name.lower(),
                'app': app
                }
            )
            f.close()

            f = open(os.path.join(TEMPLATE_DIR, app, 'edit_%s.html' % (
                model_instance._meta.object_name.lower())), 'w')
            f.write(TEMPLATES_EDIT %
                    {'modelClass': model_instance._meta.object_name})
            f.close()

            f = open(os.path.join(TEMPLATE_DIR, app, 'detail_%s.html' % (
                model_instance._meta.object_name.lower())), 'w')
            f.write(TEMPLATES_VIEW % {
                    'modelClass': model_instance._meta.object_name,
                    'model': model_instance._meta.object_name.lower()})
            f.close()
