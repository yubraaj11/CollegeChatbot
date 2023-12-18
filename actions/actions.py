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
        conn = sqlite3.connect('Database\ProgramDetail.db')  # Update with your database path

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
                    dispatcher.utter_message(text=f"I dont have any information about the {program_entity} program you insisted.")
                
                conn.close()

        return []
    
class ActionSpecifyProgram(Action):

    def name(self) -> Text:
        return "action_which_program"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Which program do you want to know about?")

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
        
        program_entity = next(tracker.get_latest_entity_values("program"), None)
        rank = next(tracker.get_latest_entity_values("rank"), None)

        if program_entity == 'bct':
            if rank <= 5000:
                response = f"You are probable to get admission in Computer Program."
            else:
                response = f"The probability of you getting admission with {rank} rank is less. However, you can still contact to the Computer Department."

        elif program_entity == 'bei':
            response = f"Electronics, Communication and Information Engineering department doesnot have rank criteria to get admission. However, this department offers scholarships based on ranks."
        else:
            response =  f"I am currently unable to parse information regarding {program_entity} program."

        dispatcher.utter_message(text=response)
        return []