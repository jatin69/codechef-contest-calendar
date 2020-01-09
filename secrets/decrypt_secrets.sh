#!/bin/sh

# Decrypt the secrets

# --quiet   : Try to be as quiet as possible.
# --batch   : to prevent interactive command 
# --yes     : to assume "yes" for questions
# --decrypt : to specify decryption mode

gpg --quiet --batch --yes --decrypt \
--passphrase="$LARGE_SECRET_PASSPHRASE" --output \
credentials_user.json \
credentials_user.json.gpg

gpg --quiet --batch --yes --decrypt \
--passphrase="$LARGE_SECRET_PASSPHRASE" --output \
credentials_service_account.json \
credentials_service_account.json.gpg

gpg --quiet --batch --yes --decrypt \
--passphrase="$LARGE_SECRET_PASSPHRASE" --output \
calendar_secrets.json \
calendar_secrets.json.gpg
