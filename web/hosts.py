from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
                         host('www', settings.ROOT_URLCONF, name='www'),# <-- The `name` we used to in the `DEFAULT_HOST` setting
                         host('twitchfilter', 'twitchfilter.urls', name='twitchfilter'),
                         host('help', 'help.urls', name='help'),

                         )
