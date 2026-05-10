"""UI strings for Kitap Atlası (TR / EN)."""

from __future__ import annotations

from typing import Any

MESSAGES: dict[str, dict[str, Any]] = {
    "tr": {
        "app_title": "Kitap Atlası",
        "sidebar_tag": "Türkiye edebiyat haritası",
        "lang_label": "Dil",
        "btn_books": "Kitap listesi",
        "btn_stats": "İstatistikler",
        "btn_about": "Hakkımızda",
        "footer": "Kitap Atlası",
        "search_placeholder": "Kitap adı, yazar veya şehir ara…",
        "search_hint": "Eşleşen kitap başlıkları",
        "book_list_window": "Kitap listesi",
        "book_list_title": "Tüm kitaplar",
        "book_list_hint": "Haritada göstermek için bir satıra çift tıklayın.",
        "close": "Kapat",
        "about_window": "Kitap Atlası — Hakkımızda",
        "about_head": "Kitap Atlası",
        "about_sub": "Edebi mekânlar ve tarihsel bağlam",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "stats_window": "İstatistikler",
        "chart_top_cities": "En çok geçen 5 il (kitap sayısı)",
        "chart_books": "Kitap",
        "chart_count": "Adet",
        "chart_no_data": "Veri yok",
        "status_loading": "Veri yükleniyor…",
        "msg_data_error": "Veri hatası",
    },
    "en": {
        "app_title": "Kitap Atlas",
        "sidebar_tag": "Map of Turkish literature",
        "lang_label": "Lang",
        "btn_books": "Book list",
        "btn_stats": "Statistics",
        "btn_about": "About us",
        "footer": "Kitap Atlas",
        "search_placeholder": "Search title, author, or city…",
        "search_hint": "Matching book titles",
        "book_list_window": "Book list",
        "book_list_title": "All books",
        "book_list_hint": "Double-click a row to show it on the map.",
        "close": "Close",
        "about_window": "Kitap Atlas — About",
        "about_head": "Kitap Atlas",
        "about_sub": "Literary places and historical context",
        "about_body": (
            "<p style='line-height:1.5;'>"
            "<b>Lead Developer</b><br/>Muhammet Efe Savaş<br/><br/>"
            "<b>Research Team</b><br/>Hacı Boz, İbrahim Efe Nazlıgül"
            "</p>"
        ),
        "stats_window": "Statistics",
        "chart_top_cities": "Top 5 provinces by book count",
        "chart_books": "Books",
        "chart_count": "Count",
        "chart_no_data": "No data",
        "status_loading": "Loading data…",
        "msg_data_error": "Data error",
    },
}


def t(locale: str, key: str) -> Any:
    lang = "tr" if locale.lower().startswith("tr") else "en"
    return MESSAGES[lang].get(key, MESSAGES["en"].get(key, key))
