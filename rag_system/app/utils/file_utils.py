SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def is_supported_file(
    filename
):

    return any(
        filename.endswith(ext)
        for ext in SUPPORTED_EXTENSIONS
    )