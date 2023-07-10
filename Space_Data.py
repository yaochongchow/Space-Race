import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from iso3166 import countries

# Set the Seaborn style
sns.set_style("darkgrid")

# Read the data from the CSV file
df = pd.read_csv('Datasets/Space_Missions_Cleaned.csv')

# Processing Data

# Extract the country of launch from the Location column
df["Country"] = df["Location"].apply(lambda location: location.split(", ")[-1])

# Extract the launch day of the week from the Datum column
df['Day'] = df['Datum'].apply(lambda datum: datum.split()[0])

# Extract the month of launch from the Datum column
df['Month'] = df['Datum'].apply(lambda datum: datum.split()[1])

# Extract the date of launch (in a month) from the Datum column
df['Date'] = df['Datum'].apply(lambda datum: int(datum.split()[2][:2]))

# Extract the hour of launch from the Datum column
df['Hour'] = df['Datum'].apply(lambda datum: int(datum.split()[-2][:2]) if datum.split()[-1] == 'UTC' else np.nan)

# Update country names to standardized ISO codes
country_mapping = {
    'Gran Canaria': 'USA',
    'Barents Sea': 'RUS',
    'Russia': 'RUS',
    'Pacific Missile Range Facility': 'USA',
    'Shahrud Missile Test Site': 'IRN',
    'Yellow Sea': 'CHN',
    'New Mexico': 'USA',
    'Iran': 'IRN',
    'North Korea': 'PRK',
    'Pacific Ocean': 'UMI',
    'South Korea': 'KOR'
}
df['Country'] = df['Country'].replace(country_mapping)

# Plotting

# Plot the count of launches by company
top_n = 25  # Number of top companies to show
top_companies = df['Company Name'].value_counts().index[:top_n]
df_top = df[df['Company Name'].isin(top_companies)]

plt.figure(figsize=(14, 8))
ax = sns.countplot(y="Company Name", data=df_top, order=top_companies)
ax.set_ylabel("Company Name", fontsize=14)
ax.set_xlabel("Count",fontsize=14)
plt.savefig('Images/companies_count_plot.png')
plt.close()

# Plot the count of launches by country
plt.figure(figsize=(24, 8))
ax = sns.countplot(y="Country", data=df, order=df["Country"].value_counts().index)
ax.set_xlim(0, 1500)
plt.savefig('Images/launch_size_by_country_plot.png')
plt.close()

# Plot the count of launches by location
top_n = 10  # Number of top locations to show
top_locations = df['Location'].value_counts().index[:top_n]
df_top = df[df['Location'].isin(top_locations)]

plt.figure(figsize=(20, 10))
ax = sns.countplot(y="Location", data=df_top, order=top_locations)
ax.set_xlabel("Count", fontsize=20)
ax.set_ylabel("Location", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
plt.xlim(0,250)
plt.subplots_adjust(left=0.4)
plt.savefig('Images/launch_locations.png')
plt.close()

# Plot the count of launches by day of the week
plt.figure(figsize=(8, 6))
ax = sns.countplot(x=df['Day'])
ax.set_title("Day of Week vs. Number of Launches", fontsize=14)
ax.set_xlabel("Day", fontsize=16)
ax.set_ylabel("Number of Launches", fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('Images/day_vs_launches.png')
plt.close()

# Plot the count of launches by day of the week with mission status
plt.figure(figsize=(10, 8))
ax = sns.countplot(x='Day', hue="Status Mission", data=df)
ax.set_title("Day of Week vs. Number of Launches", fontsize=14)
ax.set_xlabel("Day", fontsize=16)
ax.set_ylabel("Number of Launches", fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.ylim(0,1000)
plt.savefig('Images/mission_status.png')
plt.close()

# Plot the count of launches by month
plt.figure(figsize=(8, 6))
ax = sns.countplot(x='Month', data=df)
ax.set_title("Month vs. Number of Launches", fontsize=14)
ax.set_xlabel("Month", fontsize=16)
ax.set_ylabel("Number of Launches", fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('Images/month_vs_launches.png')
plt.close()

# Plot the count of launches by month with mission status
plt.figure(figsize=(14, 6))
ax = sns.countplot(x='Month', hue="Status Mission", data=df)
ax.set_title("Month vs. Number of Launches", fontsize=14)
ax.set_xlabel("Month", fontsize=16)
ax.set_ylabel("Number of Launches", fontsize=16)
ax.tick_params(labelsize=12)
plt.ylim(0, 400)
plt.tight_layout()
plt.savefig('Images/mission_distribution.png')
plt.close()

# Plot the count of launches by date of the month
plt.figure(figsize=(12, 6))
ax = sns.countplot(x=df['Date'])
ax.set_title("Date of Month vs. Number of Launches", fontsize=14)
ax.set_xlabel("Date of Month", fontsize=16)
ax.set_ylabel("Number of Launches", fontsize=16)
ax.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig('Images/date_vs_launches.png')
plt.close()

# Create the choropleth map of the number of launches by country
df['ISO'] = df['Country'].apply(lambda country: countries.get(country).alpha3)
iso_counts = df['ISO'].value_counts()

fig = px.choropleth(df, locations=iso_counts.index, color=iso_counts.values,
                    hover_name=iso_counts.index, title='Number of Launches',
                    color_continuous_scale="emrld")

fig.update_layout(
    width=800,  # Set the width of the figure
    height=600,  # Set the height of the figure
    font=dict(size=12)  # Set the font size
)

fig.write_image('Images/choropleth_map.png')

# Create the Sunburst chart
fig = px.sunburst(df, path=["Country", "Company Name", "Status Mission"], values="Count",
                  title="Sunburst Chart")

fig.update_layout(
    width=1200,  # Set the width of the figure
    height=1000,  # Set the height of the figure
    font=dict(size=12)  # Set the font size
)

fig.write_image('Images/sunburst_chart.png')


