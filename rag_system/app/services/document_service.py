import os
import shutil

from rag_system_basic.rag_system.app.rag.loaders.documents_loader import (
    loaders
)

from rag_system_basic.rag_system.app.core.config import settings


def save_uploaded_file(
    file
):

    os.makedirs(
        settings.UPLOAD_DIR,
        exist_ok=True
    )

    save_path = os.path.join(
        settings.UPLOAD_DIR,
        file.filename
    )

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return save_path


def load_documents():

    return loaders(
        settings.UPLOAD_DIR
    )