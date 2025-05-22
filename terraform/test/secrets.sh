#!/bin/bash

REGION="us-east-1"

SECRET_NAMES=$(aws secretsmanager list-secrets --region $REGION --query 'SecretList[].Name' --output text)

for SECRET_NAME in $SECRET_NAMES; do
  echo "Processing secret: $SECRET_NAME"

  SECRET_VALUE=$(aws secretsmanager get-secret-value \
    --secret-id "$SECRET_NAME" \
    --region "$REGION" \
    --query SecretString \
    --output text)

  if [ -z "$SECRET_VALUE" ] || [ "$SECRET_VALUE" == "null" ]; then
    echo "Secret $SECRET_NAME has no plain string value, skipping..."
    continue
  fi

  # Remove all newline characters
  CLEAN_VALUE=$(echo -n "$SECRET_VALUE" | tr -d '\r\n')

  if [ "$SECRET_VALUE" == "$CLEAN_VALUE" ]; then
    echo "No newline characters found, skipping update."
    continue
  fi

  aws secretsmanager update-secret \
    --secret-id "$SECRET_NAME" \
    --region "$REGION" \
    --secret-string "$CLEAN_VALUE"

  echo "Updated secret: $SECRET_NAME"
done

