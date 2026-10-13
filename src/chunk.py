from ingest import extract_pages


def chunk_pages(pages: list[dict], size: int = 500, overlap: int = 100) -> list[dict]:
    """把每页文字切成带重叠的块，返回 [{"chunk_id": 0, "page": 1, "text": "..."}]"""
    chunks = []
    step = size - overlap                       # 每块起点前进的字符数（决定重叠多少）
    for p in pages:
        text = p["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + size].strip()
            if piece:                           # 跳过空块
                chunks.append({
                    "chunk_id": len(chunks),    # 自增编号：0, 1, 2 ...
                    "page": p["page"],          # 保留页码 → 以后标注出处
                    "text": piece,
                })
    return chunks


if __name__ == "__main__":
    pages = extract_pages("data/example.pdf")
    chunks = chunk_pages(pages)
    print(f"页数 {len(pages)} → 块数 {len(chunks)}")
    print(f"平均每块 {sum(len(c['text']) for c in chunks) // len(chunks)} 字符")

    a, b = chunks[0]["text"], chunks[1]["text"]
    print("--- 第 1 块结尾 80 字 ---")
    print(a[-80:])
    print("--- 第 2 块开头 80 字 ---")
    print(b[:80])

    ov = 0
    for L in range(min(len(a), len(b)), 0, -1):   # 从最长开始往短试
        if a.endswith(b[:L]):                     # a 是否以“b 的前 L 个字”结尾
            ov = L
            break
    print(f"实际重叠字符数：{ov}（期望接近 100）")
