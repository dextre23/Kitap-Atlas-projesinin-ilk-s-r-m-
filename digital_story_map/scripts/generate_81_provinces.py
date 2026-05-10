#!/usr/bin/env python3
"""Generate data/cached_books.json with at least one book per Turkish province (81).

Plate order follows official TR codes 01–81. Provinces without a named canonical work
get a clearly fictional but plausible atlas entry (folkloric / historical narrative).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "cached_books.json"

# (province name, approx. center lat, lng) — plate codes 01–81 in order
PROVINCES: list[tuple[str, float, float]] = [
    ("Adana", 37.0000, 35.3213),
    ("Adıyaman", 37.7648, 38.2786),
    ("Afyonkarahisar", 38.7569, 30.5387),
    ("Ağrı", 39.7191, 43.0503),
    ("Amasya", 40.6499, 35.8353),
    ("Ankara", 39.9334, 32.8597),
    ("Antalya", 36.8841, 30.7056),
    ("Artvin", 41.1828, 41.8183),
    ("Aydın", 37.8560, 27.8416),
    ("Balıkesir", 39.6484, 27.8826),
    ("Bilecik", 40.1553, 29.9833),
    ("Bingöl", 38.8847, 40.4982),
    ("Bitlis", 38.3938, 42.1232),
    ("Bolu", 40.7392, 31.6089),
    ("Burdur", 37.7206, 30.2908),
    ("Bursa", 40.1826, 29.0665),
    ("Çanakkale", 40.1553, 26.4142),
    ("Çankırı", 40.6013, 33.6134),
    ("Çorum", 40.5506, 34.9556),
    ("Denizli", 37.7765, 29.0864),
    ("Diyarbakır", 37.9144, 40.2306),
    ("Edirne", 41.6818, 26.5623),
    ("Elazığ", 38.6748, 39.2226),
    ("Erzincan", 39.7500, 39.5000),
    ("Erzurum", 39.9043, 41.2678),
    ("Eskişehir", 39.7767, 30.5206),
    ("Gaziantep", 37.0662, 37.3833),
    ("Giresun", 40.9128, 38.3895),
    ("Gümüşhane", 40.4602, 39.4814),
    ("Hakkâri", 37.5744, 43.7408),
    ("Hatay", 36.4018, 36.3498),
    ("Isparta", 37.7648, 30.5566),
    ("Mersin", 36.8121, 34.6415),
    ("İstanbul", 41.0082, 28.9784),
    ("İzmir", 38.4237, 27.1428),
    ("Kars", 40.6013, 43.0975),
    ("Kastamonu", 41.3766, 33.7765),
    ("Kayseri", 38.7312, 35.4787),
    ("Kırklareli", 41.7370, 27.2242),
    ("Kırşehir", 39.1425, 34.1709),
    ("Kocaeli", 40.8533, 29.8815),
    ("Konya", 37.8667, 32.4833),
    ("Kütahya", 39.4167, 29.9833),
    ("Malatya", 38.3552, 38.3095),
    ("Manisa", 38.6191, 27.4289),
    ("Kahramanmaraş", 37.5858, 36.9371),
    ("Mardin", 37.3212, 40.7245),
    ("Muğla", 37.2153, 28.3636),
    ("Muş", 38.9462, 41.7538),
    ("Nevşehir", 38.6939, 34.6857),
    ("Niğde", 37.9667, 34.6833),
    ("Ordu", 40.9839, 37.8764),
    ("Rize", 41.0201, 40.5234),
    ("Sakarya", 40.7569, 30.3783),
    ("Samsun", 41.2867, 36.3300),
    ("Siirt", 37.9333, 41.9500),
    ("Sinop", 42.0231, 35.1531),
    ("Sivas", 39.7477, 37.0179),
    ("Tekirdağ", 40.9833, 27.5167),
    ("Tokat", 40.3167, 36.5500),
    ("Trabzon", 41.0015, 39.7178),
    ("Tunceli", 39.3074, 39.4388),
    ("Şanlıurfa", 37.1591, 38.7969),
    ("Uşak", 38.6823, 29.4082),
    ("Van", 38.4891, 43.4089),
    ("Yozgat", 39.8181, 34.8148),
    ("Zonguldak", 41.4564, 31.7987),
    ("Aksaray", 38.3687, 34.0370),
    ("Bayburt", 40.2552, 40.2249),
    ("Karaman", 37.1810, 33.2158),
    ("Kırıkkale", 39.8468, 33.5153),
    ("Batman", 37.8812, 41.1351),
    ("Şırnak", 37.4187, 42.4918),
    ("Bartın", 41.6344, 32.3375),
    ("Ardahan", 41.1105, 42.7022),
    ("Iğdır", 39.9237, 44.0450),
    ("Yalova", 40.6500, 29.2667),
    ("Karabük", 41.2061, 32.6204),
    ("Kilis", 36.7184, 37.1212),
    ("Osmaniye", 37.0742, 36.2478),
    ("Düzce", 40.8380, 31.1610),
]


def _fictional_entry(plate: int, name: str, lat: float, lng: float) -> dict:
    """Atlas-style fictional work; clearly not presented as a real bestseller."""
    title = f"{name} Sisleri (Atlas kaydı — kurgu)"
    author = "Anonim yerel rivayet derlemesi (kurgu)"
    tr_desc = (
        f"Bu kayıt, {name} ili coğrafyası ve sözlü kültürüne uyumlu, "
        f"atlas gösterimi için üretilmiş kurgusal bir anlatıdır; gerçek bir yayınevi eseri değildir."
    )
    en_desc = (
        f"A fictional atlas entry composed to represent {name} province geographically and culturally; "
        f"not a real published novel."
    )
    ctx_tr = f"{name} ve çevresinin tarihsel-topografik çerçevesine uygun, yerel hafıza motifi (kurgu)."
    ctx_en = f"Stylized local-memory motif aligned with the historical geography of {name} (fictional)."
    return {
        "id": plate,
        "title": title,
        "author": author,
        "publication_year": 1985 + (plate % 35),
        "city": name,
        "location_name": f"Merkez, {name}",
        "coordinates": [lat, lng],
        "genre": "Yerel anlatı (kurgu)",
        "spatial_type": "İl merkezi",
        "sentiment": "Duygusal",
        "quote": f"“Rüzgâr {name} üzerinden anlatı yeniden dökülür.” (kurgu alıntı)",
        "description": tr_desc,
        "description_tr": tr_desc,
        "description_en": en_desc,
        "historical_context": ctx_tr,
        "historical_context_en": ctx_en,
    }


def _huzur() -> dict:
    return {
        "id": 34,
        "title": "Huzur",
        "author": "Ahmet Hamdi Tanpınar",
        "publication_year": 1949,
        "city": "İstanbul",
        "location_name": "Beyoğlu, İstanbul",
        "coordinates": [41.0369, 28.9775],
        "genre": "Roman",
        "spatial_type": "Semt",
        "sentiment": "Melankolik",
        "quote": "Boğaz bir hüzün perdesi gibi uzanıyordu.",
        "description_tr": "Roman, İstanbul’un semtleri ve Boğaz çevresinde gezen Mümtaz’ın iç dünyasıyla geçiş dönemi kent atmosferini birleştirir.",
        "description": "Roman, İstanbul’un semtleri ve Boğaz çevresinde gezen Mümtaz’ın iç dünyasıyla geçiş dönemi kent atmosferini birleştirir.",
        "description_en": "The novel links Istanbul’s districts and the Bosphorus with an introspective portrait of transition-era urban life.",
        "historical_context": "1940’lar modernleşme ve erken çok partili dönem bağlamı.",
        "historical_context_en": "1940s modernization and early multi-party politics in Turkey.",
    }


def _anayurt() -> dict:
    return {
        "id": 45,
        "title": "Anayurt Oteli",
        "author": "Yusuf Atılgan",
        "publication_year": 1973,
        "city": "Manisa",
        "location_name": "Manisa",
        "coordinates": [38.6191, 27.4289],
        "genre": "Psikolojik kurgu",
        "spatial_type": "Otel",
        "sentiment": "Yabancılaşma",
        "quote": "Otel, zamanın dışında bir oda gibiydi.",
        "description_tr": "Otel mekânı, tekrar ve yabancılaşma üzerinden öznenin iç hapsini anlatır.",
        "description": "Otel mekânı, tekrar ve yabancılaşma üzerinden öznenin iç hapsini anlatır.",
        "description_en": "The hotel setting turns routine and alienation into a psychological prison.",
        "historical_context": "1970’ler kentleşme ve toplumsal dönüşüm atmosferi.",
        "historical_context_en": "1970s urban growth and social change in Turkey.",
    }


def main() -> None:
    if len(PROVINCES) != 81:
        print(f"Expected 81 provinces, got {len(PROVINCES)}", file=sys.stderr)
        sys.exit(1)

    books: list[dict] = []
    for plate, (name, lat, lng) in enumerate(PROVINCES, start=1):
        if plate == 34:
            books.append(_huzur())
        elif plate == 45:
            books.append(_anayurt())
        else:
            books.append(_fictional_entry(plate, name, lat, lng))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(books)} records to {OUT}")


if __name__ == "__main__":
    main()
