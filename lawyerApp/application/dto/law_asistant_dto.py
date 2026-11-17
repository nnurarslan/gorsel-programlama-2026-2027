from dataclasses import dataclass

@dataclass
class RelatedArticleDTO:
    article_number: int
    title: str
    content: str
    similarity: float

    @classmethod
    def from_json(cls, data):
        return cls(
            article_number=data.get("article_number"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            similarity=data.get("similarity", 0.0)
        )

@dataclass
class LawAssistantResponseDTO:
    question: str
    answer: str
    related_articles: list[RelatedArticleDTO]

    @classmethod
    def from_json(cls, data):
        related = [RelatedArticleDTO.from_json(a) for a in data.get("relatedArticles", [])]
        return cls(
            question=data.get("question", ""),
            answer=data.get("answer", ""),
            related_articles=related
        )
