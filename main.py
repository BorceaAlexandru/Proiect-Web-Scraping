import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Exemplu de DataFrame cu datele jocurilor
data = pd.DataFrame({
    'price': [19.99, 29.99, 49.99, 9.99],
    'rating': [4.5, 4.7, 3.8, 4.0],
    'num_reviews': [1000, 2500, 500, 1500],
})

# Scalarea prețului, ratingului și numărului de recenzii
scaler = MinMaxScaler()
data[['price', 'rating', 'num_reviews']] = scaler.fit_transform(data[['price', 'rating', 'num_reviews']])

print(data)
