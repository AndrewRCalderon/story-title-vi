def clean_columns(data):
    data.columns = (
        data.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("\r", "_", regex=False)
        .str.replace("\n", "_", regex=False)
    )

    return data.columns
