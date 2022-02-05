# A module of helper functions that I have used on multiple projects

def clean_columns(data):
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_', regex=False).str.replace('(', '', regex=False).str.replace(')', '', regex=False).str.replace('\r', '_', regex=False)

    return data.columns