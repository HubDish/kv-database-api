export

fastapi:
	pip install -r requirements.txt
	uvicorn kv_database_be.main:app --reload