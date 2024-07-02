from os import environ

SESSION_CONFIGS = [
     dict(
         name='FirstSurvey',
         app_sequence=['introduction', 'tracking_demo', 'memory_task', 'NEPR_scale', 'demographics'],
         num_demo_participants=20,
     ),
     dict(
         name='FirstSurveyduplicate',
         app_sequence=['tracking_demo', 'memory_task', 'NEPR_scale', 'demographics'],
         num_demo_participants=20,
     ),
     dict(
         name='memory',
         app_sequence=[ 'memory_task'],
         num_demo_participants=20,
     ),
     dict(
         name='trackingdemo',
         app_sequence=[ 'tracking_demo'],
         num_demo_participants=20,
     ),
     dict(
         name='demographics',
         app_sequence=[ 'demographics'],
         num_demo_participants=20,
     ),
]

# 'introduction', 'tracking_demo', 'memory_task', 'NEPR_scale', 'demographics'
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [

    'orderStimuli', 
    'comprehensionCheck',
    'comprehensionCheck2'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2191323377724'
