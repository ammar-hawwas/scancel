import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os 
current_dir = os.path.dirname(os.path.abspath(__file__))
MAIN_DATA_PATH = current_dir +'/updated_final_dataset_for_Project2.xlsx'
def merge_datasets(csv_data):
    main_data = pd.read_excel(MAIN_DATA_PATH)
    
    no_duplicates = main_data.drop_duplicates(subset=['Port', 'Protocol'])

    merged_df = no_duplicates.drop(columns=['Service Name'])
    #output_data = pd.read_csv(report_path)

    # Merge datasets
    merged_df = pd.merge(csv_data, merged_df, on=['Port', 'Protocol'], how='inner')
    return merged_df

def generate_report(merged_df):
    
    fig = make_subplots(
        rows=2, cols=3,  # 2 rows, 3 columns
        subplot_titles=(
            'Port Risks', 'Distribution of Risk Levels', 'Transport Protocol',
            'Risk Levels by Transport Protocol', 'DDoS Risk', 'Scatter Plot: DDoS Risk vs Port and Protocol'
        ),
        specs=[
            [{"type": "pie"}, {"type": "bar"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "pie"}, {"type": "scatter"}]
        ]
    )

    # Plot risk distribution without "Other"
    category_counts = merged_df['Risk'].value_counts()
    fig.add_trace(
        go.Pie(labels=category_counts.index, values=category_counts.values, hole=.3, name="Port Risks"),
        row=1, col=1
    )

    # Plot risk levels
    risk_counts = merged_df['Risk'].value_counts()
    fig.add_trace(
        go.Bar(x=risk_counts.index, y=risk_counts.values, marker_color=['red', 'orange', 'yellow', 'green', 'blue', 'purple'], name="Risk Levels"),
        row=1, col=2
    )

    # Plot transport protocol
    protocol_counts = merged_df['Protocol'].value_counts()
    fig.add_trace(
        go.Bar(x=protocol_counts.index, y=protocol_counts.values, marker_color=['blue', 'purple', 'yellow', 'green'], name="Transport Protocol"),
        row=1, col=3
    )

    # Plot risk by protocol
    grouped_data = merged_df.groupby(['Protocol', 'Risk']).size().unstack(fill_value=0)
    for risk in grouped_data.columns:
        fig.add_trace(
            go.Bar(x=grouped_data.index, y=grouped_data[risk], name=risk),
            row=2, col=1
        )

    # Plot DDoS risk distribution without "Other"
    ddos_counts = merged_df['DDoS Risk'].value_counts()
    fig.add_trace(
        go.Pie(labels=ddos_counts.index, values=ddos_counts.values, hole=.3, name="DDoS Risk"),
        row=2, col=2
    )

    # Plot scatter plot for Port vs Protocol
    scatter_fig = px.scatter(merged_df, x='Port', y='Protocol', color='DDoS Risk')
    for trace in scatter_fig.data:
        fig.add_trace(trace, row=2, col=3)

    # Update layout
    fig.update_layout(
      
        showlegend=True,
        title_text="Combined Visualizations",
        autosize=True
    )

    # Convert the figure to HTML
    plot_html = fig.to_html(full_html=False)



    return plot_html
