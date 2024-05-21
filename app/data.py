from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    """
    A class to interact with a MongoDB database, providing methods to seed, reset, count,
    and retrieve data in various formats.

    Attributes:
    ----------
    database : MongoClient
        The MongoDB client connected to the specified database.
    collection : Collection
        The specific collection within the database to interact with.
    """
    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection: str):
        """
        Initializes the Database instance with a specific collection.

        Parameters:
        ----------
        collection : str
            The name of the collection within the database.
        """
        self.collection = self.database[collection]

    def seed(self, amount=1000):
        """
        Seeds the collection with a specified number of random Monster documents.

        Parameters:
        ----------
        amount : int
            The number of Monster documents to insert into the collection.

        Returns:
        -------
        Dict[str, str]
            A dictionary indicating the success of the seeding operation.
        """
        return {'Seed successful': f"{self.collection.insert_many([Monster().to_dict() for _ in range(amount)]).acknowledged}"}

    def reset(self):
        """
        Resets the collection by deleting all documents.

        Returns:
        -------
        Dict[str, str]
            A dictionary indicating the success of the reset operation.
        """
        return {'Collection reset successful?': f'{self.collection.delete_many(filter={}).acknowledged}'}

    def count(self) -> int:
        """
        Counts the number of documents in the collection.

        Returns:
        -------
        int
            The number of documents in the collection.
        """
        return self.collection.count_documents(filter={})

    def dataframe(self) -> DataFrame:
        """
        Converts the collection's documents to a pandas DataFrame.

        Returns:
        -------
        DataFrame
            A DataFrame containing the collection's documents, excluding the '_id' field.
        """
        return DataFrame(self.collection.find({}, {"_id": False}))

    def html_table(self) -> str:
        """
        Converts the collection's documents to an HTML table.

        Returns:
        -------
        str
            An HTML string representing the collection's documents, or 'None' if the collection is empty.
        """
        if self.count() > 0:
            return self.dataframe().to_html(index=False)
        else:
            return 'None'


if __name__ == '__main__':
    db = Database("Collection")
    db.seed()
