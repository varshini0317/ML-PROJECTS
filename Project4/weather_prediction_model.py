# -*- coding: utf-8 -*-
"""Weather prediction model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aVNMdceNRE7qHSQU2W1Fb09BoesFqGEd
"""

pip install scikit-learn==1.3.0

import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

# Load the datasset
df= pd.read_csv('/content/dataset.csv')

"""STATISTICAL ANALYSIS"""

df.head()

df.info()

df.describe()

df.columns

df.dtypes

df.index

df.isnull().sum()

df['weather'].unique()

df.nunique()

df.count()

df['weather'].value_counts()

# Create an empty dictionary to store the statistics for each column
stats_dict = {
    'mean': {},
    'median': {},
    'mode': {},
    'std_dev': {},
    'variance': {}
}

# Loop through the columns of the DataFrame
for col in df.columns:
    if df[col].dtype == float:
        data_col = df[col]
        stats_dict['mean'][col] = np.mean(data_col)
        stats_dict['median'][col] = statistics.median(data_col)
        stats_dict['mode'][col] = statistics.mode(data_col)
        stats_dict['std_dev'][col] = np.std(data_col)
        stats_dict['variance'][col] = np.var(data_col)

#mean value of each column against each 'Weather Condition'
df.groupby('weather').mean(numeric_only=True)

# Print the stats_dict dictionary
print(stats_dict)

#value_counts()
df['weather'].value_counts()

"""Analysis 1: Number of times when the weather is raining"""

#groupby()
df.groupby('weather').get_group('rain')

"""Analysis 2: Number of times when the weather is sunny"""

#groupby()
df.groupby('weather').get_group('sun')

"""Analysis 3: Number of times when the weather is drizzling"""

#groupby()
df.groupby('weather').get_group('drizzle')

"""Analysis 4: Number of times when the weather is snowy"""

#groupby()
df.groupby('weather').get_group('snow')

"""DATA PREPARATION"""

df['date'] = pd.to_datetime(df['date'])

df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['day_of_week'] = df['date'].dt.dayofweek

df

"""Data Visualization"""

df1=df['weather'].value_counts().index[0]

# Plot the autocorrelation of the 'weather' column
pd.plotting.autocorrelation_plot(df['weather'] == df1)

x=df['date']
y=df['precipitation']
plt.plot(x,y,'r')
plt.title('Precipitation based on dates')
plt.show()

weather=df['weather'].value_counts()
plt.bar(weather.index, weather.values, color='pink')
plt.xlabel('Weather Condition')
plt.ylabel('Frequency')
plt.title('Frequency of Weather Conditions')

df['wind'].value_counts()
plt.bar(df['date'],df['wind'],color='blue')
plt.xlabel('DATE')
plt.ylabel('WIND')
plt.title('DATE and WIND')

# Count the frequency of each weather condition
weather = df['weather'].value_counts()

# Plot the pie chart
plt.pie(weather, labels=weather.index, autopct='%d%%', startangle=45, colors=['blue', 'lightgreen','pink','yellow','red'])
plt.title('Weather Condition Distribution')

# Get the value counts of each unique value in the weather column
weather_counts = df['weather'].value_counts()

# Print the percentage of each unique value in the weather column
for weather, count in weather_counts.items():
    percent = (count / len(df)) * 100
    print(f"Percent of {weather.capitalize()}: {percent:.2f}%")

# Scatter plot of Precipitation vs. Maximum Temperature
plt.figure(figsize=(6, 4))
sns.scatterplot(x='temp_max', y='precipitation', data=df)
plt.title('Precipitation vs. Maximum Temperature')

# Calculate Pearson correlation coefficient and p-value
corr, p_val = stats.pearsonr(df['temp_max'], df['precipitation'])
plt.text(0.1, 0.9, 'Pearson correlation: {:.2f}\np-value: {:.2e}'.format(corr, p_val), transform=plt.gca().transAxes)

#Scatter plot of Wind vs. Maximum Temperature
plt.figure(figsize=(6, 4))
sns.scatterplot(x='temp_max', y='wind', data=df)
plt.title('Wind vs. Maximum Temperature')

# Calculate Pearson correlation coefficient and p-value
corr, p_val = stats.pearsonr(df['temp_max'], df['wind'])
plt.text(0.1, 0.9, 'Pearson correlation: {:.2f}\np-value: {:.2e}'.format(corr, p_val), transform=plt.gca().transAxes)

# Scatter plot of Maximum vs. Minimum Temperature
plt.figure(figsize=(6, 4))
sns.scatterplot(x='temp_min', y='temp_max', data=df)
plt.title('Maximum vs. Minimum Temperature')

# Calculate Pearson correlation coefficient and p-value
corr, p_val = stats.pearsonr(df['temp_min'], df['temp_max'])
plt.text(0.1, 0.9, 'Pearson correlation: {:.2f}\np-value: {:.2e}'.format(corr, p_val), transform=plt.gca().transAxes)

