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

    frage_5 = models.IntegerField(
        label="Ich fühle mich verpflichtet, umweltfreundlich zu handeln, was meine Ernährung betrifft.",
        choices=[
            [1, 'Extrem unzutreffend'],
            [2, 'Sehr unzutreffend'],
            [3, 'Unzutreffend'],
            [4, 'Weder noch'],
            [5, 'Zutreffend'],
            [6, 'Sehr zutreffend'],
            [7, 'Extrem zutreffend']
        ],
        widget=widgets.RadioSelect
    )

    frage_6 = models.IntegerField(
        label="Ich finde es wichtig, dass sich Menschen im Allgemeinen umweltfreundlich ernähren.",
        choices=[
            [1, 'Extrem unzutreffend'],
            [2, 'Sehr unzutreffend'],
            [3, 'Unzutreffend'],
            [4, 'Weder noch'],
            [5, 'Zutreffend'],
            [6, 'Sehr zutreffend'],
            [7, 'Extrem zutreffend']
        ],
        widget=widgets.RadioSelect
    )

    frage_7 = models.IntegerField(
        label="Wie sehr bemühen sich Ihre Familie und Freunde, den Klimawandel zu reduzieren?",
        choices=[
            [1, 'Keine Bemühungen'],
            [2, 'Wenige Bemühungen'],
            [3, 'Mässige Bemühungen'],
            [4, 'Grosse Bemühungen'],
            [5, 'Sehr grosse Bemühungen']
        ],
        widget=widgets.RadioSelect
    )

    frage_8 = models.IntegerField(
        label="Wie wichtig ist es Ihrer Familie und Ihren Freunden, dass Sie Massnahmen zur Reduzierung des Klimawandels ergreifen?",
        choices=[
            [1, 'Überhaupt nicht wichtig'],
            [2, 'Wenig wichtig'],
            [3, 'Mässig wichtig'],
            [4, 'Wichtig'],
            [5, 'Extrem wichtig']
        ],
        widget=widgets.RadioSelect
    )


# PAGES
class NEPR(Page):
    form_model = 'player'
    form_fields = ['frage_1', 'frage_2', 'frage_3', 'frage_4', 'frage_5', 'frage_6', 'frage_7', 'frage_8']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [NEPR]
