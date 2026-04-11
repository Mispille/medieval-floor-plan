import argparse

from app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Random medieval house generator for role-play games"
    )
    parser.add_argument("--remote", action="store_true", help="Open to public network")

    args = parser.parse_args()
    host = "0.0.0.0" if args.remote else "127.0.0.1"

    app.run(host=host, debug=False)
