#!/bin/sh

# Encrypt secrets to upload to github

echo "$LARGE_SECRET_PASSPHRASE" | \
gpg --batch --yes --passphrase-fd 0 --symmetric --cipher-algo AES256 \
credentials_user.json

echo "$LARGE_SECRET_PASSPHRASE" | \
gpg --batch --yes --passphrase-fd 0 --symmetric --cipher-algo AES256 \
credentials_service_account.json

echo "$LARGE_SECRET_PASSPHRASE" | \
gpg --batch --yes --passphrase-fd 0 --symmetric --cipher-algo AES256 \
calendar_secrets.json