plt.show()

"""OUTLIER ANALYSIS"""

# Use a context manager to apply the default style to the plot
with plt.style.context('default'):

    # Create a figure with the specified size and an axis object
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot a boxplot with the given data, using the specified x and y variables, color palette, and axis object
    sns.boxplot(x="precipitation", y="weather", data=df, palette="winter", ax=ax)

    # Optional: set axis labels and title if desired
    ax.set(xlabel='Precipitation', ylabel='Weather', title='Boxplot of Weather vs. Precipitation')

with plt.style.context('default'):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="temp_max", y="weather", data=df, palette="spring", ax=ax)
    ax.set(xlabel='Temp_maxi', ylabel='Weather', title='Boxplot of Weather vs. Temp_maxi')

with plt.style.context('default'):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="temp_min", y="weather", data=df, palette="summer", ax=ax)
    ax.set(xlabel='Temp_min', ylabel='Weather', title='Boxplot of Weather vs. Temp_min')

with plt.style.context('default'):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="wind", y="weather", data=df, palette="summer", ax=ax)
    ax.set(xlabel='Wind', ylabel='Weather', title='Boxplot of Weather vs. Wind')

# Select only the numeric columns of the dataframe
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Calculate the first quartile (Q1), third quartile (Q3), and interquartile range (IQR)
Q1 = numeric_df.quantile(0.25)
Q3 = numeric_df.quantile(0.75)
IQR = Q3 - Q1

# Remove outliers using the IQR method
numeric_df = numeric_df[~((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).any(axis=1)]

# Drop any remaining NA/NaN values
numeric_df = numeric_df.dropna()

# Update the original dataframe with the cleaned numeric columns
df.update(numeric_df)

df

"""DATA MODELLING & SELECTION"""

# Separate features and target
X = df[['precipitation', 'temp_max', 'temp_min', 'wind']]
y = df['weather']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#from sklearn.preprocessing import LabelEncoder
# Create an instance of the LabelEncoder
#label_encoder = LabelEncoder()
#y_train = label_encoder.fit_transform(y_train)

"""MODEL 1- RANDOMFOREST"""

rf = RandomForestClassifier()

# Train the model
rf.fit(X_train, y_train)

# Make predictions
rf_predictions = rf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, rf_predictions)
print("Accuracy:", accuracy)

precision = precision_score(y_test, rf_predictions, average='macro')
recall = recall_score(y_test, rf_predictions, average='macro')
f1 = f1_score(y_test, rf_predictions, average='macro')

print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

"""MODEL 2- SUPPORT VECTOR"""

svc = SVC()

# Train the model
svc.fit(X_train, y_train)

# Make predictions
svc_predictions = svc.predict(X_test)

# Evaluate the model
accuracy1 = accuracy_score(y_test, svc_predictions)
print("Accuracy:", accuracy1)

precision1 = precision_score(y_test, svc_predictions, average='macro')
recall1 = recall_score(y_test, svc_predictions, average='macro')
svc_f1 = f1_score(y_test, svc_predictions, average='macro')

print("Precision:", precision1)
print("Recall:", recall1)
print("F1-score:", svc_f1)

"""MODEL 3- MULTI- LAYER PERCEPTRON"""

mlp = MLPClassifier()

mlp.fit(X_train, y_train)

# Make predictions
mlp_predictions = mlp.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, mlp_predictions)
print("Accuracy:", accuracy)

precision2 = precision_score(y_test, mlp_predictions, average='macro')
recall2 = recall_score(y_test, mlp_predictions, average='macro')
mlp_f1 = f1_score(y_test, mlp_predictions, average='macro')

print("Precision:", precision1)
print("Recall:", recall1)
print("F1-score:", mlp_f1)

"""MODEL 4- LOGISTIC REGRESSION"""

lr = LogisticRegression()

lr.fit(X_train, y_train)

# Make predictions
lr_predictions = lr.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, lr_predictions)
print("Accuracy:", accuracy)

precision = precision_score(y_test, lr_predictions, average='macro')
recall = recall_score(y_test, lr_predictions, average='macro')
f1 = f1_score(y_test, lr_predictions, average='macro')

accuracy_scores = [0.8191126279863481, 0.764505119453925, 0.8156996587030717, 0.8327645051194539]

# create a list of model names
model_names = ['Model 1', 'Model 2', 'Model 3', 'Model 4']

# create a bar chart
plt.bar(model_names, accuracy_scores)
plt.xlabel('Model Names')
plt.ylabel('Accuracy Scores')
plt.title('Accuracy Scores of Four Machine Learning Models')

# label the points on the bar chart
for i, score in enumerate(accuracy_scores):
    plt.text(i, score, f'{score:.2f}', ha='center', va='bottom')

plt.show()

"""Model 4 ie) Logistic Regression has highest accuracy

Save Model
"""

import pickle

# Save the model to a file using pickle
model_filename = 'weather_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(lr, file)

