# Django Admin Theme

## Credit

This admin theme is inspired by https://github.com/douglasmiranda/django-admin-bootstrap
so most of the credit goes to @douglasmiranda.

## Installation

    git clone https://github.com/mariusionescu/console_admin.git
    cd console_admin
    python setup.py install

## Configuration

Add 'console_admin' in INSTALLED_APPS, before Django Admin:

    INSTALLED_APPS = (
        'console_admin',
        ...
    )
Add 'django.core.context_processors.request' to TEMPLATE_CONTEXT_PROCESSORS:

    TEMPLATE_CONTEXT_PROCESSORS = (
        ....
        'django.core.context_processors.request',
        ...
    )

Add in your settings.py:

    ADMIN_MENU = [
        {
            'name': 'Menu entry name',
            'models': [
                'DjangoModel',
                'AnotherDjangoModel',
                # Or you can add an external (or internal) URL:
                # ('URL', 'https://google.com/')
            ],
            'icon':'icon-stack'
        }
    ]
    BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
    CONSOLE_ADMIN_APP_NAME = 'My Application'
    CONSOLE_ADMIN_APP_LOGO_URL = '/static/img/logo.png'


