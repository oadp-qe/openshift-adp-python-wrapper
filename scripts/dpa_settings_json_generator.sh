#!/bin/bash
set -x
readonly RED='\e[31m'
readonly BLUE='\033[34m'
readonly CLEAR='\e[39m'
CLOUD_PROVIDER=${CLOUD_PROVIDER:-$(oc get infrastructures cluster -o jsonpath='{.status.platform}' | awk '{print tolower($0)}')}
# Changeable test params; if you want to change them:
# * export them before running the script;
# * or just assign them with the script execution, e.g,  `OADP_TEST_NAMESPACE="velero" /bin/bash e2e/scripts/test_runner.sh`
E2E_TIMEOUT_MULTIPLIER=${E2E_TIMEOUT_MULTIPLIER:-2}
export NAMESPACE=${NAMESPACE:-"openshift-adp"}
export PROVIDER=${PROVIDER:-"$CLOUD_PROVIDER"}
BACKUP_LOCATION=$(echo $BACKUP_LOCATION | awk '{print tolower($0)}') # if BACKUP_LOCATION defined, use lower case
export BACKUP_LOCATION=${BACKUP_LOCATION:-"$PROVIDER"}
export BUCKET=${BUCKET:-"mybucket"}

OADP_CREDS_FILE=${OADP_CREDS_FILE:-"/tmp/test-settings/${PROVIDER}_creds"}
readonly SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
readonly TOP_DIR=$(cd "${SCRIPT_DIR}"; git rev-parse --show-toplevel)
TESTS_FOLDER=${TESTS_FOLDER:-"e2e/"}

#################################################################################################################################

verify_param_exist(){
  local PARAM=$1
  if [ -z "${!PARAM}" ]; then
      printf "${RED}$PARAM not set. flagging for exit.${CLEAR}\n"
      exit 1
  fi
}

# TODO: explain on README this filter
TEST_FILTER=" !// || target_$CLOUD_PROVIDER || !/target/ && (mr-check || vsl || (/exclude/ && !exclude_$CLOUD_PROVIDER) ) "
if [[ "$CLOUD_PROVIDER" != "aws" && "$CLOUD_PROVIDER" != "gcp" && "$CLOUD_PROVIDER" != "azure" ]]; then
    TEST_FILTER=" ( $(echo $TEST_FILTER) ) && !vsl " # exclude VSL-based test cases
fi

SETTINGS_TMP=$TOP_DIR/output_files/test-settings-$RANDOM
mkdir $SETTINGS_TMP


if [[ "$BACKUP_LOCATION" == "aws" || "$BACKUP_LOCATION" == "awss3" ]]; then
    export PROVIDER="aws"
    export CREDS_SECRET_REF=${CREDS_SECRET_REF:-"cloud-credentials"}
    export REGION=${REGION:-$(oc get infrastructures cluster -o jsonpath='{.status.platformStatus.aws.region}' --allow-missing-template-keys=false 2> /dev/null || echo'us-east-2')} # export REGION or just assign with the script execution, e.g,  `REGION="us-east-1" /bin/bash e2e/scripts/test_runner.sh`
    BUCKET="$BUCKET" TMP_DIR=$SETTINGS_TMP source $SCRIPT_DIR/aws_settings.sh
elif [[ "$BACKUP_LOCATION" == "gcp" ]]; then
    export PROVIDER="gcp"
    export CREDS_SECRET_REF=${CREDS_SECRET_REF:-"cloud-credentials-gcp"}
    export PROJECT_ID=${PROJECT_ID:-"openshift-qe"} # export PROJECT_ID
    export REGION=$(oc get infrastructures cluster -o jsonpath='{.status.platformStatus.gcp.region}' --allow-missing-template-keys=false 2> /dev/null || "us-central1") # export REGION or just assign with the script execution, e.g,  `REGION="us-east-1" /bin/bash e2e/scripts/test_runner.sh`
    BUCKET="$BUCKET" TMP_DIR=$SETTINGS_TMP source $SCRIPT_DIR/gcp_settings.sh
elif [[ "$BACKUP_LOCATION" == "azure" ]]; then
    export PROVIDER="azure"
    export CREDS_SECRET_REF=${CREDS_SECRET_REF:-"cloud-credentials-azure"}
    export AZURE_SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID:-"$(cat "${OADP_CREDS_FILE}" | awk -F  "=" '/AZURE_SUBSCRIPTION_ID/ {print $2}')"}
    verify_param_exist AZURE_SUBSCRIPTION_ID
    export AZURE_STORAGE_ACCOUNT_ID=${AZURE_STORAGE_ACCOUNT_ID:-$BUCKET}
    verify_param_exist AZURE_STORAGE_ACCOUNT_ID
    AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-"$(cat "${OADP_CREDS_FILE}" | awk -F  "=" '/AZURE_RESOURCE_GROUP/ {print $2}')"} # in case defined in creds file 
    # otherwise take the resource group from the cluster
    export AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-$(oc get infrastructures cluster -o jsonpath='{.status.platformStatus.azure.resourceGroupName}' --allow-missing-template-keys=false 2> /dev/null || true)} 
    verify_param_exist AZURE_RESOURCE_GROUP
    BUCKET="$BUCKET" TMP_DIR=$SETTINGS_TMP source $SCRIPT_DIR/azure_settings.sh
else # the rest
    export CREDS_SECRET_REF=${CREDS_SECRET_REF:-"cloud-credentials"}
    export PROVIDER="aws" # for S3 compatible storage, the provider should be aws
    if [[ "$BACKUP_LOCATION" == "minio" ]]; then
        export PROFILE=${PROFILE:-"minio"}
        export REGION=${REGION:-"minio"}
        S3_URL="http://$(oc get route minio -n minio -o jsonpath='{.spec.host}')"
    elif [[ "$BACKUP_LOCATION" == "mcg" ]]; then
        export PROFILE=${PROFILE:-"noobaa"}
        export REGION=${REGION:-"noobaa"}
        DEFAULT_SC=$(oc get storageclass -o jsonpath="{.items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=='true')].metadata.name}")
        S3_URL="https://$(oc get route s3 -n openshift-storage -o jsonpath='{.spec.host}')"
    elif [[ "$BACKUP_LOCATION" == "ibmcloud" ]]; then
        export REGION=${REGION:-}
        export PROFILE=${PROFILE:-"default"}
        S3_URL="https://s3.$REGION.cloud-object-storage.appdomain.cloud"
    fi
    S3_URL="$S3_URL" TMP_DIR=$SETTINGS_TMP /bin/bash $SCRIPT_DIR/s3_settings.sh
    FILE_SETTINGS_NAME=s3_settings.json
fi
FILE_SETTINGS_NAME=${FILE_SETTINGS_NAME:-"${PROVIDER}_settings.json"}
printf "${BLUE}Generated settings file under $SETTINGS_TMP/$FILE_SETTINGS_NAME${CLEAR}\n"


