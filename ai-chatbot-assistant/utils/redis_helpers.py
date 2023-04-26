import redis
from redis.commands.search.query import Query
from redis.commands.search.field import VectorField, TextField
import numpy as np
import hashlib
from utils.ocr import get_embedding, load_tokenizer

# Redis connection details
endpoint = "127.0.0.1"
port = 6379
username = "default"


def connect_redis():
    """Connect to Redis and return the connection object."""
    redis_conn = redis.Redis(host=endpoint, port=port, username=username)
    return redis_conn


def upload_to_redis(id_sentence: str, sourcepage: str, sourcefile: str, text: str, embedded_text: list, redis_conn: redis.Redis):
    key_doc = {
    "id": id_sentence,
    "sourcepage": sourcepage,
    "sourcefile": sourcefile,
    "content": text,
    "embeddings": np.array(embedded_text).astype(dtype=np.float32).tobytes(),
    }
    # Store a blob of a random vector of type float32 under a field named 'vector' in Redis hash.
    hash_key = hashlib.md5(text.encode()).hexdigest()
    key = f"embedding:{hash_key}"
    redis_conn.hset(key, mapping=key_doc)


# Helper function to print results
def print_results(res):
    docs = [doc.id for doc in res.docs]
    dists = [float(doc.dist) if hasattr(doc, 'dist') else '-' for doc in res.docs]
    print(f"got {len(docs)} doc ids: ", docs)
    print("\ndistances: ", dists)


def reformat_redis(redis_conn: redis.Redis, preference = "quality"):
    # Cleans the Redis database
    redis_conn.flushall()

    # Define the constants for the schema
    if preference == "quality":
        openai_embedding_dim = 768
    elif preference == "speed" or preference == "more_speed":
        openai_embedding_dim = 384
    vector_field = "embeddings"

    schema = (TextField("id"),
                TextField("content"),
                TextField("sourcepage"),
                TextField("sourcefile"),
                VectorField(vector_field,  "FLAT", {"TYPE": "FLOAT32", "DIM": openai_embedding_dim, "DISTANCE_METRIC": "COSINE"}))
    redis_conn.ft().create_index(schema, "index")
    redis_conn.ft().config_set("default_dialect", 2)


def get_top_n(n, redis_conn, vector_query):
    #q = Query(f'*=>[KNN {5} @embedding $vec_param]=>{{$yield_distance_as: dist}}') 
    q = Query(f'*=>[KNN {n} @embeddings $vec_param]=>{{$yield_distance_as: dist}}').sort_by(f'dist')
    #FTSEARCH
    res = redis_conn.ft().search(q, query_params = {'vec_param': vector_query})
    return res


def create_query_context(redis_conn: redis.Redis, user_query: str, preference="quality"):
    model = load_tokenizer(preference)
    embedded_query = get_embedding(model, user_query)
    print(len(embedded_query))
    vector_query = np.array(embedded_query).astype(dtype=np.float32).tobytes()
    search_result = get_top_n(3, redis_conn, vector_query)
    context = ""
    for doc in search_result.docs:
        # Merge the variables of the doc into a single string
        context = context + f"""Ref: [{doc.sourcefile}, page {doc.sourcepage}] Content: {doc.content}\n"""
    
    prompt = f""""As an intelligent assistant, your role is to assist students in accessing and understanding course material. You will respond to questions using the data provided in the given source context. If the necessary information is not available in the provided sources, you may draw on your own knowledge and reference the 'model' source in your response. Each source is identified by a filename, page number, and corresponding content. Ensure that you cite the source file whenever you use it in your response. Since you must use the 'model' source, please be sure to cite it accordingly."\n\n
    Question: {user_query}\n\n
    Source data:\n{context}\n\n
    Answer:"""
    print(prompt)
    return prompt