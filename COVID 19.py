import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("owid-covid-data.csv")

# Preview first 5 rows
print("🔎 Preview of dataset:")
print(df.head())

# Show available columns
print("\n📌 Columns in dataset:")
print(df.columns)

# Check dataset info (rows, datatypes, missing values)
print("\n📊 Dataset info:")
print(df.info())

# Count missing values in each column
print("\n❓ Missing values per column:")
print(df.isnull().sum().head(15))  # Show first 15 columns
# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter countries
countries = ["Kenya", "Uganda", "India", "United States", "Tanzania"]
df_filtered = df[df['location'].isin(countries)]

# Drop rows with missing critical values
df_filtered = df_filtered.dropna(subset=['date', 'location'])

# Handle missing values
df_filtered['total_vaccinations'] = df_filtered['total_vaccinations'].fillna(0)
df_filtered['new_cases'] = df_filtered['new_cases'].interpolate()
df_filtered['new_deaths'] = df_filtered['new_deaths'].interpolate()

# Preview cleaned data
df_filtered.head(10)

# Set seaborn style
sns.set_style("whitegrid")

# Filter dataset for selected countries
countries = ["Kenya", "Uganda", "India", "United States", "Tanzania"]
df_plot = df_filtered[df_filtered['location'].isin(countries)]

# 1️⃣ Total cases over time
plt.figure(figsize=(12,6))
for country in countries:
    country_data = df_plot[df_plot['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.show()

# 2️⃣ Total deaths over time
plt.figure(figsize=(12,6))
for country in countries:
    country_data = df_plot[df_plot['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)

plt.title("Total COVID-19 Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.show()

# 3️⃣ Daily new cases comparison
plt.figure(figsize=(12,6))
for country in countries:
    country_data = df_plot[df_plot['location'] == country]
    plt.plot(country_data['date'], country_data['new_cases'], label=country)

plt.title("Daily New Cases Comparison")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.legend()
plt.show()

# 4️⃣ Calculate death rate
df_plot['death_rate'] = df_plot['total_deaths'] / df_plot['total_cases']

# Display death rate for each country on last available date
latest = df_plot.groupby('location').tail(1)[['location', 'death_rate']]
print("💀 Latest Death Rates by Country:")
print(latest)


# Seaborn style
sns.set_style("whitegrid")

# Filter dataset for selected countries
countries = ["Kenya", "Uganda", "India", "United States", "Tanzania"]
df_vax = df_filtered[df_filtered['location'].isin(countries)]

# 1️⃣ Cumulative vaccinations over time
plt.figure(figsize=(12,6))
for country in countries:
    country_data = df_vax[df_vax['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title("Cumulative COVID-19 Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.show()

# 2️⃣ Compare % vaccinated population (latest available date)
df_latest = df_vax.groupby('location').tail(1)  # last available data
df_latest['percent_vaccinated'] = (df_latest['total_vaccinations'] / df_latest['population']) * 100

# Bar chart for % vaccinated
plt.figure(figsize=(8,5))
sns.barplot(x='location', y='percent_vaccinated', data=df_latest, palette="viridis")
plt.title("Percentage of Population Vaccinated")
plt.ylabel("% Vaccinated")
plt.xlabel("Country")
plt.show()

# Optional: Pie chart for a single country
country = "United States"
us_data = df_latest[df_latest['location'] == country]
plt.figure(figsize=(6,6))
plt.pie([us_data['total_vaccinations'].values[0],
         us_data['population'].values[0] - us_data['total_vaccinations'].values[0]],
        labels=["Vaccinated", "Unvaccinated"],
        autopct='%1.1f%%', colors=['#4CAF50','#FF7043'])
plt.title(f"{country}: Vaccinated vs Unvaccinated Population")
plt.show()






# Prepare dataframe with latest data for each country
df_latest_global = df_filtered.sort_values('date').groupby('location').tail(1)

# Choropleth for total cases
fig_cases = px.choropleth(
    df_latest_global,
    locations="iso_code",        # ISO 3166-1 alpha-3 country codes
    color="total_cases",
    hover_name="location",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Global COVID-19 Total Cases"
)
fig_cases.show()

# Choropleth for vaccination rates (% of population vaccinated)
df_latest_global['percent_vaccinated'] = (df_latest_global['total_vaccinations'] / df_latest_global['population']) * 100

fig_vax = px.choropleth(
    df_latest_global,
    locations="iso_code",
    color="percent_vaccinated",
    hover_name="location",
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Global COVID-19 Vaccination Rates (%)"
)
fig_vax.show()
























































