# common sequence generator
def get_next_sequence_value(collection_name: str, sequence_name: str, db) -> int:
    sequence_doc = db[collection_name].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return sequence_doc["sequence_value"]
