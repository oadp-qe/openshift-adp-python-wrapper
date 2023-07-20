# -*- coding: utf-8 -*-

from ocp_resources.resource import Resource


class StorageClass(Resource):
    """
    StorageClass object.
    """

    api_group = Resource.ApiGroup.STORAGE_K8S_IO
    def __init__(
        self,
        name=None,
        client=None,
        provisioner=None,
        volume_binding_mode=None,
        teardown=True,
        yaml_file=None,
        **kwargs,
    ):
        super().__init__(
            client=client,
            name=name,
            teardown=teardown,
            yaml_file=yaml_file,
            **kwargs,
        )
        self.provisioner = provisioner
        self.volume_binding_mode = volume_binding_mode

    def to_dict(self):
        if not self.res:
            super().to_dict()

        if not self.yaml_file and self.provisioner:
            self.set_provisioner(
                provisioner=self.provisioner,
                volume_binding_mode=self.volume_binding_mode,
            )

    def set_provisioner(self,provisioner=None, volume_binding_mode=None):
        if not self.res:
            super().to_dict()
        self.res["provisioner"]=provisioner
        if volume_binding_mode:
            self.res["volumeBindingMode"]=volume_binding_mode

    class Types:
        """
        These are names of StorageClass instances when you run `oc get sc`
        """

        LOCAL_BLOCK = "local-block"
        HOSTPATH = "hostpath-provisioner"
        CEPH_RBD = "ocs-storagecluster-ceph-rbd"
        NFS = "nfs"
        HOSTPATH_CSI = "hostpath-csi"

    class Provisioner:
        HOSTPATH = "kubevirt.io/hostpath-provisioner"
        NO_PROVISIONER = "kubernetes.io/no-provisioner"
        CEPH_RBD = "openshift-storage.rbd.csi.ceph.com"
        CEPHFS="openshift-storage.cephfs.csi.ceph.com"
        HOSTPATH_CSI = "kubevirt.io.hostpath-provisioner"

    class VolumeBindingMode:
        """
        VolumeBindingMode indicates how PersistentVolumeClaims should be provisioned and bound.
        When unset, Immediate is used.
        When "Immediate", if you want to use the "node aware" hostpath-provisioner,
        ProvisionOnNode annotations should be introduced to PVC.
        Or in order to be able to use the hpp without specifying the node on the PVC,
        since CNV-2.2, hpp supports for "WaitForFirstConsumer".
        """

        # TODO: Rename to Uppercase
        Immediate = "Immediate"
        WaitForFirstConsumer = "WaitForFirstConsumer"

    class Annotations:
        IS_DEFAULT_CLASS = (
            f"{Resource.ApiGroup.STORAGECLASS_KUBERNETES_IO}/is-default-class"
        )

