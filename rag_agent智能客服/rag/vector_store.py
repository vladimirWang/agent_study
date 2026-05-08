from langchain_chroma import Chroma
from utils.path_tool import get_abs_path
from utils.config_handler import chroma_conf
from utils.logger_handler import logger
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class VectorStoreService(object):
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"]
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
            从数据文件夹内读取数据文件，转为向量存入向量库，
            要计算文件md5去做去重
            :return: None
        """
        def check_md5_hex(md5_for_check: str):
            md5_file_path = get_abs_path(chroma_conf["md5_hex_store"])
            if not os.path.exists(md5_file_path):
                open(md5_file_path, "w", encoding="utf-8").close()
                return False

            with open(md5_file_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False


    def save_md5(md5_value: str):
        md5_file_path = get_abs_path(chroma_conf["md5_hex_store"])
        with open(md5_file_path, "a", encoding="utf-8") as f:
            f.write(md5_value + "\n")

    # def upload_by_str(self, data: str, filename: str):
    #     md5_hex = get_file_md5_hex(data)