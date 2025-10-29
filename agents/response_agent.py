# agents/response_agent.py
import pandas as pd
import numpy as np

class ResponsePlannerAgent:
    def __init__(self, master_df, fleet_df):
        self.df = master_df.copy()
        self.fleet = fleet_df.copy()

        # Normalise column names to lowercase to avoid KeyErrors
        self.fleet.columns = [c.lower() for c in self.fleet.columns]

    def simple_reassign(self, incident_row):
        """
        Heuristic: find an available vehicle with required capacity and minimal age.
        Handles case-insensitive column names.
        """
        required_capacity = incident_row.get('Order_Value_INR', 1)

        # Defensive column access
        fleet = self.fleet.copy()

        # Find available vehicles
        if 'status' in fleet.columns:
            candidates = fleet[fleet['status'].str.lower() == 'available'].copy()
        else:
            candidates = fleet.copy()

        if 'capacity_kg' in candidates.columns:
            candidates = candidates[candidates['capacity_kg'] >= required_capacity]

        if candidates.empty:
            return {"action": "escalate_human", "reason": "no_available_vehicle"}

        # Sort by age if present
        if 'age_years' in candidates.columns:
            candidates = candidates.sort_values(by='age_years', ascending=True)

        selected = candidates.iloc[0].to_dict()
        return {
            "action": "reassign_vehicle",
            "vehicle_id": selected.get('vehicle_id'),
            "vehicle_type": selected.get('vehicle_type'),
            "age_years": selected.get('age_years')
        }

    def suggest_reroute(self, incident_row):
        suggestions = []
        if incident_row.get('Traffic_Delay_Minutes', 0) > 15:
            suggestions.append("reroute_avoid_high_traffic")
        if str(incident_row.get('Weather_Impact', '')).lower() in ['rain', 'storm', 'yes', 'true']:
            suggestions.append("reroute_avoid_weather_impact")
        if not suggestions:
            suggestions.append("hold_for_monitoring")
        return {"action": "reroute_suggestions", "suggestions": suggestions}

    def plan_response(self, incidents_df):
        plans = []
        for _, r in incidents_df.iterrows():
            rep = self.simple_reassign(r)
            rer = self.suggest_reroute(r)
            plans.append({
                "Order_ID": r.get('Order_ID'),
                "Reassignment": rep,
                "Reroute": rer
            })
        return pd.DataFrame(plans)
