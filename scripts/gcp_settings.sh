#!/bin/bash

cat > $TMP_DIR/gcp_settings.json <<EOF

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

if [[ $CLOUD_PROVIDER == "gcp" ]]; then
cat >> $TMP_DIR/gcp_settings.json << EOF
,
      "snapshotLocations": [
        {
          "velero": {
            "provider": "$PROVIDER",
            "config": {
              "snapshotLocation" : "$REGION",
              "project": "$PROJECT_ID"
            }
          }
        }
      ]
EOF
fi

echo -e "\n  }\n}" >>  $TMP_DIR/gcp_settings.json

x=$(cat $TMP_DIR/gcp_settings.json); echo "$x" | grep -o '^[^#]*'  > $TMP_DIR/gcp_settings.json
