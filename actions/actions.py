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
                        prog, program_name, fee, CourseDuration, SeatsNo, hod = row
                        response = (
                            f"The program you inquired about is '{program_name}' with an enrollment capacity of "
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



class ActionAdmissionConfidence(Action):
    def name(self) -> Text:
        return "action_admission_confidence"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        program_entity = next(tracker.get_latest_entity_values("program"), None)
        rank = int(next(tracker.get_latest_entity_values("rank"), None))

        if program_entity == 'bct':
            if rank <= 5000:
                response = f"You are probable to get admission in Computer Program."
            else:
                response = f"The probability of you getting admission with {rank} rank is less. However, you can still contact to the Computer Department."

        elif program_entity == 'bei':
            response = (f"Electronics, Communication and Information Engineering department doesnot have rank criteria to get admission. However, this department offers scholarships based on ranks."
                        f"\n 1. Rank '1 - 1000': Full Fee -> 80,000/- -> For first three students"
                        f"\n 2. Rank '1 - 1000': Full Fee -> 80,000/- -> After first three students upto ten students"
                        f"\n 3. Rank '1001 - 2000': Full Fee -> 5,50,000/- "
                        f"\n 4. Rank '2001 - 3000': Full Fee -> 5,90,000/- "
                        f"\n 5. Rank '3001 - 5000': Full Fee -> 5,90,000/- -> For first ten students"
                        f"\n 6. Rank '3001 - 5000': Full Fee -> 6,50,000/- -> After first ten students"
                        f"\n 6. Rank '5001 - 6721': Full Fee -> 6,90,000/- -> For first ten students"
                        f"\n 6. Rank '5001 - 6721': Full Fee -> 10,76,800/- -> After first ten students"
                        )
        else:
            response =  f"I am currently unable to parse information regarding {program_entity} program."

        dispatcher.utter_message(text=response)
        return []
    

class ActionAskSyllabus(Action):
    def name(self) -> Text:
        return "action_ask_syllabus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to the database
        conn = sqlite3.connect('Database\SyllabusDetail.db')  # Update with your database path

        if conn:
            program_entity = next(tracker.get_latest_entity_values('program'), None)

            
            if program_entity:
                # Perform a database query based on the program
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM syllabus WHERE prog = ?
                ''', (program_entity,))
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        prog, link = row
                        response = (f"You can find the syllabus of program {prog} via this link: {link}  ")
                        dispatcher.utter_message(text=response)
                else:
                    dispatcher.utter_message(text=f"Sorry! Currently I dont have any information regarding syllabus about the {program_entity} program you insisted.")
                
                conn.close()

        return []