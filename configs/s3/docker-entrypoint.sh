#!/bin/sh
set -e

MINIO_ACCESS_KEY=${MINIO_ROOT_USER}
MINIO_SECRET_KEY=${MINIO_ROOT_PASSWORD}
MINIO_HOST="http://localhost:9000"

create_bucket() {
  echo "Creating bucket: $BUCKET_NAME"
  mc alias set myminio $MINIO_HOST $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
  mc mb myminio/$BUCKET_NAME
  mc anonymous set download myminio/$BUCKET_NAME
}

initialize_mc() {
  echo "Initializing MinIO Client"
  mc alias set myminio $MINIO_HOST $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
}

minio server /data --console-address ":9090" &

sleep 5

initialize_mc || true
create_bucket || true

wait
