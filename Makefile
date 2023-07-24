export

fastapi:
	pip install -r requirements.txt
	uvicorn kv-database-be.main:app --reload