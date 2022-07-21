#!/bin/bash
cat > $TMP_DIR/s3_settings.json <<EOF
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
            "provider": "$PROVIDER",
            "default": true,
            "config": {
                "insecureSkipTLSVerify": "true",
                "profile": "$PROFILE",
                "region": "$REGION",
                "s3ForcePathStyle": "true",
                "s3Url": "$S3_URL"
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
  }
}
EOF

x=$(cat $TMP_DIR/s3_settings.json); echo "$x" | grep -o '^[^#]*'  > $TMP_DIR/s3_settings.json

# temporarily create restic-secret (until https://github.com/openshift/oadp-operator/pull/747 is merged)
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: restic-secret
  namespace: $NAMESPACE
type: Opaque
stringData:
  # The repository url
  RESTIC_REPOSITORY: s3:$S3_URL/$BUCKET
  # The repository encryption key
  RESTIC_PASSWORD: my-secure-restic-password
  # ENV vars specific to the chosen back end
  # https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
  AWS_ACCESS_KEY_ID: $(cat $OADP_CREDS_FILE | awk -F  "=" '/aws_access_key_id/ {print $2}')
  AWS_SECRET_ACCESS_KEY: $(cat $OADP_CREDS_FILE | awk -F  "=" '/aws_secret_access_key/ {print $2}')
EOF