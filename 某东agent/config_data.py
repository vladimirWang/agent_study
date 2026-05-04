md5_path = "./md5.txt"

# chroma
collection_name="jd_agent"
persist_directory="./chroma_db"

# spliter
chunk_size=1000
chunk_overlap=100
separators=["\n\n", "\n", "!", ".", "?", "。", "！", "？", " ", ""]
max_split_char_number=1000


similarity_threshold=2

embedding_model="text-embedding-v4"
chat_model_name = "qwen3-max"