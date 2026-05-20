import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        timeout_keep_alive=300,  # giữ kết nối 5 phút
        h11_max_incomplete_event_size=5 * 1024 * 1024  # 5MB upload
    )