
<h1 align="center">dpa_settings_json_generator.sh variables</h1>

This document explains the variables one can export for the dpa_settings_json_generator.sh script, available options, and their default value set by the script if the variable was not defined (exported).

- [common variables](#common-variables)
  * [`CLOUD_PROVIDER`](#cloud_provider)
  * [`NAMESPACE`](#namespace)
  * [`BACKUP_LOCATION`](#backup_location)
  * [`BUCKET`](#bucket)
  * [`OADP_CREDS_FILE`](#oadp_creds_file)
  * [`TESTS_FOLDER`](#tests_folder)
  * [`CREDS_SECRET_REF`](#creds_secret_ref)
- [Specific backup location variables](#specific-backup-location-variables)
  * [`BACKUP_LOCATION` equals "aws" or "awss3":](#backup_location-equals-aws-or-awss3)
    + [`REGION`](#region)
  * [`BACKUP_LOCATION` equals "gcp"](#backup_location-equals-gcp)
    + [`REGION`](#region-1)
    + [`PROJECT_ID`](#project_id)
  * [`BACKUP_LOCATION` equals "azure":](#backup_location-equals-azure)
    + [`AZURE_STORAGE_ACCOUNT_ID`](#azure_storage_account_id)
  * [`BACKUP_LOCATION` equals "minio"/"mcg"/"ibmcloud" (S3 compatible)](#backup_location-equals-miniomcgibmcloud-s3-compatible)
    + [`REGION`](#region-2)
    + [`PROFILE`](#profile)


## common variables

### `CLOUD_PROVIDER`
* **description:** the cluster type
* **available options:**  aws, gcp, azure, openstack, none (currently used for ibm on premise), ibmcloud
* **default value:** `$(oc get infrastructures cluster -o jsonpath='{.status.platform}' | awk '{print tolower($0)}')`


### `NAMESPACE`
* **description:** the namespace where the OADP operator is installed.
* **available options:** The test cases assume the OADP operator is installed, so it should be the exact namespace where the operator is installed.
* **default value:** openshift-adp

### `BACKUP_LOCATION`
* **description:** the default backup location of the DPA CR
* **available options:** aws/awss3, gcp, azure, minio, mcg, ibmcloud
* **default value:** defaults to the value of `CLOUD_PROVIDER` variable


### `BUCKET`
* **description:** the object storage (bucket) name
* **available options:** the name any bucket available on the `BACKUP_LOCATION` with the correct permissions (`OADP_CREDS_FILE`)
* **default value:** defaults to the value of `CLOUD_PROVIDER` variable.


### `OADP_CREDS_FILE`
* **description:** the path to the credentials file required for object storage backup and restore and for native snapshots (if available).
* **available options:** the location of the credentials file on your local machine
* **default value:** /tmp/test-settings/${CLOUD_PROVIDER}_creds


### `TESTS_FOLDER`
* **description:** the location of the suite you want to execute
* **available options:** e2e/, upgrade/, e2e/kubevirt/tests
* **default value:** e2e/


### `CREDS_SECRET_REF`
* **description:** the secret name reference used for the default backup location and the default snapshot location (if available).
* **available options:** could be changed to any name, but it's **not** recommended to change the defaults, due to VSL name limitation to some defaults. For more information, please refer the explanation on [Using Credentials with the OADP Operator](https://github.com/openshift/oadp-operator/blob/master/docs/credentials.md#using-credentials-with-the-oadp-operator)
* **default value:** 
    * for aws: cloud-credentials
    * for gcp: cloud-credentials-gcp
    * for azure: cloud-credentials-azure
    * for any other S3 compatible backup location: cloud-credentials

## Specific backup location variables

The following variables are specifc to the backup location, depending on the value of the `BACKUP_LOCATION` variable. The variables' values will be ignored/not set if they are not relevant to the `BACKUP_LOCATION`.

### `BACKUP_LOCATION` equals "aws" or "awss3":
#### `REGION`
* **description:** the AWS region where the object stoage/bucket (`BUCKET`) is located 
* **available options:** the AWS region where the object stoage/bucket (`BUCKET`) is located 
* **default value:** `$(oc get infrastructures cluster -o jsonpath='{.status.platformStatus.aws.region}' --allow-missing-template-keys=false 2> /dev/null || echo'us-east-2')` - meaning: if the cluster type is AWS, it will use the cluster's region from `oc get infrastructures cluster` or if it's not, it will default to us-east-2

### `BACKUP_LOCATION` equals "gcp"
#### `REGION`
* **description:** the GCP region where the cluster is located. If it's not a GCP cluster, this variable setting is not required as it's used for native snapshot configuration. 
* **available options:** the GCP region where the cluster is located (in case of GCP cluster)
* **default value:** `$(oc get infrastructures cluster -o jsonpath='{.status.platformStatus.gcp.region}' --allow-missing-template-keys=false 2> /dev/null || "us-central1")` - meaning: if the cluster type is GCP, it will use the cluster's region from `oc get infrastructures cluster` or if it's not, it will default to us-central1

#### `PROJECT_ID`
* **description:** the GCP project ID used for native snapshots backup-restore. If it's not a GCP cluster, this variable setting is not required as it's used for native snapshot configuration. 
* **available options:** a valid GCP project ID used for native snapshots backup-restore (in case of GCP cluster).
* **default value:** openshift-qe # TODO: use as default the value from `oc get infrastructures cluster` command

### `BACKUP_LOCATION` equals "azure":
#### `AZURE_STORAGE_ACCOUNT_ID`
* **description:** the storage account ID where the Azure Container Blob (the `BUCKET`) resides.
* **available options:** a valid storage account ID where the Azure Container Blob (the `BUCKET`) resides.
* **default value:** defaults to the value of `BUCKET` variable (just to simplify QE's CI process)

### `BACKUP_LOCATION` equals "minio"/"mcg"/"ibmcloud" (S3 compatible)
#### `REGION`
* **description:** for minio/mcg/ibmcloud region could be any allowed string.
* **available options:** for minio/mcg/ibmcloud region could be any allowed string.
* **default value:**
    * for minio: "minio"
    * for mcg: "noobaa"
    * for ibmcloud: no default


#### `PROFILE`
* **description:** the profile of the credentials to be used from the `OADP_CREDS_FILE`.
* **available options:** depends on the profiles available in the `OADP_CREDS_FILE`.
* **default value:**
    * for minio: "minio"
    * for mcg: "noobaa"
    * for ibmcloud: "default"