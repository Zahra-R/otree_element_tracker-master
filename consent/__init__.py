from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.BooleanField(
        label="Ich stimme zu",
        widget=widgets.CheckboxInput
    )

class consentpage(Page):
    form_model = 'player'
    form_fields = ['consent']

    def error_message(self, values):
        if values['consent'] != 1:
            return "Bitte stimmen Sie zu, um fortzufahren."

page_sequence = [consentpage]

