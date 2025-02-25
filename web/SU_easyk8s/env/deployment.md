### 部署指南

1. K3S without traefik
```
curl –sfL \
    https://rancher-mirror.rancher.cn/k3s/k3s-install.sh |INSTALL_K3S_EXEC="server --disable traefik" INSTALL_K3S_MIRROR=cn sh -s - \
     --system-default-registry "change it"
```

2. helm charts 

安装 nginx-ingress 和 nfs-subdir-external-provisioner 

```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod u+x get_helm.sh && ./get_helm.sh
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
helm repo add nginx-stable https://helm.nginx.com/stable
helm install nginx-ingress nginx-stable/nginx-ingress --create-namespace --set rbac.create=true --namespace ingress-nginx

helm install --namespace kube-system nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
--set nfs.server='0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com' \
--set nfs.path=/nfs-root  \
--set image.repository=registry.cn-hangzhou.aliyuncs.com/k8s_sys/nfs-subdir-external-provisioner \
--set image.tag=v4.0.2 \
--set storageClass.name=nfs-client \
--set storageClass.defaultClass=false 
```

3. len-metrics with kube-state-metrics

> just open in Lens

4. 安装 python app

```
kubectl apply -f ./k8s/deploy.yaml -f ./k8s/pv.yaml -f ./k8s/rolling.yaml
```
