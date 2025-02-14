# Severe Weather Data Explorer (DataFrame Edition)

This project demonstrates a **pandas-based** severe weather explorer. Instead of using SQLite/SQL, we load CSV data directly into **in-memory pandas DataFrames** and query them via custom classes (`wind_df.py`, `tornado_df.py`, `hail_df.py`). We use **Streamlit** to provide a user-friendly web interface.

---

## Project Structure

Make sure **all** the following files exist **in the same folder**:

1. **main.py**  
   - The primary Streamlit app. Presents the UI and orchestrates queries.

2. **ui_helper.py**  
   - Contains helper functions for:
     - Clearing old query results in `st.session_state`
     - Storing new query results
     - Displaying a table and CSV download button

3. **storm_dataframes.py**  
   - Defines a `StormDataFrames` class that loads CSVs into pandas DataFrames (no SQL DB needed).

4. **wind_df.py**, **tornado_df.py**, **hail_df.py**  
   - Each has a class (`WindDF`, `TornadoDF`, `HailDF`) that performs dataset-specific queries in pandas.

5. **CSV Files**  
   - `wind_historical_data.csv`
   - `tor_historical_data.csv`
   - `hail_historical_data.csv`
   - (Optionally) `wind_data_dictionary.csv`, `tor_data_dictionary.csv`, `hail_data_dictionary.csv` for reference

---

## Installation

1. **Python 3.7+** is recommended.
2. Install required packages (at minimum `streamlit` and `pandas`):

   ```bash
   pip install streamlit pandas
Or use pip install -r requirements.txt if you have a requirements.txt file.

How to Run
In a terminal, navigate to the folder containing main.py.
Execute:
bash
Copy
Edit
streamlit run main.py
This will open a browser window (or tab) at localhost:8501 with the app interface.
Using the App
Pick a Dataset: Choose between Wind, Tornado, or Hail via the radio buttons at the top.
Select a Query: The dropdown will show available queries (e.g. “Count wind gusts >= X”, “Monthly breakdown”, etc.).
Set Parameters: Enter numeric or date/time inputs for the query.
Run Query:
Clicking Run Query clears any old results for that dataset, then executes the new query.
View/Download:
Below each query, you’ll see:
A checkbox to Show the results in a table.
A checkbox to Download those same results as a CSV file.
Switching Queries or re-running the same query with new parameters will overwrite the previous results.
Optional: Close DB
A button labeled “Close DB” is provided at the bottom. Clicking it clears the in-memory DataFrames to free resources (useful for testing, but not required for normal usage).

Troubleshooting
File Not Found: Verify wind_historical_data.csv, tor_historical_data.csv, etc. are all spelled correctly and in the same folder.
Missing Packages: Ensure pandas and streamlit are installed in the environment you’re running (pip list or conda list).
Indentation or Syntax: If you’ve edited the code, confirm the indentation for Python if/elif blocks is correct.