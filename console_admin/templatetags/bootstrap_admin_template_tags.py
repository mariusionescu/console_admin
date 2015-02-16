from django.contrib.admin import site
from django.apps import apps
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.conf import settings
from django import template
register = template.Library()

MAX_LENGTH_BOOTSTRAP_COLUMN = 12


def css_classes_for_field(field, custom_classes):
    orig_class = field.field.widget.attrs.get('class', '')
    required = 'required' if field.field.required else ''
    classes = field.css_classes(' '.join([orig_class, custom_classes, required]))
    return classes


@register.filter()
def get_label(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    return field.label_tag(attrs={'class': classes}, label_suffix='')


@register.filter()
def add_class(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    try:
        # For widgets like SelectMultiple, checkboxselectmultiple
        field.field.widget.widget.attrs.update({'class': classes})
    except:
        field.field.widget.attrs.update({'class': classes})
    return field


@register.filter()
def widget_type(field):
    if isinstance(field, dict):
        return 'adminreadonlyfield'
    try:
        # For widgets like SelectMultiple, checkboxselectmultiple
        widget_type = field.field.widget.widget.__class__.__name__.lower()
    except:
        widget_type = field.field.widget.__class__.__name__.lower()
    return widget_type


@register.filter()
def placeholder(field, placeholder=''):
    field.field.widget.attrs.update({'placeholder': placeholder})
    return field


def sidebar_menu_setting():
    return getattr(settings, 'BOOTSTRAP_ADMIN_SIDEBAR_MENU', False)


@register.assignment_tag
def display_sidebar_menu(has_filters=False):
    if has_filters:
        # Always display the menu in change_list.html
        return True
    return sidebar_menu_setting()


@register.inclusion_tag('bootstrap_admin/sidebar_menu.html',
                        takes_context=True)
def render_menu_app_list(context):
    show_global_menu = sidebar_menu_setting()
    dependency = 'django.core.context_processors.request'
    if not show_global_menu:
        return {'app_list': ''}

    if dependency not in settings.TEMPLATE_CONTEXT_PROCESSORS:
        raise ImproperlyConfigured(
            "bootstrap_admin: in order to use the 'sidebar menu' requires" +
            " the '%s' to be added to settings.TEMPLATE_CONTEXT_PROCESSORS."
            % dependency
        )

    # Code adapted from django.contrib.admin.AdminSite
    app_dict = {}
    user = context.get('user')
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(context.get('request'))

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse(
                            'admin:%s_%s_changelist' % info,
                            current_app=site.name
                        )
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse(
                            'admin:%s_%s_add' % info,
                            current_app=site.name
                        )
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': apps.get_app_config(app_label).verbose_name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=site.name
                        ),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'all_models': []
                    }

    # Sort the apps alphabetically.
    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    # Try to create the menu using the settings.ADMIN_MENU data structure

    if hasattr(settings, 'ADMIN_MENU') and settings.ADMIN_MENU:
        app_list_config = []
        for app_config in settings.ADMIN_MENU:
            app_obj = {'name': None, 'models': [], 'app_url': [], 'all_models': []}
            for app in app_list:
                for model_name in app_config['models']:
                    if type(model_name) in (tuple, list):
                        m = {'name': model_name[0], 'admin_url': model_name[1]}
                        app_obj['name'] = app_config['name']
                        app_obj['icon'] = app_config['icon']
                        app_obj['models'].append(m)
                        app_obj['all_models'].append(m['name'])
                        app_obj['app_url'].append(app_config['name'])
                        continue
                    for m in app['models']:
                        if m['object_name'] == model_name:
                            app_obj['name'] = app_config['name']
                            app_obj['icon'] = app_config['icon']
                            app_obj['models'].append(m)
                            app_obj['app_url'].append(app_config['name'])
                            app_obj['all_models'].append(m['object_name'].lower())
            app_list_config.append(app_obj)
    else:
        app_list_config = app_list

    path = context.get('request').path
    try:
        active_model = path.split('/')[3]
    except IndexError:
        active_model = 'console'

    return {'app_list': app_list_config, 'current_url': context.get('request').path, 'active_model': active_model}


@register.filter()
def class_for_field_boxes(line):
    size_column = MAX_LENGTH_BOOTSTRAP_COLUMN / len(line.fields)
    return 'col-sm-{0}'.format(size_column or 1)  # if '0' replace with 1
