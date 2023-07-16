#!/bin/bash

source venv/bin/activate
uvicorn server:app --port 60000 --reload