# tornado_df.py

import pandas as pd

class TornadoDF:
    def __init__(self, db):
        self.db = db
        self.table = "tornado"
    
    def count_ef_tornadoes_exact(self, ef_scale, start_date, end_date):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0

        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)

        mask = (
            (df["TOR_F_SCALE"] == ef_scale) &
            (df["DATE"] >= start_dt) &
            (df["DATE"] <= end_dt)
        )
        return df[mask].shape[0]

    def count_ef_tornadoes_at_least(self, ef_scale, start_date, end_date):
        """
        Let's define a scale ordering for F0 < F1 < ... < F5, EF0 < EF1 < ... < EF5, etc.
        We'll do something simplistic: store them in a dict: 
           'F0'=0, 'F1'=1, ... 'F5'=5, 'EF0'=0, 'EF1'=1, ... 'EF5'=5, 'EFU'=-1, ...
        Then we filter where event scale >= the numeric of ef_scale.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0

        # We need a small helper to rank scales.
        scale_map = {
            "FU": -1, "EFU": -1,
            "F0": 0, "EF0": 0,
            "F1": 1, "EF1": 1,
            "F2": 2, "EF2": 2,
            "F3": 3, "EF3": 3,
            "F4": 4, "EF4": 4,
            "F5": 5, "EF5": 5,
        }
        # If the user typed something unknown, treat as 0
        min_rank = scale_map.get(ef_scale, 0)

        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)

        def get_rank(v):
            return scale_map.get(v, -999)  # If unknown, -999

        df = df.dropna(subset=["TOR_F_SCALE", "DATE"])  # remove rows w/ missing scale or date
        mask = (
            (df["DATE"] >= start_dt) &
            (df["DATE"] <= end_dt) &
            (df["TOR_F_SCALE"].apply(get_rank) >= min_rank)
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

    def top_tornado_length(self, limit=5):
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []
        
        df2 = df.dropna(subset=["TOR_LENGTH"]).copy()
        df2.sort_values(by="TOR_LENGTH", ascending=False, inplace=True)
        return df2.head(limit).to_dict("records")

    def percent_of_tornadoes_between_times(self, start_time, end_time):
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