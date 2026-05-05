from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableWithMessageHistory
from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv

load_dotenv()

def print_prompt(prompt):
    print("-"*10, prompt, "-"*10)
    return prompt
    
class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model)
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知参考资料为主,简洁和专业地回答问题。参考资料: {context}。"),
            ("system", "并且我提供用户的对话历史记录如下: {history}。"),
            MessagesPlaceholder("history"),
            ("user", "请回答用户提问: {input}")
        ])
        self.chat_model = ChatTongyi(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        # 获得最终执行链
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            print("length: ", len(docs))
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段: {doc.page_content}文档元数据: {doc.metadata}"

            return formatted_str
            
        def format_for_retriever(data: dict) -> str:
            print("----temp----: ", data)
            return data['input']

        
        def format_for_prompt(data: dict) -> str:
            print("----temp2----: ", data)
            new_data = {
                "input": data['input']['input'],
                "context": data['context'],
                "history": data['input']['history']
            }
            return new_data
        chain = (
            {
                "input": RunnablePassthrough(), 
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
             } | RunnableLambda(format_for_prompt) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain

if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "user001"
        }
    }
    res = RagService().chain.invoke({"input": "我的体重是多少"}, session_config)
    print(res)