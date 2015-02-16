# Django Admin Theme

This admin theme is inspired by https://github.com/douglasmiranda/django-admin-bootstrap
so most of the credit goes to @douglasmiranda.

Please configure in your settings.py:

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
