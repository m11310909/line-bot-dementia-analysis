from google.cloud import aiplatform
import os

# 確保以下三行環境變數已經 export
#   GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID
project_id = os.getenv("PROJECT_ID")

# 這裡先假設你猜測是 asia-east1，如果不是再改其他
for region in ["asia-east1","us-central1","us-west1","asia-northeast1"]:
    try:
        aiplatform.init(project=project_id, location=region)
        models = aiplatform.Model.list()
        if models:
            print(f"Regions: {region}")
            for m in models:
                print("  ", m.display_name)
            break
    except Exception:
        pass
else:
    print("No models found in tested regions.")
