import uvicorn


def main():
    uvicorn.run("url_shortener.main:app",
                host="localhost",  # settings.SERVER_HOST
                port=8000,         # settings.SERVER_PORT
                reload=True,       # settings.ENV in ["test", "dev"]
                log_level="debug") # if settings.ENV in ["test", "dev"] else None


if __name__ == "__main__":
    main()
