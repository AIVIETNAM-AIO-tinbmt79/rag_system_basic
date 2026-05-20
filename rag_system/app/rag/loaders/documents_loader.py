import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)


def load_single_file(file_path: str):
    """Load a single file based on its extension."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    docs = loader.load()

    for doc in docs:
        doc.metadata["file_type"] = ext.lstrip(".")
        doc.metadata["filename"] = os.path.basename(file_path)

    return docs


def loaders(data_path: str):
    """Load all supported files from a directory."""
    supported_exts = {".pdf", ".docx", ".txt"}
    data = []

    if not os.path.exists(data_path):
        return data

    for filename in os.listdir(data_path):
        ext = os.path.splitext(filename)[-1].lower()
        if ext not in supported_exts:
            continue
        file_path = os.path.join(data_path, filename)
        try:
            docs = load_single_file(file_path)
            data.extend(docs)
        except Exception as e:
            print(f"[WARN] Could not load {filename}: {e}")

    return data