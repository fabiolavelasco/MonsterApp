from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from pandas import DataFrame
from datetime import datetime


class Machine:
    """
    A class to represent a machine learning model, specifically a Random Forest Classifier,
    trained on a given dataset.

    Attributes:
    ----------
    name : str
        The name of the machine learning model.
    model : RandomForestClassifier
        The Random Forest Classifier model.
    timestamp : str
        The timestamp of when the model was created and trained.
    """

    def __init__(self, df: DataFrame):
        """
        Initializes the Machine instance, trains the Random Forest Classifier on the provided DataFrame.

        Parameters:
        ----------
        df : DataFrame
            The DataFrame containing the training data. Assumes the target variable is in the 'Rarity' column.
        """
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = RandomForestClassifier(
            n_estimators=100,
            n_jobs=-1,
            max_depth=30,
            bootstrap=False,
            criterion='gini',
            max_features='log2',
            min_samples_leaf=1,
            min_samples_split=2
        )
        self.model.fit(features, target)
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __call__(self, feature_basis: DataFrame):
        """
        Makes a prediction using the trained model.

        Parameters:
        ----------
        feature_basis : DataFrame
            The DataFrame containing the features for prediction.

        Returns:
        -------
        tuple
            A tuple containing the predicted class and the probability of the predicted class.
        """
        prediction = self.model.predict(feature_basis)[0]
        probas = self.model.predict_proba(feature_basis)[0]
        return prediction, max(probas)

    def save(self, filepath: str):
        """
        Saves the Machine instance to a file.

        Parameters:
        ----------
        filepath : str
            The path where the Machine instance will be saved.
        """
        dump(self.model, 'model.joblib')

    @staticmethod
    def open(filepath: str):
        """
        Loads a Machine instance from a file.

        Parameters:
        ----------
        filepath : str
            The path to the file from which the Machine instance will be loaded.

        Returns:
        -------
        Machine
            The loaded Machine instance.
        """
        return load('model.joblib')

    def info(self) -> str:
        """
        Provides information about the Machine instance.

        Returns:
        -------
        str
            A string containing the model name and the timestamp of when the model was created.
        """
        return f'Currently running {self.name}, from {self.timestamp}'
