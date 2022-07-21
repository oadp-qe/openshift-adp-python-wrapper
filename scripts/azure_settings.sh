#!/bin/bash

cat > $TMP_DIR/azure_settings.json <<EOF
{
  "metadata": {
    "namespace": "$NAMESPACE"
  },
  "spec": {
      "configuration":{
        "velero":{
          "defaultPlugins": [
            "openshift", "$PROVIDER"
          ]
        }
      },
      "backupLocations": [
        {
          "velero": {
            "default": true,
            "provider": "$PROVIDER",
            "config": {
                "resourceGroup": "$AZURE_RESOURCE_GROUP",
                "storageAccount": "$AZURE_STORAGE_ACCOUNT_ID",
                "storageAccountKeyEnvVar": "AZURE_STORAGE_ACCOUNT_ACCESS_KEY",
                "subscriptionId": "$AZURE_SUBSCRIPTION_ID"
            },
            "credential":{
                "name": "$CREDS_SECRET_REF",
                "key": "cloud"
            },
            "objectStorage":{
              "bucket": "$BUCKET"
            }
          }
        }
      ]
EOF

if [[ $CLOUD_PROVIDER == "azure" ]]; then
cat >> $TMP_DIR/azure_settings.json << EOF
,
      "snapshotLocations": [
        {
          "velero": {
            "provider": "$CLOUD_PROVIDER",
            "config": {
                "resourceGroup": "$AZURE_RESOURCE_GROUP",
                "subscriptionId": "$AZURE_SUBSCRIPTION_ID"
            }
          }
        }
      ]
EOF
fi

echo -e "\n  }\n}" >>  $TMP_DIR/azure_settings.json


x=$(cat $TMP_DIR/azure_settings.json); echo "$x" | grep -o '^[^#]*'  > $TMP_DIR/azure_settings.json
