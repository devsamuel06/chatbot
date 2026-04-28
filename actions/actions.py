from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionResumoAgendamento(Action):
    def name(self) -> Text:
        return "action_resumo_agendamento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        servico = tracker.get_slot("servico")
        nome = tracker.get_slot("nome_pet")
        horario = tracker.get_slot("horario")

        if not servico:
            dispatcher.utter_message(text="Qual serviço você deseja? (Banho ou Tosa)")
            return []
        
        if not nome:
            dispatcher.utter_message(text=f"Legal, {servico}! E qual o nome do pet?")
            return []
            
        if not horario:
            dispatcher.utter_message(text=f"E que horas você quer trazer o {nome}?")
            return []

        msg = (
            f" **Confirmação de Agendamento**\n"
            f" Pet: {nome}\n"
            f" Serviço: {servico.capitalize()}\n"
            f" Horário: {horario}\n\n"
            f"Podemos confirmar este horário?"
        )
        
        dispatcher.utter_message(text=msg)
        return []