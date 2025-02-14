# wind_df.py

import pandas as pd

class WindDF:
    def __init__(self, db):
        """
        db is a StormDataFrames instance.
        """
        self.db = db
        self.table = "wind"

    def count_wind_gusts(self, min_knots, start_date, end_date):
        """
        Count events with MAGNITUDE (Knots) >= min_knots between [start_date, end_date].
        We'll assume df["DATE"] is a datetime.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0

        # Convert start/end to actual timestamps:
        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)
        
        # Filter
        mask = (
            (df["MAGNITUDE (Knots)"] >= min_knots) &
            (df["DATE"] >= start_dt) &
            (df["DATE"] <= end_dt)
        )
        return df[mask].shape[0]

    def get_top_property_damage(self, start_date, end_date, limit=5):
        """
        Return top-N rows sorted by DAMAGE_PROPERTY_NUM descending, in the given date range.
        We'll just return a list of dictionaries or list-of-lists if you like.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []
        
        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date)

        mask = (df["DATE"] >= start_dt) & (df["DATE"] <= end_dt)
        df_filtered = df[mask].copy()
        df_filtered.sort_values(by="DAMAGE_PROPERTY_NUM", ascending=False, inplace=True)
        df_top = df_filtered.head(limit)

        # Convert to a list of dict or list of tuples. 
        # For Streamlit, you might just return df_top directly, or df_top.to_dict("records").
        return df_top.to_dict("records")

    def get_percentile_rank(self, gust_knots):
        """
        Return the percentile of events whose MAGNITUDE (Knots) is less than 'gust_knots'.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0.0

        count_less = (df["MAGNITUDE (Knots)"] < gust_knots).sum()
        total = df.shape[0]
        if total == 0:
            return 0.0
        return (count_less / total) * 100.0

    def monthly_breakdown(self):
        """
        Return a list of (month, count) for all wind events. 
        Month as '01', '02', ..., '12'.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []

        # Drop missing dates
        df_clean = df.dropna(subset=["DATE"])
        df_clean["Month"] = df_clean["DATE"].dt.strftime("%m")
        grouped = df_clean.groupby("Month").size().reset_index(name="Count")
        
        # Convert to list of tuples
        return list(zip(grouped["Month"], grouped["Count"]))

    def yearly_breakdown(self):
        """
        Return a list of (year, count) for all wind events. 
        Year as '1950', '1951', etc.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return []

        df_clean = df.dropna(subset=["DATE"])
        df_clean["Year"] = df_clean["DATE"].dt.strftime("%Y")
        grouped = df_clean.groupby("Year").size().reset_index(name="Count")
        
        return list(zip(grouped["Year"], grouped["Count"]))

    def percent_of_events_in_time_range(self, start_time, end_time):
        """
        Percent of wind events for which BEGIN_TIME is between start_time and end_time (string comparison).
        E.g. '0000' <= BEGIN_TIME <= '2359'.
        """
        df = self.db.get_table_df(self.table)
        if df is None or df.empty:
            return 0.0

        total = df.shape[0]
        if total == 0:
            return 0.0

        # Some rows may have NaN or float in BEGIN_TIME; let's coerce them to string:
        df_strtime = df["BEGIN_TIME"].fillna("").astype(str)

        mask = (df_strtime >= start_time) & (df_strtime <= end_time)
        in_range = mask.sum()
        return (in_range / total) * 100.0