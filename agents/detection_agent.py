# agents/detection_agent.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class DataIngestionAgent:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_all(self):
        self.orders = pd.read_csv(f"{self.data_dir}/orders.csv")
        self.delivery = pd.read_csv(f"{self.data_dir}/delivery_performance.csv")
        self.routes = pd.read_csv(f"{self.data_dir}/routes_distance.csv")
        self.fleet = pd.read_csv(f"{self.data_dir}/vehicle_fleet.csv")
        self.warehouse = pd.read_csv(f"{self.data_dir}/warehouse_inventory.csv")
        self.feedback = pd.read_csv(f"{self.data_dir}/customer_feedback.csv")
        self.costs = pd.read_csv(f"{self.data_dir}/cost_breakdown.csv")
        return self.merge_master()

    def merge_master(self):
        df = self.orders.copy()
        # Merge all on Order_ID (primary key)
        df = df.merge(self.delivery, on="Order_ID", how="left")
        df = df.merge(self.routes, on="Order_ID", how="left")
        df = df.merge(self.costs, on="Order_ID", how="left")
        df = df.merge(self.feedback, on="Order_ID", how="left")

        # Derived metrics
        df["Delay_Days"] = df["Actual_Delivery_Days"] - df["Promised_Delivery_Days"]
        df["Delay_Flag"] = (df["Delay_Days"] > 0).astype(int)
        df["Total_Cost"] = (
            df["Fuel_Cost"]
            + df["Labor_Cost"]
            + df["Vehicle_Maintenance"]
            + df["Insurance"]
            + df["Packaging_Cost"]
            + df["Technology_Platform_Fee"]
            + df["Other_Overhead"]
        )

        # Clean nulls
        df = df.replace({np.nan: None})
        return df


class IncidentDetectionAgent:
    def __init__(self, master_df):
        self.df = master_df.copy()
        self.incidents = pd.DataFrame()

    def flag_basic_incidents(self, delay_days_threshold=2):
        # Delays
        delayed = self.df[self.df["Delay_Days"] > delay_days_threshold].copy()
        delayed["Incident_Type"] = "Delivery Delay"

        # Poor feedback
        poor = self.df[self.df["Rating"] <= 2].copy()
        poor["Incident_Type"] = "Low Rating / Complaint"

        # Cost spikes
        cost_mean = self.df["Total_Cost"].mean()
        cost_std = self.df["Total_Cost"].std()
        expensive = self.df[self.df["Total_Cost"] > cost_mean + 2 * cost_std].copy()
        expensive["Incident_Type"] = "Cost Spike"

        # Combine all
        all_incidents = pd.concat([delayed, poor, expensive]).drop_duplicates(subset=["Order_ID"])
        self.incidents = all_incidents
        return all_incidents

    def anomaly_detection(self):
        num_df = self.df[
            [
                "Delay_Days",
                "Delivery_Cost_INR",
                "Total_Cost",
                "Traffic_Delay_Minutes",
                "Distance_KM",
                "Fuel_Consumption_L",
            ]
        ].fillna(0)
        iso = IsolationForest(contamination=0.05, random_state=42)
        preds = iso.fit_predict(num_df)
        anomalies = self.df[preds == -1].copy()
        anomalies["Incident_Type"] = "Anomaly"
        self.incidents = pd.concat([self.incidents, anomalies]).drop_duplicates(subset=["Order_ID"])
        return anomalies
