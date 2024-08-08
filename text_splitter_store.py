import os
import sqlite3
import uuid

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter

from util.file import get_file_paths, load_text

data_folder_name = 'data'
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
vector_store = Chroma(
    collection_name="post",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="post_store"
)

db_conn = sqlite3.connect('post_vectors.db')
db_cursor = db_conn.cursor()

db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS post_vectors (
        id TEXT PRIMARY KEY,
        title TEXT,
        vector_ids TEXT
    )
""")


def handle_post(path):
    id = str(uuid.uuid4())
    title = os.path.splitext(os.path.basename(path))[0]
    post = load_text(path)
    post_chunk = text_splitter.split_text(post)
    post_id = str(vector_store.add_documents(post_chunk))
    db_cursor.execute("INSERT INTO post_vectors (id, title, vector_ids) VALUES (?, ?, ?)",
                      (id, title, post_id))
    db_conn.commit()


for file_path in get_file_paths(data_folder_name):
    handle_post(file_path)

db_conn.close()
