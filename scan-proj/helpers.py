import pandas as pd

def seperate_firewall(df):
    report_data = df.iloc[:-1]
    FireWall_report = df.iloc[-1]

    FireWall_report = FireWall_report.dropna(axis=0)


    return report_data, FireWall_report

def extract_and_merge_firewall_status(orginal_df,merged_df):
    firewall_status = orginal_df.iloc[-1]
    firewall_status_df = firewall_status.to_frame().T
    
    # if option is false drop the last row as it will become duplicate
    
    merged_df = merged_df.iloc[:-1]
    
    merged_df = pd.concat([merged_df, firewall_status_df], ignore_index=True)
    return merged_df
    