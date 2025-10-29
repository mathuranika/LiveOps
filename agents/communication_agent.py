# agents/communication_agent.py
import json
from datetime import datetime

class CommunicationAgent:
    def __init__(self):
        self.logs = []

    def log(self, event_type, payload):
        entry = {
            "ts": datetime.utcnow().isoformat()+"Z",
            "event": event_type,
            "payload": payload
        }
        self.logs.append(entry)
        print("[COMM]", entry)  # helpful for local runs

    def get_logs(self, last_n=200):
        return list(reversed(self.logs[-last_n:]))

    def compose_customer_message(self, order_row, action):
        # Small templated message to customer
        customer = order_row.get('customer_name', order_row.get('customer_id', 'customer'))
        order = order_row.get('order_id')
        if action.get('action') == 'reassign_vehicle':
            vehicle = action.get('vehicle_id')
            return f"Hi {customer}, your order {order} is being reassigned to vehicle {vehicle} to reduce delay. Expect update soon."
        elif action.get('action') == 'escalate_human':
            return f"Hi {customer}, we are investigating an issue with your order {order}. Our team will update you shortly."
        else:
            return f"Hi {customer}, update on order {order}: {action}"
