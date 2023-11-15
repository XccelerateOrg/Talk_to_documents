import os
import chromadb
from chromadb.utils import embedding_functions
from config import vector_dir, collection_name, group_every_x_lines

embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path=vector_dir)
collection = chroma_client.get_or_create_collection(name=collection_name)


def process_file(file_path):
    file_name = file_path.split(os.sep)[-1]
    full_text = ""
    with open(file_path, "r") as f:
        full_text = f.read()

    id_offset = collection.count()
    doc_collection = []
    metadata_collection = []
    ids_collection = []
    lines = full_text.split('\n')

    idx = 0

    for i in range(0, len(lines), group_every_x_lines):
        doc_collection.append('\n'.join(lines[i: i + group_every_x_lines]))
        metadata_collection.append({'doc_name': f"{file_name}_{idx + 1}"})
        ids_collection.append(str(id_offset + idx))
        idx += 1

    collection.add(documents=doc_collection,
                   metadatas=metadata_collection,
                   ids=ids_collection)

    if collection.count() > id_offset:
        return True
    else:
        return False


def process_query(query):
    query_result = collection.query(query_texts=query,
                                    n_results=1,
                                    include=["metadatas",
                                             "documents",
                                             "distances"]
                                    )
    return query_result
