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
    AChoice = models.IntegerField(min=0, max=10000)
    BChoice = models.IntegerField(min=0, max=10000)

class Memory(Page):
    form_model = 'player'
    form_fields = ['AChoice', 'BChoice']

    @staticmethod
    def vars_for_template(player: Player):
        round_number = player.round_number
        with open("memory_task/memorystimuli.json", 'r') as f:
            stimuli = json.load(f)
        current_stimulus = stimuli[round_number - 1]
        return {
            'round_number': round_number,
            'APicture': "/static/global/images/" + current_stimulus['PictureA'],
            'BPicture': "/static/global/images/" + current_stimulus['PictureB'],
            'ADescription': current_stimulus['DescriptionA'],
            'BDescription': current_stimulus['DescriptionB'],
        }

page_sequence = [Memory]

with open("memory_task/memorystimuli.json", 'r') as f:
    stimuli = json.load(f)
