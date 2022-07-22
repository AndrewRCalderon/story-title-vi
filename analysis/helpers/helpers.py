# A module of helper functions that I have used on multiple projects

def clean_columns(data):
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_', regex=False).str.replace('(', '', regex=False).str.replace(')', '', regex=False).str.replace('\r', '_', regex=False).str.replace('\n', '_', regex=False)
    
    return data.columns

if __name__ == "__main__":
    clean_columns()