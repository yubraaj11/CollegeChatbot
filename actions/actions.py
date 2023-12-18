# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import sqlite3
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionQueryDatabase(Action):
    def name(self) -> Text:
        return "action_query_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to the database
        conn = sqlite3.connect('university.db')  # Update with your database path

        if conn:
            program_entity = next(tracker.get_latest_entity_values('program'), None)

            
            if program_entity:
                # Perform a database query based on the program
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM programs WHERE prog = ?
                ''', (program_entity,))
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        index, prog, program_name, fee, CourseDuration, SeatsNo, hod = row
                        response = (
                            f"The program in question is '{program_name}' with an enrollment capacity of "
                            f"{SeatsNo} seats. Its duration spans over {CourseDuration}, and the overall fee "
                            f"for this course amounts to approximately {fee}."
                        )
                        dispatcher.utter_message(text=response)
                else:
                    dispatcher.utter_message(template="utter_no_info", program=program_entity)
                
                conn.close()

        return []
    
class ActionSpecifyProgram(Action):

    def name(self) -> Text:
        return "action_which_program"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Which program do you want to knwo about?")

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_explain_program"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        program_entity = next(tracker.get_latest_entity_values('program'), None)
        if program_entity:
            dispatcher.utter_message(text=f"Your requested program is '{program_entity}'.")
        else: 
            dispatcher.utter_message(text="Sorry I didnt get that")
        # dispatcher.utter_message(text="Hello World!")

        return []

class ActionAdmissionConfidence(Action):
    def name(self) -> Text:
        return "action_admission_confidence"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        program = tracker.latest_message.get('entties', [{'entity': 'program', 'value': None}])
        rank = tracker.latest_message.get('entties', [{'entity': 'rank', 'value': None}])

        if program == 'bct':
            dispatcher.utter_message(text="Computer Program")
        elif program == 'bei':
            dispatcher.utter_message(text="Electronics Program")
        else:
            dispatcher.utter_message(text="no solution")



        return []