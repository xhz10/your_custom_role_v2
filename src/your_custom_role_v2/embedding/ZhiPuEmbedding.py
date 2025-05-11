from typing import List
import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI
load_dotenv()

def embedding(input_document: List[str]):
    api_key = os.getenv("ZHIPU_API_EMBEDDING_KEY")
    client = ZhipuAI(api_key=api_key)
    response = client.embeddings.create(
        model="embedding-3",  # 填写需要调用的模型编码
        input=input_document,
    )
    all_embeddings = [embedding.embedding for embedding in response.data]

    return all_embeddings



if __name__ == '__main__':
    client = ZhipuAI(api_key="2fc0f0cae1544b4595c191177c203593.cYziszMsE6H3S0EW")
    response = client.embeddings.create(
        model="embedding-3",  # 填写需要调用的模型编码
        input=[
            "美食非常美味，服务员也很友好。",
            "这部电影既刺激又令人兴奋。",
            "阅读书籍是扩展知识的好方法。"
        ],
    )
    all_embeddings = [embedding.embedding for embedding in response.data]

    print(response)
