#!/bin/bash
uvicorn --host=0.0.0.0 app.main:app --reload --proxy-headers
