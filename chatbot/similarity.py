from sentence_transformers import SentenceTransformer, util
from torch import Tensor

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')


class classifier:
    def get_top_similarity_answer(self, query, answers_list):
        query_embedding = model.encode(query)
        passage_embedding = model.encode(answers_list)
        similarity_scores = Tensor.tolist(util.dot_score(query_embedding, passage_embedding))[0]
        index = similarity_scores.index(max(similarity_scores))
        return answers_list[index]
