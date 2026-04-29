from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionResumoAgendamento(Action):
    def name(self) -> Text:
        return "action_resumo_agendamento"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        servico = tracker.get_slot("servico")
        nome = tracker.get_slot("nome_pet")
        horario = tracker.get_slot("horario")
        raca = tracker.get_slot("raca")

        # Progride através dos slots necessários
        if not servico:
            dispatcher.utter_message(response="utter_pedir_servico")
            return []
        
        if not nome:
            dispatcher.utter_message(response="utter_pedir_nome_pet")
            return []
            
        if not horario:
            dispatcher.utter_message(response="utter_pedir_horario")
            return []

        # Se chegou aqui, mostra confirmação
        msg = (
            f"**Confirmação de Agendamento**\n"
            f"🐾 Pet: {nome}\n"
            f"✂️ Serviço: {servico.capitalize()}\n"
            f"⏰ Horário: {horario}\n\n"
            f"Podemos confirmar este agendamento?"
        )
        
        dispatcher.utter_message(text=msg)
        return []


class ActionValidarServico(Action):
    """Valida se o serviço informado é válido"""
    def name(self) -> Text:
        return "action_validar_servico"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        servicos_validos = ["banho", "tosa", "banho e tosa", "tosa higiênica"]
        servico = tracker.get_slot("servico")
        
        if servico and servico.lower() in servicos_validos:
            return []
        
        dispatcher.utter_message(response="utter_pedir_servico")
        return [SlotSet("servico", None)]


class ActionLimparSlots(Action):
    """Limpa os slots para recomeçar o agendamento"""
    def name(self) -> Text:
        return "action_limpar_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("servico", None),
            SlotSet("nome_pet", None),
            SlotSet("horario", None),
            SlotSet("raca", None)
        ]