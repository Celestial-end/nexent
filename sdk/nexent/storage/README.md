# Storage Module

Storage abstraction layer for Nexent SDK, providing a unified interface for different storage backends.

## Features

- **Abstract Factory Pattern**: Define common storage interface
- **Multiple Backends**: Support for MinIO and S3-compatible storage
- **Easy to Extend**: Add new storage backends by implementing `StorageClient` interface
- **Type Safe**: Full type hints support

## Quick Start

### Create a Storage Client

```python
from nexent.storage import create_storage_client, StorageType

# Create MinIO client
client = create_storage_client(
    storage_type=StorageType.MINIO,
    endpoint="http://localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    default_bucket="my-bucket"
)
```

### Upload Files

```python
# Upload local file
success, url = client.upload_file(
    file_path="local_file.txt",
    object_name="remote_file.txt"
)

# Upload file object
from io import BytesIO
file_obj = BytesIO(b"file content")
success, url = client.upload_fileobj(
    file_obj=file_obj,
    object_name="remote_file.txt"
)
```

### Download Files

```python
# Download file to local
success, message = client.download_file(
    object_name="remote_file.txt",
    file_path="local_file.txt"
)

# Get file stream
success, stream = client.get_file_stream(
    object_name="remote_file.txt"
)
if success:
    content = stream.read()
```

### Get File Information

```python
# Get file size
size = client.get_file_size("remote_file.txt")

# Check if file exists
exists = client.exists("remote_file.txt")

# Get presigned URL
success, url = client.get_file_url(
    object_name="remote_file.txt",
    expires=3600  # 1 hour
)
```

### List Files

```python
# List all files
files = client.list_files()

# List files with prefix
files = client.list_files(prefix="images/")
```

### Delete Files

```python
# Delete file
success, message = client.delete_file("remote_file.txt")
```

## API Reference

### StorageClient (Abstract Base Class)

All storage implementations must implement these methods:

- `upload_file(file_path, object_name=None, bucket=None) -> Tuple[bool, str]`
- `upload_fileobj(file_obj, object_name, bucket=None) -> Tuple[bool, str]`
- `download_file(object_name, file_path, bucket=None) -> Tuple[bool, str]`
- `get_file_url(object_name, bucket=None, expires=3600) -> Tuple[bool, str]`
- `get_file_stream(object_name, bucket=None) -> Tuple[bool, Any]`
- `get_file_size(object_name, bucket=None) -> int`
- `list_files(prefix="", bucket=None) -> List[Dict[str, Any]]`
- `delete_file(object_name, bucket=None) -> Tuple[bool, str]`
- `exists(object_name, bucket=None) -> bool`

### MinIOStorageClient

MinIO storage implementation using boto3.

**Constructor Parameters:**
- `endpoint`: MinIO endpoint URL (required)
- `access_key`: Access key ID (required)
- `secret_key`: Secret access key (required)
- `region`: AWS region name (optional, default: "us-east-1")
- `default_bucket`: Default bucket name (optional)
- `secure`: Whether to use HTTPS (default: True)

### Factory Methods

#### create_storage_client()

Create a storage client instance.

```python
client = create_storage_client(
    storage_type=StorageType.MINIO,
    endpoint="http://localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    default_bucket="my-bucket"
)
```

#### create_storage_client_from_config()

Create a storage client from a `StorageConfig` object.

```python
from nexent.storage import StorageConfig, StorageType

config = StorageConfig(
    storage_type=StorageType.MINIO,
    endpoint="http://localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    default_bucket="my-bucket"
)

client = create_storage_client_from_config(config)
```

## Extending the Storage Module

To add a new storage backend:

1. Create a new class inheriting from `StorageClient`
2. Implement all abstract methods
3. Add the new storage type to `StorageType` enum
4. Update `create_storage_client()` factory method

Example:

```python
from .base import StorageClient

class MyStorageClient(StorageClient):
    def __init__(self, config_param1, config_param2):
        # Initialize your storage client
        pass
    
    def upload_file(self, file_path, object_name=None, bucket=None):
        # Implement upload logic
        pass
    
    # Implement other abstract methods...
```

## Error Handling

All methods return tuples with success status:
- `(True, result)` on success
- `(False, error_message)` on failure

Example:

```python
success, result = client.upload_file("file.txt", "remote.txt")
if success:
    print(f"Uploaded to: {result}")
else:
    print(f"Error: {result}")
```

## Notes

- The SDK follows the environment variable rule: it does not read environment variables directly. Configuration must be passed as parameters.
- All file paths use forward slashes (`/`) for object names.
- Bucket names are optional if `default_bucket` is set during initialization.

