import requests
import os
import json

BASE_URL = "http://localhost:8000"

def test_versioning():
    try:
        # 1. Login
        login_data = {"username": "atharva", "password": "password123"}
        print("Attempting login...")
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        
        if resp.status_code != 200:
            print("Login failed. Trying to register...")
            reg_data = {
                "username": "atharva", 
                "email": "atharva@test.com", 
                "password": "password123",
                "full_name": "Atharva"
            }
            requests.post(f"{BASE_URL}/api/auth/register", json=reg_data)
            resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        
        if resp.status_code != 200:
            print(f"Could not authenticate: {resp.text}")
            return

        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get initial count
        resp = requests.get(f"{BASE_URL}/api/datasets", headers=headers)
        initial_count = len(resp.json())
        print(f"Initial dataset count: {initial_count}")

        # 3. Upload a small dataset
        csv_content = "id,name,age\n1,Alice,30\n2,Bob,25\n3,Charlie,35"
        files = {'file': ('test_versioning.csv', csv_content, 'text/csv')}
        print("Uploading test dataset...")
        resp = requests.post(f"{BASE_URL}/api/upload-dataset", headers=headers, files=files)
        dataset_id = str(resp.json()["dataset_id"])
        print(f"Uploaded dataset. ID: {dataset_id}")
        
        # 4. Preprocess (Drop a column) - This should be a DRAFT now
        print("Applying preprocessing (Drop 'age' column)...")
        preprocess_config = {
            "dataset_id": dataset_id,
            "steps": [
                {"type": "remove_columns", "columns": ["age"]}
            ]
        }
        resp = requests.post(f"{BASE_URL}/api/preprocess", headers=headers, json=preprocess_config)
        if resp.status_code == 200:
            print("Preprocessing draft applied successfully.")
        else:
            print(f"Preprocessing failed: {resp.text}")
            return
        
        # 5. Check if a new dataset record was created (It SHOULD NOT have been)
        resp = requests.get(f"{BASE_URL}/api/datasets", headers=headers)
        post_draft_count = len(resp.json())
        print(f"Dataset count after draft: {post_draft_count}")
        
        if post_draft_count != initial_count + 1:
            print("FAILURE: A new database record was created during preprocessing draft!")
        else:
            print("SUCCESS: Preprocessing remained in-memory (No version bloat).")
        
        # 6. Save as Version
        version_name = f"Cleaned_V_Test_{os.urandom(2).hex()}"
        print(f"Saving version as '{version_name}'...")
        resp = requests.post(
            f"{BASE_URL}/api/datasets/{dataset_id}/save-version", 
            headers=headers, 
            json={"version_name": version_name}
        )
        
        if resp.status_code != 200:
            print(f"Save version failed: {resp.text}")
            return
            
        version_result = resp.json()
        print(f"Save version result: {version_result['message']}")
        version_id = str(version_result["dataset_id"])
        
        # 7. Verify the new version exists in DB
        resp = requests.get(f"{BASE_URL}/api/datasets", headers=headers)
        datasets = resp.json()
        final_count = len(datasets)
        print(f"Final dataset count: {final_count}")
        
        new_version = next((d for d in datasets if str(d["id"]) == version_id), None)
        
        if new_version:
            print(f"VERIFICATION SUCCESS: Version '{version_name}' found in database.")
            print(f"Details: Rows={new_version['rows']}, Columns={new_version['column_count']}")
            if new_version['column_count'] == 2:
                 print("Correct column count (age was dropped).")
            else:
                 print(f"Incorrect column count: {new_version['column_count']} (expected 2)")
        else:
            print("VERIFICATION FAILURE: New version record not found.")

    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    test_versioning()
