from otree.api import *
import json
import random
import itertools

class C(BaseConstants):
    NAME_IN_URL = 'tracking_demo'
    PLAYERS_PER_GROUP = None
    stimulipath = "tracking_demo/stimuli.json"
    with open(stimulipath, 'r') as j:
        stimulitable = json.loads(j.read())
    NUM_ROUNDS = 15

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    choice = models.StringField(choices=['A', 'B'])
    sustainableLeft = models.BooleanField()
    treatment = models.StringField()
    choice_sustainable = models.BooleanField()

    def store_tracking_data(self, payload):
        HoverEvent.create(
            player=self,
            element_id=payload["element_id"],
            enter_time=payload["enter_time"],
            leave_time=payload["leave_time"],
            duration=payload["duration"],
            attributeType=payload["attributeType"],
            attributeValue=payload["attributeValue"],
        )

class HoverEvent(models.ExtraModel):
    player = models.Link(Player)
    element_id = models.StringField()
    enter_time = models.FloatField()
    leave_time = models.FloatField()
    duration = models.IntegerField()
    attributeType = models.StringField()
    attributeValue = models.StringField()

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        treatments = itertools.cycle(["label", "norm", "control"])
        for player in subsession.get_players():
            player.treatment = next(treatments)
            player.participant.vars['treatment'] = player.treatment
            player.participant.orderStimuli = random.sample(range(0, C.NUM_ROUNDS), C.NUM_ROUNDS)

def custom_export(players):
    yield [
        "session",
        "participant_code",
        "round_number",
        "id_in_group",
        "element_id",
        "enter_time",
        "leave_time",
        "duration",
        "attributeType",
        "attributeValue"
    ]
    for player in players:
        for e in HoverEvent.filter(player=player):
            yield [
                player.session.code,
                player.participant.code,
                player.round_number,
                player.id_in_group,
                e.element_id,
                e.enter_time,
                e.leave_time,
                e.duration,
                e.attributeType,
                e.attributeValue
            ]

class Tracker(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def live_method(player, data):
        player.store_tracking_data(data)

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        roundStimulus = C.stimulitable[player.participant.orderStimuli[round_number-1]]

        player.sustainableLeft = random.choice([True, False])
        player.treatment = player.participant.vars['treatment']

        if player.sustainableLeft == 1:
            base_data = {
                'round_number': round_number,
                'APicture': "/static/global/images/" + roundStimulus['PictureB'],
                'APrice': roundStimulus['PriceB'],
                'ACO2': roundStimulus['CO2B'],
                'AProtein': roundStimulus['ProteinB'],
                'BPicture': "/static/global/images/" + roundStimulus['PictureA'],
                'BPrice': roundStimulus['PriceA'],
                'BCO2': roundStimulus['CO2A'],
                'BProtein': roundStimulus['ProteinA'],
                'AName': roundStimulus['NameB'],
                'BName': roundStimulus['NameA'],
                'sustainable_name': roundStimulus['NameA'],
                'sustainable_price': roundStimulus['PriceA'],
                'sustainable_co2': roundStimulus['CO2A'],
                'sustainable_protein': roundStimulus['ProteinA'],
            }
        else:
            base_data = {
                'round_number': round_number,
                'APicture': "/static/global/images/" + roundStimulus['PictureA'],
                'APrice': roundStimulus['PriceA'],
                'ACO2': roundStimulus['CO2A'],
                'AProtein': roundStimulus['ProteinA'],
                'BPicture': "/static/global/images/" + roundStimulus['PictureB'],
                'BPrice': roundStimulus['PriceB'],
                'BCO2': roundStimulus['CO2B'],
                'BProtein': roundStimulus['ProteinB'],
                'AName': roundStimulus['NameA'],
                'BName': roundStimulus['NameB'],
                'sustainable_name': roundStimulus['NameB'],
                'sustainable_price': roundStimulus['PriceB'],
                'sustainable_co2': roundStimulus['CO2B'],
                'sustainable_protein': roundStimulus['ProteinB'],
            }

        if player.treatment == 'label':
            base_data.update({
            })
            if player.sustainableLeft == 0:
                base_data['template'] = 'tracking_demo/Label_nonsustainable.html'
            else:
                base_data['template'] = 'tracking_demo/Label_sustainable.html'

        elif player.treatment == 'norm':
            base_data.update({
            })
            if player.sustainableLeft == 0:
                base_data['template'] = 'tracking_demo/Norm_nonsustainable.html'
            else:
                base_data['template'] = 'tracking_demo/Norm_sustainable.html'

        elif player.treatment == 'control':
            base_data.update({
            })
            base_data['template'] = 'global/blank_page.html'

        return base_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        choice = player.choice
        if player.sustainableLeft:
            if choice == 'A':
                player.participant.vars['chosen_option'] = 'sustainable'
            else:
                player.participant.vars['chosen_option'] = 'non-sustainable'
        else:
            if choice == 'B':
                player.participant.vars['chosen_option'] = 'sustainable'
            else:
                player.participant.vars['chosen_option'] = 'non-sustainable'
        print(player.participant.vars)

class Label_sustainable(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'label' and player.participant.vars['chosen_option'] == 'sustainable'

    def vars_for_template(player: Player):
        return {}

class Label_nonsustainable(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'label' and player.participant.vars['chosen_option'] == 'non-sustainable'

    def vars_for_template(player: Player):
        return {}

class Norm_sustainable(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'norm' and player.participant.vars['chosen_option'] == 'sustainable'

    def vars_for_template(self):
        return {}

class Norm_nonsustainable(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'norm' and player.participant.vars['chosen_option'] == 'non-sustainable'

    def vars_for_template(player: Player):
        return {}

page_sequence = [Tracker, Label_sustainable, Label_nonsustainable, Norm_sustainable, Norm_nonsustainable]