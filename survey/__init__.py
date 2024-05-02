from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'complex_form_layout'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField()
    gender = models.StringField(choices=["female","male","diverse", "other"])
    preference = models.StringField(widget=widgets.RadioSelect, choices=[["wrp","Wrap"], ["brt","Burrito"], ["flf","Falafel"] ])
    consent = models.IntegerField(
        choices=[(1, 'Ich stimme zu'), (2, 'Ich stimme nicht zu')],
        widget=widgets.RadioSelect
    )


    

# PAGES
# Hier steht ein bedeutungsloser KOmmentar
class MyPage(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'preference']

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def error_message(self, values):
        if values['consent'] != 1:
            return "Sie müssen zustimmen, um fortzufahren."
        
class Introduction(Page):
    form_model = 'player'

page_sequence = [MyPage, Consent, Introduction]

