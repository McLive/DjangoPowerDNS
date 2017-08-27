class DatabaseRouter(object):
    """A router to control all database operations on models in
    the 'powerdns_manager' application.

    Based on the default example router of Django 1.4:

        https://docs.djangoproject.com/en/1.4/topics/db/multi-db/#an-example

    It is highly recommended to configure django-powerdns-manager to use a
    different database than the rest of the apps of the Django project for
    security and performance reasons.

    The ``PowerdnsManagerDbRouter`` database router is provided for this
    purpose. All you need to do, is configure an extra database in
    ``settings.py`` named ``powerdns`` and add this router to the
    ``DATABASE_ROUTERS`` list.

    The following example assumes using SQLite databases, but your are free to
    use any database backend you want, provided that it is also supported by
    the PowerDNS server software::

        DATABASES = {
            'default': {    # Used by all apps of the Django project except django-powerdns-manager
                'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'main.db',               # Or path to database file if using sqlite3.
                'USER': '',                      # Not used with sqlite3.
                'PASSWORD': '',                  # Not used with sqlite3.
                'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            },
            'powerdns': {    # Used by django-powerdns-manager and PowerDNS server
                'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'powerdns.db',           # Or path to database file if using sqlite3.
                'USER': '',                      # Not used with sqlite3.
                'PASSWORD': '',                  # Not used with sqlite3.
                'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }
        }
        DATABASE_ROUTERS = ['powerdns_manager.routers.PowerdnsManagerDbRouter']

    The configuration above indicates that ``main.db`` will be used by all
    the apps of the Django project, except ``django-powerdns-manager``. The
    ``powerdns.db`` database will be used by ``django-powerdns-manager``.
    PowerDNS should also be configured to use ``powerdns.db``.

    Run syncdb like this:

        python manage.py syncdb
        python manage.py syncdb --database=powerdns

    """

    def db_for_read(self, model, **hints):
        """Point all operations on powerdns_manager models to 'powerdns'"""
        # raise Exception(hints)
        # raise Exception( 'READ OBJ: ' + str(type(hints['instance'])) + str(hints) )
        if model._meta.app_label == 'auth':
            return 'default'
        elif model._meta.app_label == 'dpdns':
            return 'powerdns'
        return None

    def db_for_write(self, model, **hints):
        """Point all operations on powerdns_manager models to 'powerdns'"""
        if model._meta.app_label == 'auth':
            return 'default'
        elif model._meta.app_label == 'dpdns':
            return 'powerdns'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if a model in powerdns_manager is involved"""
        if obj1._meta.app_label == 'dpdns' or obj2._meta.app_label == 'dpdns':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure the powerdns_manager app only appears on the 'powerdns' db"""
        if db == 'powerdns':
            return app_label == 'dpdns'
        elif app_label == 'dpdns':
            return False
        return None
