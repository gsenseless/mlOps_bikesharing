It is a model wrapped into the container, which predicts 'Rented Bike Count' based on bike sharing​ data.
To run it:
```
docker build -t bike_sharing -f app.dockerfile .
docker run bike_sharing
```