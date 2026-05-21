import chromadb

client = chromedb.client()

collections = client.get_or_create_collection(
    name="indexed"
)

