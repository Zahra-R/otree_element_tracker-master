from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'comprehension_check'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    CORRECT_ANSWER = 'Ein Wert für die klimaschädlichen Gase aus der Lebensmittelproduktion'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    comprehension_answer = models.StringField()

class Check(Page):
    form_model = 'player'
    form_fields = ['comprehension_answer']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'question': 'Was versteht man unter CO2e?',
            'answers': [
                'Eine Kennzahl für den Wasserverbrauch in der Lebensmittelproduktion',
                'Ein Maß für die Luftverschmutzung',
                'Ein Indikator für die Temperaturerhöhung',
                C.CORRECT_ANSWER
            ],
            'correct_answer': C.CORRECT_ANSWER,
            'comprehension_check_failed': player.participant.vars.get('comprehension_check_failed', False)
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.comprehension_answer != C.CORRECT_ANSWER:
            player.participant.vars['comprehension_check_failed'] = True
        else:
            player.participant.vars['comprehension_check_failed'] = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.vars.get('comprehension_check_failed', False):
            return 'instructions'
        return None

page_sequence = [Check]




