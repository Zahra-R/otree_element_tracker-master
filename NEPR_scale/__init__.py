from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'NEPR_scale'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    frage_1 = models.IntegerField(
        label="Wir müssen das empfindliche Gleichgewicht des Klimas schützen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Stimme eher nicht zu'],
            [4, 'Stimme eher zu'],
            [5, 'Stimme zu'],
            [6, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_2 = models.IntegerField(
        label="Klimaschutz ist wichtig für unsere Zukunft.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Stimme eher nicht zu'],
            [4, 'Stimme eher zu'],
            [5, 'Stimme zu'],
            [6, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_3 = models.IntegerField(
        label="Ich mache mir Sorgen um den Zustand des Klimas.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Stimme eher nicht zu'],
            [4, 'Stimme eher zu'],
            [5, 'Stimme zu'],
            [6, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_4 = models.IntegerField(
        label="Der Klimawandel hat schwerwiegende Folgen für Menschen und die Natur.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Stimme eher nicht zu'],
            [4, 'Stimme eher zu'],
            [5, 'Stimme zu'],
            [6, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )


# PAGES
class NEPR(Page):
    form_model = 'player'
    form_fields = ['frage_1', 'frage_2', 'frage_3', 'frage_4']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [NEPR]
