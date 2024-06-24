from otree.api import *
import json
import random
import itertools

class C(BaseConstants):
    NAME_IN_URL = 'choice_task'
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
            stimulusID=payload["stimulusID"],
            foodName=payload["foodName"],
        )

class HoverEvent(models.ExtraModel):
    player = models.Link(Player)
    element_id = models.StringField()
    enter_time = models.FloatField()
    leave_time = models.FloatField()
    duration = models.IntegerField()
    attributeType = models.StringField()
    attributeValue = models.FloatField()
    stimulusID = models.StringField()
    foodName = models.StringField()

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
        "attributeValue",
        "stimulusID", 
        "foodName"
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
                e.attributeValue, 
                e.stimulusID,
                e.foodName
            ]

class choice(Page):
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
                'ALabel': "/static/global/images/" + roundStimulus['LabelB'] + ".webp",
                'APrice': roundStimulus['PriceB'],
                'ACO2': roundStimulus['CO2B'],
                'AProtein': roundStimulus['ProteinB'],
                'BPicture': "/static/global/images/" + roundStimulus['PictureA'],
                'BLabel': "/static/global/images/" + roundStimulus['LabelA'] + ".webp",
                'BPrice': roundStimulus['PriceA'],
                'BCO2': roundStimulus['CO2A'],
                'BProtein': roundStimulus['ProteinA'],
                'AName': roundStimulus['NameB'],
                'BName': roundStimulus['NameA'],
                'sustainable_name': roundStimulus['NameA'],
                'sustainable_price': roundStimulus['PriceA'],
                'sustainable_co2': roundStimulus['CO2A'],
                'sustainable_protein': roundStimulus['ProteinA'],
                'StimulusID': roundStimulus['StimulusID']
                
            }
        else:
            base_data = {
                'round_number': round_number,
                'APicture': "/static/global/images/" + roundStimulus['PictureA'],
                'ALabel': "/static/global/images/" + roundStimulus['LabelA'] + ".webp",
                'APrice': roundStimulus['PriceA'],
                'ACO2': roundStimulus['CO2A'],
                'AProtein': roundStimulus['ProteinA'],
                'BPicture': "/static/global/images/" + roundStimulus['PictureB'],
                'BLabel': "/static/global/images/" + roundStimulus['LabelB'] + ".webp",
                'BPrice': roundStimulus['PriceB'],
                'BCO2': roundStimulus['CO2B'],
                'BProtein': roundStimulus['ProteinB'],
                'AName': roundStimulus['NameA'],
                'BName': roundStimulus['NameB'],
                'sustainable_name': roundStimulus['NameB'],
                'sustainable_price': roundStimulus['PriceB'],
                'sustainable_co2': roundStimulus['CO2B'],
                'sustainable_protein': roundStimulus['ProteinB'],
                'StimulusID': roundStimulus['StimulusID']
            }

        if player.treatment == 'label':
            base_data.update({
            })
            if player.sustainableLeft == 0:
                base_data['template'] = 'tracking_demo/L_N.html'
            else:
                base_data['template'] = 'tracking_demo/L_S.html'

        elif player.treatment == 'norm':
            base_data.update({
            })
            if player.sustainableLeft == 0:
                base_data['template'] = 'tracking_demo/N_N.html'
            else:
                base_data['template'] = 'tracking_demo/N_S.html'

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
        player.choice_sustainable = player.participant.vars['chosen_option'] == 'sustainable'
        print(player.participant.vars)

