from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'memory_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    LEBENSMITTEL = [
        {"name": "Apfel", "co2": 0.1},
        {"name": "Banane", "co2": 0.2},
        {"name": "Brokkoli", "co2": 0.3},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
     guessed_co2 = models.FloatField(
        label="Geben Sie bitte an, wie viel CO2 das Lebensmittel in Gramm pro Portion ausstößt:"
    )
correct_guess = models.BooleanField()   


# PAGES
class Memory(Page):
    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        return {'round_number': round_number, 'food_name': 'Bowl', 'food_image': '_static/global/images/bowl.webp'}
    form_model = 'player'
    form_fields = ['guessed_co2']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Memory]
