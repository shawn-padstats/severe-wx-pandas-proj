# storm_dataframes.py

import os
import pandas as pd
from datetime import datetime

def parse_mmddyyyy(date_str):
    """
    Helper function to parse 'MM/DD/YYYY' into a proper datetime.
    If invalid, returns NaT.
    """
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%Y")
    except:
        return pd.NaT

class StormDataFrames:
    """
    A drop-in replacement for 'StormDatabase' which:
    - Stores data in memory as pandas DataFrames,
    - Has same method signatures: create_table, load_csv_into_table, execute_query, close,
    - But uses no actual SQL or DB file on disk.
    """
    def __init__(self, db_path="storms.db", recreate=True):
        """
        We keep the same signature, though 'db_path' and 'recreate' are largely irrelevant 
        to the in-memory approach. We initialize an internal dict to hold data.
        """
        self.data = {
            "wind": None,
            "tornado": None,
            "hail": None
        }
    
    def create_table(self, table_name):
        """
        In a real DB we would create a table schema. 
        Here, we could either do nothing or create an empty DataFrame placeholder.
        """
        if table_name not in self.data:
            self.data[table_name] = None  # or an empty DataFrame
        else:
            self.data[table_name] = None

    def load_csv_into_table(self, csv_path, table_name):
        """
        Reads CSV into a pandas DataFrame and stores it in self.data[table_name].
        We parse 'DATE' columns as datetime, if present, and leave the rest as strings/numbers.
        
        If your CSV date columns are consistently in position 0 or 1, 
        we can parse them with parse_mmddyyyy or read_csv parse_dates.
        """
        # Example: if the CSV definitely has the first column as a date in MM/DD/YYYY,
        # we can do something like:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV path does not exist: {csv_path}")
        
        # We'll do a first read to see if there's a header row and check column names
        # so we can do conditional date parsing. You can adapt as needed.
        df = pd.read_csv(
            csv_path,
            header=0,
            dtype=str,             # read everything as string initially
            na_values=["", "None", "NaN"],
            keep_default_na=True
        )
        
        # Convert known numeric columns to floats/ints if you want. 
        # For example, we might attempt numeric for anything that looks numeric:
        for col in df.columns:
            # Simple heuristic: try convert to numeric if possible
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
        
        # Convert date columns. Often, you know the exact col name is "DATE".
        # If it exists in df, parse with our custom function.
        if "DATE" in df.columns:
            df["DATE"] = pd.to_datetime(df["DATE"].apply(parse_mmddyyyy), errors="coerce")
        
        # Store the final DataFrame
        self.data[table_name] = df

    def execute_query(self, sql, params=None):
        """
        NOT USED in the DataFrame world, but we keep the method so existing code doesn't break.
        We can raise an error or return an empty list.
        """
        raise NotImplementedError("execute_query() is not used in the pandas-based version.")

    def get_table_df(self, table_name):
        """
        Retrieve the DataFrame for a given table.
        """
        return self.data[table_name]
    
    def close(self):
        """
        Nothing to do for DataFrame-based approach, but we keep it for compatibility.
        """
        pass