# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict    djhflkdjhfkjds
from rasa_sdk.events import SlotSet, AllSlotsReset
import json

with open("data.json", encoding="utf-8") as json_file:
    data = json.load(json_file)


class Utilities():

    @classmethod
    def createButtons(cls, intent: str, entity: str, slot_values: list, titles: list) -> List:
        buttons = []
        for i in zip(titles, slot_values):
            dict_ = {}
            dict_['title'] = i[0].strip()
            dict_['payload'] = "/" + intent.strip() + "{\"" + entity.strip() + "\":\" "+i[1].strip()+" \"}"
            buttons.append(dict_)
        return buttons

    @classmethod
    def convertDict(cls, dict_: dict):
        titles = []
        slot_values = []
        for i in dict_:
            titles.append(i)
            slot_values.append(dict_[i])
        return titles, slot_values



class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"
    
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        channel = tracker.get_latest_input_channel()
        channel = "english"
        intent = tracker.get_intent_of_latest_message()
        intent = "greet"
        entity = "greet_count"
        response_number = str(tracker.get_slot(entity)).strip()
        response_number = "0" if response_number == "None" else response_number
        print(response_number)
        choice = None
        choice = 0 if channel == "english" else 1 
        if response_number.startswith("END"):
            dispatcher.utter_message(text = data[response_number]['text'][choice])
            return [AllSlotsReset()]
        try:
            data[response_number]
        except KeyError:
            dispatcher.utter_message(text = "Technical Eroor")
            return [AllSlotsReset()]
        else:
            try:
                titles, slot_values = Utilities.convertDict(dict_ = data[response_number]['buttons'][choice])
            except KeyError:
                text = str(data[response_number]['text'][choice])
                if text.endswith("END"):
                    dispatcher.utter_message(text = text[:-4])
                    return [AllSlotsReset()]
                else:
                    try:
                        skip = data[response_number]['skip']
                    except KeyError:
                        dispatcher.utter_message(text = text)
                        return []
                    else:
                        dispatcher.utter_message(text = text)
                        return [SlotSet("greet_count", skip)]
            else:
                text = str(data[response_number]['text'][choice])
                buttons = Utilities.createButtons(intent = intent, entity = entity, slot_values = slot_values, titles = titles)
                if text.endswith("END"):
                    dispatcher.utter_message(text = text[:-4], buttons = buttons)
                    return [AllSlotsReset()]
                else:
                    dispatcher.utter_message(text = text, buttons = buttons)

        return []





        # // "buttons": [
        # //     {
        # //         "submit": "52"
        # //     },
        # //     {
        # //         "tanga": "52"
        # //     }
        # // ]
