from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class BookEntry:
    id: int
    title: str
    author: str
    publication_year: int
    location_name: str
    coordinates: tuple[float, float]
    genre: str
    spatial_type: str
    sentiment: str
    quote: str
    description: str
    description_tr: str
    description_en: str
    historical_context: str
    historical_context_en: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BookEntry":
        coordinates = data.get("coordinates", [0.0, 0.0])
        lat, lng = float(coordinates[0]), float(coordinates[1])
        desc_tr = str(data.get("description_tr", data.get("description", "")))
        desc_legacy = str(data.get("description", desc_tr))
        return cls(
            id=int(data.get("id", 0)),
            title=str(data.get("title", "")),
            author=str(data.get("author", "")),
            publication_year=int(data.get("publication_year", 0)),
            location_name=str(data.get("location_name", "")),
            coordinates=(lat, lng),
            genre=str(data.get("genre", "")),
            spatial_type=str(data.get("spatial_type", "")),
            sentiment=str(data.get("sentiment", "")),
            quote=str(data.get("quote", "")),
            description=desc_legacy,
            description_tr=desc_tr,
            description_en=str(data.get("description_en", "")),
            historical_context=str(data.get("historical_context", data.get("donem", ""))),
            historical_context_en=str(data.get("historical_context_en", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "location_name": self.location_name,
            "coordinates": [self.coordinates[0], self.coordinates[1]],
            "genre": self.genre,
            "spatial_type": self.spatial_type,
            "sentiment": self.sentiment,
            "quote": self.quote,
            "description": self.description,
            "description_tr": self.description_tr,
            "description_en": self.description_en,
            "historical_context": self.historical_context,
            "historical_context_en": self.historical_context_en,
        }
