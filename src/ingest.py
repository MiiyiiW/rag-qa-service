import pymupdf


def extract_pages(pdf_path: str) -> list[dict]:
    """把 PDF 每页的文字抽出来，返回 [{"page": 1, "text": "..."}, ...]"""
    doc = pymupdf.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:                                  # 空白页跳过
            pages.append({"page": i, "text": text})
    doc.close()
    return pages


if __name__ == "__main__":
    pages = extract_pages("data/example.pdf")
    print(f"共 {len(pages)} 页有文字")
    print(pages[0]["text"][:300])
