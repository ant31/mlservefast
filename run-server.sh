#!/bin/bash
PORT=${PORT:-8000}
gunicorn mlservefast.main:app -b :$PORT --timeout 120 -w 4 --reload -c conf/gunicorn.py
# uvicorn mlservefast.main:app  --reload
