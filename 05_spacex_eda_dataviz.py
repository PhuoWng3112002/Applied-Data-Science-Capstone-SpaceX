import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# 1. FlightNumber vs PayloadMass
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=14)
plt.ylabel("Pay load Mass (kg)", fontsize=14)
plt.show()

# 2. FlightNumber vs LaunchSite
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=3)
plt.show()

# 3. PayloadMass vs LaunchSite
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=3)
plt.show()

# 4. Success Rate vs Orbit Type
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
sns.barplot(x='Orbit', y='Class', data=orbit_success)
plt.ylabel("Success Rate")
plt.show()

# 5. Yearly Success Trend
df['Year'] = df['Date'].apply(lambda x: x.split("-")[0])
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
sns.lineplot(x='Year', y='Class', data=yearly_success, marker='o')
plt.ylabel("Success Rate")
plt.show()

# Feature Engineering & One-Hot Encoding
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
features_one_hot = features_one_hot.astype('float64')
features_one_hot.to_csv('dataset_part_3.csv', index=False)