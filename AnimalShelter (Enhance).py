# AnimalShelter.py

from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AnimalShelter:
    """
    CRUD operations for the AAC MongoDB collection
    """

    def __init__(self, username="aacuser", password="ChangeMe123",
                 host="127.0.0.1", port=27017,
                 db_name="aac", collection_name="animals",
                 auth_source="admin"):
        try:
            uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}"
            self.client = MongoClient(uri)
            self.client.admin.command("ping")

            self.database = self.client[db_name]
            self.collection = self.database[collection_name]

            logging.info("MongoDB connected successfully!")

        except Exception as e:
            logging.error(f"MongoDB connection failed: {e}")
            raise

    # -------------------------
    # VALIDATION METHOD (NEW)
    # -------------------------
    def validate_data(self, data):
        required_fields = ["animal_type", "breed"]

        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary.")

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        return True

    # -------------------------
    # CREATE (ENHANCED)
    # -------------------------
    def create(self, data: dict):
        try:
            self.validate_data(data)

            result = self.collection.insert_one(data)
            logging.info("Document inserted successfully")

            return result.inserted_id

        except Exception as e:
            logging.error(f"Insert failed: {e}")
            return None

    # -------------------------
    # READ (BASIC)
    # -------------------------
    def read(self, query: dict = None):
        try:
            if query is None:
                query = {}

            return list(self.collection.find(query))

        except Exception as e:
            logging.error(f"Read failed: {e}")
            return []

    # -------------------------
    # READ FILTERED (NEW)
    # -------------------------
    def read_filtered(self, animal_type=None, breed=None):
        try:
            query = {}

            if animal_type:
                query["animal_type"] = animal_type
            if breed:
                query["breed"] = breed

            logging.info(f"Running filtered query: {query}")
            return list(self.collection.find(query))

        except Exception as e:
            logging.error(f"Filtered read failed: {e}")
            return []

    # -------------------------
    # UPDATE (ENHANCED)
    # -------------------------
    def update(self, query: dict, update_values: dict):
        try:
            if not query or not update_values:
                raise ValueError("Query and update values required.")

            result = self.collection.update_many(query, {"$set": update_values})
            logging.info(f"{result.modified_count} document(s) updated")

            return result.modified_count

        except Exception as e:
            logging.error(f"Update failed: {e}")
            return 0

    # -------------------------
    # DELETE (ENHANCED)
    # -------------------------
    def delete(self, query: dict):
        try:
            if not query:
                raise ValueError("Query required.")

            result = self.collection.delete_many(query)
            logging.info(f"{result.deleted_count} document(s) deleted")

            return result.deleted_count

        except Exception as e:
            logging.error(f"Delete failed: {e}")
            return 0