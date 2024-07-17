from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
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
    comprehension1 = models.StringField(choices=[ ["a_false", "Eine Kennzahl für den Wasserverbrauch in der Lebensmittelproduktion."], ["b_false", "Eine chemische Verbindung von Kohlendioxid, die modifiziert wurde, um weniger umweltschädlich zu sein."], ["c_false", "Ein Indikator für die Erwärmungsrate der Oberflächentemperatur der Erde."], ["correct", "Eine Kennzahl, die klimaschädliche Emissionen in Kohlenstoffdioxid-Einheiten angibt."]], label ="<b>Was versteht man unter CO2e?</b>",  widget = widgets.RadioSelect )

    comprehension2 = models.StringField(choices=[ ["a_false", "Eine Kennzahl für den Wasserverbrauch in der Lebensmittelproduktion."], ["b_false", "Eine chemische Verbindung von Kohlendioxid, die modifiziert wurde, um weniger umweltschädlich zu sein."], ["c_false", "Ein Indikator für die Erwärmungsrate der Oberflächentemperatur der Erde."], ["correct", "Eine Kennzahl, die klimaschädliche Emissionen in Kohlenstoffdioxid-Einheiten angibt."]], label ="<b>Was versteht man unter CO2e?</b>",  widget = widgets.RadioSelect )



# PAGES

class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def error_message(self, values):
        if values['consent'] != 1:
            return "Bitte stimmen Sie zu, um fortzufahren."


class Instructions(Page):
    form_model = 'player'


class Comprehension_check(Page):
    form_model = 'player'
    form_fields = ['comprehension1']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['comprehensionCheck'] = player.comprehension1
        

class Instructions2(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.comprehension1 != "correct"
    

class Comprehension_check2(Page):
    form_model = 'player'
    form_fields = ['comprehension2']


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['comprehensionCheck2'] = player.comprehension2
    @staticmethod
    def is_displayed(player: Player):
        return player.comprehension1 != "correct"


page_sequence = [Consent, Instructions, Comprehension_check, Instructions2, Comprehension_check2]

