# FastAPI Assignment - Doctor/Patient API

Built a basic REST API for managing docs and patients. 

I split the code into `models.py`, `database.py`, and `main.py` to keep it organized and not have one giant file.

### How to run:
1. You'll need fastapi and uvicorn. Also `email-validator` for the Pydantic email check:
   `pip install fastapi uvicorn "pydantic[email]"`
2. Run it with:
   `uvicorn main:app --reload`
3. Go to `http://127.0.0.1:8000/docs` to test everything.

### Notes:
* Used **Pydantic** for validation (age must be > 0 and emails have to be valid).
* **UUID** handles the unique IDs so they don't overlap.
* Data is stored in lists in `database.py`, so it clears out if you kill the server.

