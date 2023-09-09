from uvicorn import run


def main():
    run(
        "unit_commitment.app:app",
        host="0.0.0.0",
        port=8888,
        reload=True,
    )


if __name__ == "__main__":
    main()