class L_S(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'label' and player.participant.vars['chosen_option'] == 'sustainable'
    
    def vars_for_template(player: Player):
        roundStimulus = C.stimulitable[player.participant.orderStimuli[player.round_number-1]]
        choice = player.choice

        if player.sustainableLeft == 0:
            APicture = "/static/global/images/" + roundStimulus['PictureA']
            AName = roundStimulus['NameA']
            ALabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureB']
            BName = roundStimulus['NameB']
            BLabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            co2e_chosen = roundStimulus['CO2B'] 
            co2e_not_chosen = roundStimulus['CO2A'] 
            label = roundStimulus['LabelA'] if choice == 'A' else roundStimulus['LabelB']
            chosen, not_chosen = ('A', 'B') if choice == 'A' else ('B', 'A')

        else:
            APicture = "/static/global/images/" + roundStimulus['PictureB']
            AName = roundStimulus['NameB']
            ALabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureA']
            BName = roundStimulus['NameA']
            BLabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            co2e_chosen = roundStimulus['CO2B'] 
            co2e_not_chosen = roundStimulus['CO2A'] 
            label = roundStimulus['LabelB'] if choice == 'B' else roundStimulus['LabelA']
            chosen, not_chosen = ('B', 'A') if choice == 'B' else ('A', 'B')

        if label == 'labelA':
            chosen_color = 'green'
        elif label == 'labelB':
            chosen_color = 'green'
        elif label in ['labelC', 'labelD', 'labelE']:
            chosen_color = 'green'  
        else:
            chosen_color = 'black'

        not_chosen_color = 'black'

        message_chosen = f'<span style="color: {chosen_color}; font-size: xx-large; font-weight: bold;">{co2e_chosen} gCO2e</span>'
        message_not_chosen = f'<span style="color: {not_chosen_color}; font-size: xx-large; font-weight: bold; opacity: 0.5;">{co2e_not_chosen} gCO2e</span>'

        return {
            'APicture': APicture,
            'AName': AName,
            'ALabel': ALabel,
            'AOpacity': 1.0 if choice == 'A' else 0.5,
            'BPicture': BPicture,
            'BName': BName,
            'BLabel': BLabel,
            'BOpacity': 1.0 if choice == 'B' else 0.5,
            'ALabelOpacity': 1.0 if choice == 'A' else 0.5,
            'BLabelOpacity': 1.0 if choice == 'B' else 0.5,
            'AMessage': message_chosen if choice == 'A' else message_not_chosen,
            'BMessage': message_not_chosen if choice == 'A' else message_chosen,
            'chosen': chosen,
            'not_chosen': not_chosen,
            'co2e_value_chosen': co2e_chosen,
            'co2e_value_not_chosen': co2e_not_chosen        
        }

class L_N(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'label' and player.participant.vars['chosen_option'] == 'non-sustainable'
    
    def vars_for_template(player: Player):
        roundStimulus = C.stimulitable[player.participant.orderStimuli[player.round_number-1]]
        choice = player.choice

        if player.sustainableLeft == 0:
            APicture = "/static/global/images/" + roundStimulus['PictureA']
            AName = roundStimulus['NameA']
            ALabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureB']
            BName = roundStimulus['NameB']
            BLabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            co2e_chosen = roundStimulus['CO2A']
            co2e_not_chosen = roundStimulus['CO2B']
            #label = roundStimulus['LabelA'] if choice == 'A' else roundStimulus['LabelB']
            chosen, not_chosen = ('A', 'B') if choice == 'A' else ('B', 'A')

        else:
            APicture = "/static/global/images/" + roundStimulus['PictureB']
            AName = roundStimulus['NameB']
            ALabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureA']
            BName = roundStimulus['NameA']
            BLabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            co2e_chosen = roundStimulus['CO2A']
            co2e_not_chosen = roundStimulus['CO2B']
            #label = roundStimulus['LabelB'] if choice == 'B' else roundStimulus['LabelA']
            chosen, not_chosen = ('B', 'A') if choice == 'B' else ('A', 'B')

 ## here it the new correct code that should be adapted for all pages 

        if player.choice_sustainable == 'sustainable':
            chosen_color = roundStimulus['ColorB']
            not_chosen_color = roundStimulus['ColorA']
        else: 
            chosen_color = roundStimulus['ColorA']
            not_chosen_color = roundStimulus['ColorB']

        message_chosen = f'<span style="color: {chosen_color}; font-size: xx-large; font-weight: bold;">{co2e_chosen} gCO2e</span>'
        message_not_chosen = f'<span style="color: {not_chosen_color}; font-size: xx-large; font-weight: bold; opacity: 0.5;">{co2e_not_chosen} gCO2e</span>'

        return {
            'APicture': APicture,
            'AName': AName,
            'ALabel': ALabel,
            'AOpacity': 1.0 if choice == 'A' else 0.5,
            'BPicture': BPicture,
            'BName': BName,
            'BLabel': BLabel,
            'BOpacity': 1.0 if choice == 'B' else 0.5,
            'ALabelOpacity': 1.0 if choice == 'A' else 0.5,
            'BLabelOpacity': 1.0 if choice == 'B' else 0.5,
            'AMessage': message_chosen if choice == 'A' else message_not_chosen,
            'BMessage': message_not_chosen if choice == 'A' else message_chosen,
            'chosen': chosen,
            'not_chosen': not_chosen,
            'co2e_value_chosen': co2e_chosen,
            'co2e_value_not_chosen': co2e_not_chosen     
        }

import random

class N_S(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'norm' and player.participant.vars['chosen_option'] == 'sustainable'

    def vars_for_template(player: Player):
        roundStimulus = C.stimulitable[player.participant.orderStimuli[player.round_number - 1]]
        choice = player.choice
        sustainable_side = player.participant.vars.get('sustainable_side', 'left')

        if player.sustainableLeft == 0:
            APicture = "/static/global/images/" + roundStimulus['PictureA']
            AName = roundStimulus['NameA']
            ALabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureB']
            BName = roundStimulus['NameB']
            BLabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            co2e_chosen = roundStimulus['CO2B'] 
            co2e_not_chosen = roundStimulus['CO2A'] 
            label = roundStimulus['LabelA'] if choice == 'A' else roundStimulus['LabelB']
            chosen, not_chosen = ('A', 'B') if choice == 'A' else ('B', 'A')

        else:
            APicture = "/static/global/images/" + roundStimulus['PictureB']
            AName = roundStimulus['NameB']
            ALabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureA']
            BName = roundStimulus['NameA']
            BLabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            co2e_chosen = roundStimulus['CO2B'] 
            co2e_not_chosen = roundStimulus['CO2A'] 
            label = roundStimulus['LabelB'] if choice == 'B' else roundStimulus['LabelA']
            chosen, not_chosen = ('B', 'A') if choice == 'B' else ('A', 'B')

        if label == 'labelA':
            chosen_color = 'green'
        elif label == 'labelB':
            chosen_color = 'green'
        elif label in ['labelC', 'labelD', 'labelE']:
            chosen_color = 'green'
        else:
            chosen_color = 'black'

        not_chosen_color = 'black'

        message_chosen = f'<span style="color: {chosen_color}; font-size: xx-large; font-weight: bold;">{co2e_chosen} gCO2e</span>'
        message_not_chosen = f'<span style="color: {not_chosen_color}; font-size: xx-large; font-weight: bold; opacity: 0.5;">{co2e_not_chosen} gCO2e</span>'

        additional_texts = [
            "Immer mehr Menschen entscheiden sich für eine umweltbewusste Ernährung.",
            "Umweltfreundliche Lebensmittel gewinnen zunehmend an Popularität.",
            "Immer mehr Menschen erkennen die Bedeutung einer umweltbewussten Ernährung.",
            "Der Umweltgedanke bei der Lebensmittelauswahl wächst stetig.",
            "Viele passen ihre Ernährung an, um ihren ökologischen Fussabdruck zu verringern."
        ]

        if choice in ['A', 'B'] and sustainable_side in ['left', 'right']:
            AdditionalText = random.choice(additional_texts)
        else:
            AdditionalText = ''

        return {
            'APicture': APicture,
            'AName': AName,
            'ALabel': ALabel,
            'AOpacity': 1.0 if choice == 'A' else 0.5,
            'BPicture': BPicture,
            'BName': BName,
            'BLabel': BLabel,
            'BOpacity': 1.0 if choice == 'B' else 0.5,
            'ALabelOpacity': 1.0 if choice == 'A' else 0.5,
            'BLabelOpacity': 1.0 if choice == 'B' else 0.5,
            'AMessage': message_chosen if choice == 'A' else message_not_chosen,
            'BMessage': message_not_chosen if choice == 'A' else message_chosen,
            'chosen': chosen,
            'not_chosen': not_chosen,
            'co2e_value_chosen': co2e_chosen,
            'co2e_value_not_chosen': co2e_not_chosen,
            'AdditionalText': AdditionalText,
            'sustainable_side': sustainable_side
        }

class N_N(Page):
    def is_displayed(player: Player):
        return player.participant.vars['treatment'] == 'norm' and player.participant.vars['chosen_option'] == 'non-sustainable'

    def vars_for_template(player: Player):
        roundStimulus = C.stimulitable[player.participant.orderStimuli[player.round_number-1]]
        choice = player.choice

        if player.sustainableLeft == 0:
            APicture = "/static/global/images/" + roundStimulus['PictureA']
            AName = roundStimulus['NameA']
            ALabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureB']
            BName = roundStimulus['NameB']
            BLabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            co2e_chosen = roundStimulus['CO2A'] 
            co2e_not_chosen = roundStimulus['CO2B'] 
            label = roundStimulus['LabelA'] if choice == 'A' else roundStimulus['LabelB']
            chosen, not_chosen = ('A', 'B') if choice == 'A' else ('B', 'A')
        else:
            APicture = "/static/global/images/" + roundStimulus['PictureB']
            AName = roundStimulus['NameB']
            ALabel = "/static/global/images/" + roundStimulus['LabelB'] + ".webp"
            BPicture = "/static/global/images/" + roundStimulus['PictureA']
            BName = roundStimulus['NameA']
            BLabel = "/static/global/images/" + roundStimulus['LabelA'] + ".webp"
            co2e_chosen = roundStimulus['CO2A'] 
            co2e_not_chosen = roundStimulus['CO2B'] 
            label = roundStimulus['LabelB'] if choice == 'B' else roundStimulus['LabelA']
            chosen, not_chosen = ('B', 'A') if choice == 'B' else ('A', 'B')

        if label == 'labelC':
            chosen_color = 'orange'
        elif label == 'labelD':
            chosen_color = 'darkorange'
        elif label == 'labelE':
            chosen_color = 'red'
        elif label in ['labelA', 'labelB']:
            chosen_color = 'red'  
        else:
            chosen_color = 'black'

        not_chosen_color = 'black'

        message_chosen = f'<span style="color: {chosen_color}; font-size: xx-large; font-weight: bold;">{co2e_chosen} gCO2e</span>'
        message_not_chosen = f'<span style="color: {not_chosen_color}; font-size: xx-large; font-weight: bold; opacity: 0.5;">{co2e_not_chosen} gCO2e</span>'

        return {
            'APicture': APicture,
            'AName': AName,
            'ALabel': ALabel,
            'AOpacity': 1.0 if choice == 'A' else 0.5,
            'BPicture': BPicture,
            'BName': BName,
            'BLabel': BLabel,
            'BOpacity': 1.0 if choice == 'B' else 0.5,
            'ALabelOpacity': 1.0 if choice == 'A' else 0.5,
            'BLabelOpacity': 1.0 if choice == 'B' else 0.5,
            'AMessage': message_chosen if choice == 'A' else message_not_chosen,
            'BMessage': message_not_chosen if choice == 'A' else message_chosen,
            'chosen': chosen,
            'not_chosen': not_chosen,
            'co2e_value_chosen': co2e_chosen,
            'co2e_value_not_chosen': co2e_not_chosen        
        }

page_sequence = [choice, L_S, L_N, N_S, N_N]


