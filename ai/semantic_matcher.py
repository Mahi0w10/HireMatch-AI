from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the semantic similarity model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_description):

    if not resume_text.strip() or not job_description.strip():
        return 0

    # Convert both texts into numerical embeddings
    embeddings = model.encode([
        resume_text,
        job_description
    ])

    # Calculate similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Convert similarity into a percentage
    score = round(max(0, min(1, float(similarity))) * 100)

    return score