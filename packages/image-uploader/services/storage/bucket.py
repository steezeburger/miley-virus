from datetime import timedelta
import uuid

from django.conf import settings
from django.utils.timezone import now
from google.cloud import storage

from core.models import User


class Bucket:

    @classmethod
    def generate_signed_upload_url(cls,
                                   *,
                                   asset_type: str,
                                   file_name: str,
                                   mime_type: str,
                                   upload_belongs_to: User) -> dict:
        storage_client = storage.Client()
        bucket_name = settings.STORAGE_BUCKET
        bucket = storage_client.bucket(bucket_name)

        unique_id = uuid.uuid4()
        blob_name = f'{upload_belongs_to.pk}/{asset_type}/{file_name}/{unique_id}'
        blob = bucket.blob(blob_name)
        expires_at = now() + timedelta(minutes=15)

        signed_url = blob.generate_signed_url(
            version='v4',
            # This URL is valid for 15 minutes
            expiration=expires_at,
            # Allow PUT requests using this URL.
            method='PUT',
            content_type=mime_type,
        )

        return {
            'expires_at': expires_at,
            'resource_path': blob_name,
            'url': signed_url,
        }

    @classmethod
    def generate_signed_download_url(cls,
                                     *,
                                     blob_name) -> dict:
        storage_client = storage.Client()
        bucket_name = settings.STORAGE_BUCKET
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(blob_name)
        expires_at = now() + timedelta(minutes=15)

        signed_url = blob.generate_signed_url(
            version='v4',
            # This URL is valid for 15 minutes
            expiration=expires_at,
            # Allow GET requests using this URL.
            method='GET',
        )
        return signed_url
