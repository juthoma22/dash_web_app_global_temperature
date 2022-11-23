# Dash Web App Global Temperature
A simple web app, using [dash](https://dash.plotly.com/introduction), displaying the average temperature per country per year on a map

## Dependencies
Please use pipenv to install dependencies to work on the web app or run it.

`pipenv install --dev` installs all dependencies, includcing development dependencies.

`pipenv install` installs the dependencies required to run the web app.

A requirements.txt files is included, with the necessary dependencies to run the web app, e.g. for running it in a docker container.

## Environment variables
This web app downloads a dataset from kaggle, using the kaggle API. Therefore kaggle user data is required.

Please set the two environment variables `KAGGLE_USERNAME` and `KAGGLE_KEY` or include a kaggle.json. Read more [here](https://www.kaggle.com/docs/api "Kaggle API Documentation")