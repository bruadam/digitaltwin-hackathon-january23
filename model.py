# Import libraries and dependencies for training and testing a neural network model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score

# Read in the data
df = pd.read_excel('training_data.xlsx')

# Drop the _time, locationid columns
df.drop(['_time', 'locationid'], axis=1, inplace=True)

# Define the features set (X) and the target set (y)
X = df.drop('occupancy', axis=1).values
y = df['occupancy'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# Scale the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create the model
model = tf.keras.Sequential()

# Train the model
model.fit(x=X_train, y=y_train, epochs=600, validation_data=(X_test, y_test), verbose=1)

# Save the model
model.save('occupancy_model.h5')

# Evaluate the model
losses = pd.DataFrame(model.history.history)
losses.plot()
plt.show()

# Make predictions
predictions = model.predict_classes(X_test)

# Evaluate the model
print('Mean Absolute Error:', mean_absolute_error(y_test, predictions))
print('Mean Squared Error:', mean_squared_error(y_test, predictions))
print('Root Mean Squared Error:', np.sqrt(mean_squared_error(y_test, predictions)))
print('Explained Variance Score:', explained_variance_score(y_test, predictions))

# Plot the predictions
plt.figure(figsize=(12, 6))
plt.plot(y_test, label='True Values')
plt.plot(predictions, label='Predictions')
plt.legend()
plt.show()

# Plot the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, predictions)
sns.heatmap(cm, annot=True, fmt='g')
plt.show()

# Plot the classification report
from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))

# Plot the ROC curve
from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_test, predictions)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# Plot the AUC
from sklearn.metrics import roc_auc_score
print('AUC:', roc_auc_score(y_test, predictions))

# Plot the precision-recall curve
from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_test, predictions)
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()
