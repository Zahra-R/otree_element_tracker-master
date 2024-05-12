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
        label="Wir erreichen bald die Grenze der Bevölkerungszahl, welche die Erde verkraften kann.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_2 = models.IntegerField(
        label="Menschen haben das Recht, die natürliche Umwelt zu verändern, um ihre Bedürfnisse zu stillen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_3 = models.IntegerField(
        label="Wenn Menschen in die Natur eingreifen, so hat das oft katastrophale Konsequenzen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_4 = models.IntegerField(
        label="Der menschliche Einfallsreichtum wird sicherstellen, dass wir die Erde nicht unbewohnbar machen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_5 = models.IntegerField(
        label="Menschen überbeanspruchen die Umwelt in starkem Maße.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_6 = models.IntegerField(
        label="Die Erde hat viele natürliche Ressourcen, wenn wir nur lernen diese zu entwickeln.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_7 = models.IntegerField(
        label="Pflanzen und Tiere haben das gleiche Recht zu existieren wie Menschen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_8 = models.IntegerField(
        label="Das Gleichgewicht der Natur ist stark genug, um mit den Auswirkungen der modernen Industrie-Nationen fertig zu werden.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_9 = models.IntegerField(
        label="Trotz unserer speziellen Fähigkeiten sind wir Menschen immer noch den Gesetzen der Natur unterworfen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_10 = models.IntegerField(
        label="Die sogenannte „Öko-Krise“, welche die Menschheit bedroht, wird stark überschätzt.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_11 = models.IntegerField(
        label="Die Erde ist wie ein Raumschiff mit sehr beschränktem Raum und Ressourcen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_12 = models.IntegerField(
        label="Menschen sind dazu bestimmt, über den Rest der Natur zu bestimmen.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_13 = models.IntegerField(
        label="Das Gleichgewicht der Natur ist sehr empfindlich und leicht gestört.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_14 = models.IntegerField(
        label="Menschen werden irgendwann einmal genügend darüber gelernt haben, wie die Natur funktioniert und in der Lage sein, diese zu kontrollieren.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )

    frage_15 = models.IntegerField(
        label="Wenn die Dinge weiterhin so weitergehen wie jetzt, werden wir bald eine größere ökologische Katastrophe erleben.",
        choices=[
            [1, 'Stimme überhaupt nicht zu'],
            [2, 'Stimme nicht zu'],
            [3, 'Neutral'],
            [4, 'Stimme zu'],
            [5, 'Stimme voll und ganz zu']
        ],
        widget=widgets.RadioSelect
    )


# PAGES
class NEPR(Page):
    form_model = 'player'
    form_fields = ['frage_1', 'frage_2', 'frage_3', 'frage_4', 'frage_5', 'frage_6', 'frage_7', 'frage_8', 'frage_9', 'frage_10', 'frage_11', 'frage_12', 'frage_13', 'frage_14', 'frage_15']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [NEPR]
