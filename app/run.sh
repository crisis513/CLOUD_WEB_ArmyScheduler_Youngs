#!/bin/bash
venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 3000
