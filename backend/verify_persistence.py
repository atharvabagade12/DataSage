from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from models import User
import os
import shutil

# Setup Test Client
client = TestClient(app)

# Mock Auth
async def mock_get_current_user():
    return {"id": 1, "username": "testuser", "email": "test@example.com"}

app.dependency_overrides["auth.get_current_user"] = mock_get_current_user
# We also need to override the one imported in main.py if it was imported directly
# But main.py uses 'auth.get_current_user' in Depends, so the string override might not work if auth is imported.
# Let's check main.py imports. It does `import auth`. So `app.dependency_overrides[auth.get_current_user] = ...` is better.

import auth
app.dependency_overrides[auth.get_current_user] = mock_get_current_user

def verify_persistence():
    print("Starting Persistence Verification...")
    
    # 1. Upload Dataset
    print("\n1. Testing Upload...")
    csv_content = "col1,col2\n1,10\n2,20\n3,30"
    files = {"file": ("test_data.csv", csv_content, "text/csv")}
    
    response = client.post("/api/upload-dataset", files=files)
    if response.status_code != 200:
        print(f"Upload failed: {response.text}")
        return
    
    data = response.json()
    dataset_id = data['dataset_id']
    print(f"Upload successful. Dataset ID: {dataset_id}")
    
    # 2. List Datasets
    print("\n2. Testing List Datasets...")
    response = client.get("/api/datasets")
    if response.status_code != 200:
        print(f"List datasets failed: {response.status_code} - {response.text}")
        return
        
    datasets = response.json()
    print(f"Got {len(datasets)} items in response")
    print(f"Response type: {type(datasets)}")
    print(f"Response content: {datasets}")
    
    if isinstance(datasets, dict):
        # Handle case where it returns a dict (maybe error or wrapped response)
        if 'detail' in datasets:
             print(f"Error detail: {datasets['detail']}")
             return
        # If it's a dict of datasets (legacy format?)
        found = str(dataset_id) in datasets
    else:
        found = any(d['id'] == dataset_id for d in datasets)
    if found:
        print(f"Dataset {dataset_id} found in list.")
    else:
        print(f"Dataset {dataset_id} NOT found in list.")
        return

    # 3. Get Dataset Info
    print("\n3. Testing Get Dataset Info...")
    response = client.get(f"/api/datasets/{dataset_id}")
    if response.status_code == 200:
        info = response.json()
        print(f"Got info. Rows: {info['total_rows']}")
    else:
        print(f"Get info failed: {response.text}")
        return

    # 4. Preprocess
    print("\n4. Testing Preprocessing...")
    preprocess_config = {
        "dataset_id": dataset_id,
        "steps": [
            {"type": "handle_missing", "strategies": {"col1": "mean"}}
        ]
    }
    response = client.post("/api/preprocess", json=preprocess_config)
    if response.status_code == 200:
        result = response.json()
        cleaned_id = result['cleaned_dataset_id']
        print(f"Preprocessing successful. New ID: {cleaned_id}")
    else:
        print(f"Preprocessing failed: {response.text}")
        return

    print("\nVerification Complete! Persistence is working.")

if __name__ == "__main__":
    # Ensure we have a user in DB for FK constraints (if strict)
    # But since we are mocking the user object in the dependency, 
    # the actual DB query in upload_dataset uses `current_user['id']`.
    # If the DB enforces FK on user_id, we need a real user in DB.
    # Let's insert one just in case.
    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    user = session.query(User).filter_by(id=1).first()
    if not user:
        user = User(id=1, username="testuser", email="test@example.com", hashed_password="x")
        session.add(user)
        session.commit()
    session.close()

    verify_persistence()
