from django_hosts import patterns, host

host_patterns = patterns('path.to',
    host(r'api', 'CalorieApp.urls', name='api'),
    host(r'beta', 'beta.urls', name='beta'),
)