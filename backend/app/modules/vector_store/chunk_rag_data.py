from app.utils.generate_chunk_id import generate_id


def chunk_rag_data(data):
    try:
        # Validate required top-level fields
        required_fields = ["cleaned_text", "perspective", "facts"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["facts"], list):
            raise ValueError("Facts must be a list")

        # Validate perspective structure
        perspective_data = data["perspective"]
        if hasattr(perspective_data, "dict"):
            perspective_data = perspective_data.dict()

        article_id = generate_id(data["cleaned_text"])
        chunks = []

        # Add counter-perspective chunk
        perspective_obj = data["perspective"]

        # Optional safety check

        if not (
            hasattr(perspective_obj, "perspective")
            and hasattr(perspective_obj, "reasoning")
        ):
            raise ValueError("Perspective object missing required fields")

        chunks.append({
            "id": f"{article_id}-perspective",
            "text": perspective_obj.perspective,
            "metadata": {
                "type": "counter-perspective",
                "reasoning": perspective_obj.reasoning,
                "article_id": article_id
            }
        })

        # Add each fact as a separate chunk
        for i, fact in enumerate(data["facts"]):
            fact_fields = [
                        "original_claim",
                        "verdict",
                        "explanation",
                        "source_link"
                        ]
            for field in fact_fields:
                if field not in fact:
                    raise ValueError("Missing required fact field:"
                                     f" {field} in fact index {i}")

            chunks.append({
                "id": f"{article_id}-fact-{i}",
                "text": fact["original_claim"],
                "metadata": {
                    "type": "fact",
                    "verdict": fact["verdict"],
                    "explanation": fact["explanation"],
                    "source_link": fact["source_link"],
                    "article_id": article_id
                }
            })

        return chunks

    except Exception as e:
        print(f"[Error] Failed to chunk the data: {e}")
        raise
