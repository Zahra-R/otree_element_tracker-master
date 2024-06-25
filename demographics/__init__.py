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

    studierende = models.StringField(
        label="Sind Sie momentan an einer Universität eingeschrieben?",
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )

    monatliches_einkommen = models.StringField(
        label="Wie hoch ist Ihr monatliches Nettoeinkommen? (in CHF/Euro)",
        choices=['0-500', '500-1000', '1000-2000', '2000-5000', '5000-8000', '> 8000', 'Ich möchte keine Angabe machen'],
        widget=widgets.RadioSelect
    )

    haushalts_einkauf = models.StringField(
        label="Sind Sie für den Lebensmitteleinkauf in Ihrem Haushalt zuständig?",
        choices=['Ja', 'Nein'],
        widget=widgets.RadioSelect
    )

    politische_orientierung = models.StringField(
        label="Wie würden Sie Ihre politische Orientierung beschreiben?",
        choices=['Links', 'Mitte-links', 'Mitte', 'Mitte-rechts', 'Rechts', 'Ich möchte keine Angabe machen'],
        widget=widgets.RadioSelect
    )

    ernaehrungsgewohnheiten = models.StringField(
        label="Welche der folgenden Ernährungsgewohnheiten treffen auf Sie zu?",
        choices=['AllesesserIn', 'Vegetarisch', 'Vegan', 'Pescetarisch', 'Sonstige'],
        widget=widgets.RadioSelect
    )

    email = models.StringField(
        blank=True, label="Ihre Emailadresse (Angabe freillig; benötigt für Gewinnspielteilnahme)"
    )

# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['alter', 'geschlecht', 'studierende', 'monatliches_einkommen', 'politische_orientierung', 'ernaehrungsgewohnheiten', 'haushalts_einkauf']


class Goodbye(Page):
    form_model = 'player'
    form_fields = ['email']


class ResultsWaitPage(WaitPage):
    pass


# class Results(Page):
#    pass


page_sequence = [Demographics, Goodbye]


