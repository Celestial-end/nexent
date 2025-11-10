"""
Storage factory for creating storage client instances

Provides factory methods to create different types of storage clients.
"""

from enum import Enum
from typing import Optional

from .storage_client_base import StorageClient
from .minio import MinIOStorageClient


class StorageType(Enum):
    """Storage type enumeration"""
    MINIO = "minio"
    # Future storage types can be added here
    # S3 = "s3"
    # AZURE = "azure"
    # GCS = "gcs"


class StorageConfig:
    """Storage configuration data class"""

    def __init__(
        self,
        storage_type: StorageType,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        region: Optional[str] = None,
        default_bucket: Optional[str] = None,
        secure: bool = True,
        **kwargs
    ):
        """
        Initialize storage configuration

        Args:
            storage_type: Type of storage backend
            endpoint: Storage endpoint URL
            access_key: Access key ID
            secret_key: Secret access key
            region: Region name
            default_bucket: Default bucket name
            secure: Whether to use HTTPS
            **kwargs: Additional configuration parameters
        """
        self.storage_type = storage_type
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.default_bucket = default_bucket
        self.secure = secure
        self.extra_config = kwargs


def create_storage_client(
    storage_type: StorageType,
    endpoint: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region: Optional[str] = None,
    default_bucket: Optional[str] = None,
    secure: bool = True,
    **kwargs
) -> StorageClient:
    """
    Factory method to create storage client instances

    Args:
        storage_type: Type of storage backend (StorageType enum)
        endpoint: Storage endpoint URL
        access_key: Access key ID
        secret_key: Secret access key
        region: Region name (optional)
        default_bucket: Default bucket name (optional)
        secure: Whether to use HTTPS (default: True)
        **kwargs: Additional configuration parameters

    Returns:
        StorageClient: Instance of the requested storage client

    Raises:
        ValueError: If storage_type is not supported or required parameters are missing

    Example:
        # Create MinIO client
        client = create_storage_client(
            storage_type=StorageType.MINIO,
            endpoint="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            default_bucket="my-bucket"
        )

        # Upload a file
        success, url = client.upload_file("local_file.txt", "remote_file.txt")
    """
    if storage_type == StorageType.MINIO:
        if not endpoint:
            raise ValueError("endpoint is required for MinIO storage")
        if not access_key:
            raise ValueError("access_key is required for MinIO storage")
        if not secret_key:
            raise ValueError("secret_key is required for MinIO storage")

        return MinIOStorageClient(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            default_bucket=default_bucket,
            secure=secure
        )
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")


def create_storage_client_from_config(config: StorageConfig) -> StorageClient:
    """
    Create storage client from configuration object

    Args:
        config: StorageConfig instance

    Returns:
        StorageClient: Instance of the requested storage client

    Example:
        config = StorageConfig(
            storage_type=StorageType.MINIO,
            endpoint="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin"
        )
        client = create_storage_client_from_config(config)
    """
    return create_storage_client(
        storage_type=config.storage_type,
        endpoint=config.endpoint,
        access_key=config.access_key,
        secret_key=config.secret_key,
        region=config.region,
        default_bucket=config.default_bucket,
        secure=config.secure,
        **config.extra_config
    )

