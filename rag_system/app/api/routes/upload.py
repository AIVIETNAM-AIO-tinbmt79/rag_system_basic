from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from rag_system_basic.rag_system.app.services.document_service import (
    save_uploaded_file,
)

from rag_system_basic.rag_system.app.rag.loaders.documents_loader import load_single_file

from rag_system_basic.rag_system.app.services.indexing_service import (
    indexing_pipeline
)

from rag_system_basic.rag_system.app.core.security import (
    get_current_user
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(
        get_current_user
    )
):
    # Step 1: Save file
    save_path = save_uploaded_file(file)

    # Step 2: Load only the uploaded file
    try:
        documents = load_single_file(save_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not documents:
        raise HTTPException(
            status_code=422,
            detail="File was saved but no content could be extracted. "
                   "It may be a scanned PDF or corrupted file."
        )

    # Step 3: Index
    result = indexing_pipeline(documents)

    return result