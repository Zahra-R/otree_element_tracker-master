from otree.api import *
import json
import random



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
    choice = models.StringField( choices = ['A', 'B'])
    def store_tracking_data(self, payload):
        HoverEvent.create(
            player=self,
            element_id=payload["element_id"],
            enter_time=payload["enter_time"],
            leave_time=payload["leave_time"],
            duration = payload["duration"],
            attributeType = payload["attributeType"],
            attributeValue = payload["attributeValue"],
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
     for player in subsession.get_players():
        if subsession.round_number == 1: 
            player.participant.orderStimuli = random.sample(range(0, C.NUM_ROUNDS), C.NUM_ROUNDS)




def custom_export(players):
    yield ["session", "participant_code", "round_number", "id_in_group", "element_id", "enter_time", "leave_time", "duration", "attributeType", "attributeValue"]
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
        print(C.stimulitable)
        roundStimulus = C.stimulitable[player.participant.orderStimuli[round_number-1]]
        print(player.participant.orderStimuli)
        return {
            'round_number': round_number,
            'APicture': " /static/global/images/" + roundStimulus['PictureA'], 
            'APrice': roundStimulus['PriceA'], 
            'ACO2':  roundStimulus['CO2A'], 
            'AProtein':  roundStimulus['ProteinA'], 
            'BPicture': " /static/global/images/" + roundStimulus['PictureB'], 
            'BPrice': roundStimulus['PriceB'], 
            'BCO2':  roundStimulus['CO2B'], 
            'BProtein':  roundStimulus['ProteinB'], 
            'AName':  roundStimulus['NameA'], 
            'BName':  roundStimulus['NameB'], 
        } 


page_sequence = [Tracker]
