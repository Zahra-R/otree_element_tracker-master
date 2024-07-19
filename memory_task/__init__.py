from otree.api import *
import json

class Constants(BaseConstants):
    name_in_url = 'memory_task'
    players_per_group = None
    num_rounds = 7

SPECIFIC_IMAGE_PAIRS = [
    {"PictureA": "baconegg.webp", "PictureB": "hummus.webp"},
    {"PictureA": "cereal.webp", "PictureB": "oats.webp"},
    {"PictureA": "icecream.webp", "PictureB": "sorbet.webp"},
    {"PictureA": "apples.webp", "PictureB": "dates.webp"},
    {"PictureA": "granolabar.webp", "PictureB": "cracker.webp"},
]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    AName = models.StringField()
    BName = models.StringField()
    AEstimate = models.IntegerField(min=0, max=50000)
    BEstimate = models.IntegerField(min=0, max=50000)
    ACorrect = models.IntegerField()
    BCorrect = models.IntegerField()

class Memory(Page):
    form_model = 'player'
    form_fields = ['AEstimate', 'BEstimate']

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        with open("memory_task/memorystimuli.json", 'r') as f:
            stimuli = json.load(f)
        current_stimulus = stimuli[round_number - 1]

        player.AName = current_stimulus['DescriptionA']
        player.BName = current_stimulus['DescriptionB']
        player.ACorrect = current_stimulus['CO2A']
        player.BCorrect = current_stimulus['CO2B']

        return {
            'round_number': round_number,
            'APicture': "/static/global/images/" + current_stimulus['PictureA'],
            'BPicture': "/static/global/images/" + current_stimulus['PictureB'],
            'ADescription': current_stimulus['DescriptionA'],
            'BDescription': current_stimulus['DescriptionB'],
        }

page_sequence = [Memory]

