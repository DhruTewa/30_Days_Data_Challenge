import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import kaleido

import nbformat
print(nbformat.__version__)

df = pd.read_csv('./Data/MyAir_SleepData/SLEEP_RECORD.csv')
df_filtered = df[['SESSION_DATE','USAGE_HOURS', 'SLEEP_SCORE', 'AHI_SCORE', 'LEAK_SCORE', 'MASK_SCORE',
       'USAGE_SCORE', 'MASK_SESSION_COUNT', 'AHI', 'LEAK_50_PERCENTILE','LEAK_70_PERCENTILE', 'LEAK_95_PERCENTILE']]
df_filtered.head()
df_filtered['SESSION_DATE'] = pd.to_datetime(df_filtered['SESSION_DATE'])
df_filtered.head()
df_filtered.shape
df_filtered['SESSION_DATE'] = df_filtered['SESSION_DATE'].dt.strftime('%Y-%m-%d')
df_filtered['SESSION_DATE'] = pd.to_datetime(df_filtered['SESSION_DATE'])
df_filtered.sort_values(by='SESSION_DATE', ascending=True, inplace=True)
df_filtered.reset_index(drop=True, inplace=True)
df_filtered.head()

plt.figure(figsize=(20, 6))
plt.title('Sleep Data Over Time')
sns.lineplot(data=df_filtered, x='SESSION_DATE', y='USAGE_HOURS')

df_filtered.head()

# Plotting Sleep Score Over Time
plt.figure(figsize=(20, 6))
plt.title('Sleep Score Over Time')
sns.lineplot(data=df_filtered, x='SESSION_DATE', y='SLEEP_SCORE', marker='o')
plt.xlabel('Date')
plt.ylabel('Sleep Score')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# Filter data for January 2025 to March 2025
start_date = '2025-01-01'
end_date = '2025-03-31'
df_filtered = df_filtered[(df_filtered['SESSION_DATE'] >= start_date) & (df_filtered['SESSION_DATE'] <= end_date)]

# Extracting day and month for grouping
df_filtered['DAY'] = df_filtered['SESSION_DATE'].dt.day
df_filtered['MONTH'] = df_filtered['SESSION_DATE'].dt.month

# Grouping by month and day to calculate the average sleep score
monthly_trend = df_filtered.groupby(['MONTH', 'DAY'])['SLEEP_SCORE'].mean().reset_index()

# Create a subplot for each month (January to March)
fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    subplot_titles=("January 2025", "February 2025", "March 2025"),
    vertical_spacing=0.1
)

# Define colors for each month
colors = ['#636EFA', '#EF553B', '#00CC96']

for month, row, color in zip(range(1, 4), range(1, 4), colors):  # Loop through months 1 (Jan) to 3 (Mar)
    # Filter data for the current month
    month_data = monthly_trend[monthly_trend['MONTH'] == month]
    
    if not month_data.empty and len(month_data) > 1:  # Ensure there is enough data
        # Add the sleep score trend line
        fig.add_trace(
            go.Scatter(
                x=month_data['DAY'],
                y=month_data['SLEEP_SCORE'],
                mode='lines+markers',
                name=f'Month {month}',
                line=dict(color=color, width=2),
                marker=dict(size=8, symbol='circle', color=color),
                hovertemplate='Day: %{x}<br>Sleep Score: %{y:.2f}<extra></extra>'
            ),
            row=row,
            col=1
        )
        
        # Calculate and add the slope line
        x = month_data['DAY']
        y = month_data['SLEEP_SCORE']
        slope, intercept = np.polyfit(x, y, 1)  # Linear regression to calculate slope
        fig.add_trace(
            go.Scatter(
                x=x,
                y=slope * x + intercept,
                mode='lines',
                name=f'Slope Line (Month {month})',
                line=dict(color='red', dash='dash', width=2),
                hoverinfo='skip'  # Skip hover info for slope line
            ),
            row=row,
            col=1
        )
    else:
        # Add a placeholder trace if no data is available
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode='lines',
                name=f'No Data for Month {month}',
                line=dict(color='gray', dash='dot')
            ),
            row=row,
            col=1
        )

# Update layout for better visualization
fig.update_layout(
    height=1000,  # Adjust height for better spacing
    title=dict(
        text="Sleep Score Trends (Jan 2025 - Mar 2025) with Slope Lines",
        font=dict(size=20),
        x=0.5
    ),
    xaxis_title="Day of the Month",
    yaxis_title="Sleep Score",
    plot_bgcolor='rgba(240, 240, 240, 0.9)',  # Light background for better contrast
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,  # Move the legend below the plot
        xanchor="center",
        x=0.5
    )
)

# Update x-axis ticks to show all days of the month
fig.update_xaxes(
    title_text="Day of the Month",
    tickmode='linear',
    dtick=1,
    showgrid=True,
    gridcolor='lightgray'
)

# Update y-axis for all subplots
fig.update_yaxes(
    title_text="Sleep Score",
    showgrid=True,
    gridcolor='lightgray'
)

# Show the plot
fig.show()

# Save the plot as a high-resolution PNG file
fig.write_image("sleep_score_trends.png", width=1920, height=1080, scale=2)