The product uses machine learning models to predict crop yields from environmental
data. Data from 'Crop_recommendation.csv' is preprocessed in Pandas, handling missing values
and splitting into training/testing sets via stratified sampling.

Four classifiers Logistic Regression, Decision Tree, Naive Bayes, and Random Forest are trained, with Random Forest
chosen for deployment due to superior accuracy. 

The model is serialized using joblib/pickle for
efficiency. A Flask web app fetches real-time weather (temperature, humidity, rainfall) via APIs
and IP geolocation. User-inputted soil parameters (Nitrogen, Phosphorus, Potassium, pH) are
processed to predict suitable crops, displayed on the frontend. Error handling ensures smooth
user interaction. 

The modular design supports scalability and future enhancements for evolving
agricultural needs.

