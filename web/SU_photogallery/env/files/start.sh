#!/bin/bash
###
 # @Author: Nbc
 # @Date: 2025-01-13 16:13:47
 # @LastEditors: Nbc
 # @LastEditTime: 2025-01-13 16:32:19
 # @FilePath: \files\start.sh
 # @Description: 
 # 
 # Copyright (c) 2025 by Nbc, All Rights Reserved. 
### 

if [[ -f /flag.sh ]]; then
	source /flag.sh
	rm -f /flag.sh
fi


# 启动服务
php -S 0.0.0.0:80 -t /tmp/suctf_web/ -d expose_php=off -d disable_functions="passthru,exec,putenv,chroot,chgrp,chown,shell_exec,popen,proc_open,pcntl_exec,ini_alter,ini_restore,dl,openlog,syslog,readlink,symlink,popepassthru,pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,imap_open,apache_setenv"
