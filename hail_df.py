# hail_df.py

import pandas as pd

class HailDF:
    def __init__(self, db):
        self.db = db
        self.table = "hail"
    
    def count_hail_above_size(self, min_hail, start_date, end_date):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0
        
        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)

        mask = (
            (df["HAIL SIZE (INCHES)"] >= min_hail) &
            (df["DATE"] >= start_dt) &
            (df["DATE"] <= end_dt)
        )
        return df[mask].shape[0]

    def monthly_breakdown(self):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []
        
        df_clean = df.dropna(subset=["DATE"])
        df_clean["Month"] = df_clean["DATE"].dt.strftime("%m")
        grouped = df_clean.groupby("Month").size().reset_index(name="Count")
        return list(zip(grouped["Month"], grouped["Count"]))

    def yearly_breakdown(self):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []
        
        df_clean = df.dropna(subset=["DATE"])
        df_clean["Year"] = df_clean["DATE"].dt.strftime("%Y")
        grouped = df_clean.groupby("Year").size().reset_index(name="Count")
        return list(zip(grouped["Year"], grouped["Count"]))

    def top_property_damage(self, start_date, end_date, limit=5):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []

        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)

        mask = (df["DATE"] >= start_dt) & (df["DATE"] <= end_dt)
        df_filtered = df[mask].copy()
        df_filtered.sort_values(by="DAMAGE_PROPERTY_NUM", ascending=False, inplace=True)
        return df_filtered.head(limit).to_dict("records")

    def percent_of_hail_in_time_range(self, start_time, end_time):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0.0
        
        total = df.shape[0]
        if total == 0:
            return 0.0

        df_strtime = df["BEGIN_TIME"].fillna("").astype(str)
        mask = (df_strtime >= start_time) & (df_strtime <= end_time)
        in_range = mask.sum()
        return (in_range / total) * 100.0