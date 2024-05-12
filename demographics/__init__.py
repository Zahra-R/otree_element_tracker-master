from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    alter = models.IntegerField(
        label="Wie alt sind Sie?",
        min=18,
        max=100,
    )

    geschlecht = models.StringField(
        label="Mit welchem Geschlecht identifizieren Sie sich?",
        choices=['Weiblich', 'Männlich', 'Divers', 'Sonstige'],
        widget=widgets.RadioSelect
    )

    monatliches_einkommen = models.StringField(
        label="Wie hoch ist Ihr monatliches Einkommen?",
        choices=['0-500', '500-1000', '1000-2000', '2000-5000', '5000-8000', '> 8000', 'Ich möchte keine Angabe machen'],
        widget=widgets.RadioSelect
    )

    haushalts_einkauf = models.StringField(
        label="Sind Sie für den Einkauf in Ihrem Haushalt zuständig?",
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )



# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['alter', 'geschlecht', 'monatliches_einkommen', 'haushalts_einkauf']


class Goodbye(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


# class Results(Page):
#    pass


page_sequence = [Demographics, Goodbye]
