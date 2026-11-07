from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_chunks(text: str, max_words: int = 100) -> list[str]:
    """
    Split long text into smaller chunks to avoid sentence-transformer token truncation.
    """
    words = text.split()
    if not words:
        return []

    chunks = [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]
    return chunks


def calculate_semantic_similarity(resume_text: str, job_description: str) -> int:
    """
    Calculates semantic similarity between resume chunks and the job description.
    Uses the average of the top 3 best matching chunks to prevent long resume dilution.
    """
    if (
        not isinstance(resume_text, str)
        or not isinstance(job_description, str)
        or not resume_text.strip()
        or not job_description.strip()
    ):
        return 0

    # Split resume into chunks
    resume_chunks = split_into_chunks(resume_text, max_words=100)
    if not resume_chunks:
        return 0

    # Encode JD and chunks
    jd_embedding = model.encode([job_description])
    resume_embeddings = model.encode(resume_chunks)

    # Compute cosine similarity
    similarities = cosine_similarity(
        jd_embedding,
        resume_embeddings
    )[0]

    if len(similarities) == 0:
        return 0

    # Take the top 3 best matching chunks (or all if fewer than 3)
    top_scores = sorted(similarities, reverse=True)[:3]
    average_similarity = sum(top_scores) / len(top_scores)

    # Scale to 0-100 percentage
    score = round(max(0, min(1, float(average_similarity))) * 100)
    return score