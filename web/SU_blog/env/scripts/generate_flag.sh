#!/bin/bash

# 设置静态flag
flag="SUCTF{fl4sk_1s_5imp1e_bu7_pyd45h_1s_n0t_s0_I_l0v3}"

# 将flag写入/flag文件
echo "$flag" > /flag

# 设置适当的权限
chmod 400 /flag
chown root:root /flag