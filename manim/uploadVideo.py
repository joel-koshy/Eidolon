import argparse
import os
from google.cloud import storage
from google.api_core import exceptions

def upload_video_to_gcs(bucket_name, source_file_path, destination_blob_name=None):
    
    try:
        storage_client = storage.Client()
    except Exception as e:
        print("Error initializing GCS client. Is google-cloud-storage installed?")
        print(f"Authentication Error: {e}")
        print("Please run `gcloud auth application-default login` or set GOOGLE_APPLICATION_CREDENTIALS.")
        return

    # --- 2. Check if local file exists ---
    if not os.path.exists(source_file_path):
        print(f"Error: Source file not found at '{source_file_path}'")
        return

    # --- 3. Set destination blob name ---
    if destination_blob_name is None:
        # Use the local filename as the destination name
        destination_blob_name = os.path.basename(source_file_path)

    try:
        # --- 4. Get the bucket ---
        bucket = storage_client.bucket(bucket_name)

        # --- 5. Create a new blob (file object) in the bucket ---
        blob = bucket.blob(destination_blob_name)

        # --- 6. Upload the file ---
        print(f"Uploading '{source_file_path}' to 'gs://{bucket_name}/{destination_blob_name}'...")
        
        # You can also use `upload_from_file` if you have an open file object.
        # `upload_from_filename` is efficient for large files.
        blob.upload_from_filename(source_file_path)

        print(f"File uploaded successfully.")
        print(f"Public URL: {blob.public_url}")
        return blob.public_url

    except exceptions.NotFound:
        print(f"Error: Bucket '{bucket_name}' not found.")
    except exceptions.Forbidden as e:
        print(f"Error: Permission denied for bucket '{bucket_name}'.")
        print("Does your account have 'Storage Object Admin' or 'Storage Object Creator' role?")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    upload_video_to_gcs(
        bucket_name="eidolon-videos",
        source_file_path="./media/videos/test/480p15/IntegralExplanation.mp4",
    )