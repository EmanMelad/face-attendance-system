---
title: Face Attendance System
emoji: 📸
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.34.0
app_file: app.py
pinned: false
---

# Face Attendance System

A facial recognition system that logs attendance to Google Sheets.

## Features
- 👥 Face recognition via uploaded images
- 📊 Automatic logging to Google Sheets
- 🌐 Hugging Face Spaces deployment

## Setup
1. Add known faces to the `persons/` folder
2. Set Google Sheets credentials in Space Secrets:
   - `GCP_PRIVATE_KEY`
   - `GCP_CLIENT_EMAIL`
   - `GCP_PROJECT_ID`

## Requirements
See `requirements.txt` for dependencies.
