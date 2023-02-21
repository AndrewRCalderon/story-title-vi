import pandas as pd

data1 = {
    "MemberID": ["UDUKPX", "UDUKPX", "UDUKPX", "UDUKPX", "UDUKPX"],
    "StartDate": ["2020-03-11", "2020-03-14", "2020-03-15", "2020-03-17", "2020-03-18"],
    "EndDate": ["2020-03-11", "2020-03-14", "2020-03-15", "2020-03-17", "2020-03-18"],
}

data2 = {
    "MemberID": ["UDUKPX"],
    "1_StartDate": "2020-03-11",
    "1_EndDate": "2020-03-11",
    "2_StartDate": "2020-03-14",
    "2_EndDate": "2020-03-14",
    "3_StartDate": "2020-05-15",
    "3_EndDate": "2020-05-15",
    "4_StartDate": "2020-05-17",
    "4_EndDate": "2020-05-17",
    "5_StartDate": "2020-08-18",
    "5_EndDate": "2020-08-18",
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)


def compare_dates():
    for m in range(4):
        length = 6
        for i in range(1, length):
            if i <= 3:
                start = pd.to_datetime(df2[f"{i+1}_StartDate"])
                end = pd.to_datetime(df2[f"{i}_EndDate"])
                time_delta = (start - end).dt.days
                print(time_delta[0])

                if time_delta[0] < 30:
                    new_end = pd.to_datetime(df2[f"{i+2}_EndDate"])
                    new_start = pd.to_datetime(df2[f"{i+2}_StartDate"])
                    df2[f"{i+1}_StartDate"] = new_start
                    df2[f"{i+1}_EndDate"] = new_end

            if i == 4:
                start = pd.to_datetime(df2[f"{i+1}_StartDate"])
                end = pd.to_datetime(df2[f"{i}_EndDate"])
                time_delta = (start - end).dt.days

                if time_delta[0] < 30:
                    df2[f"{i+1}_StartDate"] = ""
                    df2[f"{i+1}_EndDate"] = ""


compare_dates()
print(df2)
