import sys

DEBUG = False

def audit_hook(event, args):
    audit_functions = {
        "os.system": {"ban": True},
        "subprocess.Popen": {"ban": True},
        "subprocess.run": {"ban": True},
        "subprocess.call": {"ban": True},
        "subprocess.check_call": {"ban": True},
        "subprocess.check_output": {"ban": True},
        "_posixsubprocess.fork_exec": {"ban": True},
        "os.spawn": {"ban": True},
        "os.spawnlp": {"ban": True},
        "os.spawnv": {"ban": True},
        "os.spawnve": {"ban": True},
        "os.exec": {"ban": True},
        "os.execve": {"ban": True},
        "os.execvp": {"ban": True},
        "os.execvpe": {"ban": True},
        "os.fork": {"ban": True},
        "shutil.run": {"ban": True},
        "ctypes.dlsym": {"ban": True},
        "ctypes.dlopen": {"ban": True}
    }
    if event in audit_functions:
        if DEBUG:
            print(f"[DEBUG] found event {event}")
        policy = audit_functions[event]
        if policy["ban"]:
            strr = f"AUDIT BAN : Banning FUNC:[{event}] with ARGS: {args}"
            print(strr)
            raise PermissionError(f"[AUDIT BANNED]{event} is not allowed.")
        else:
            strr = f"[DEBUG] AUDIT ALLOW : Allowing FUNC:[{event}] with ARGS: {args}"
            print(strr)
            return

sys.addaudithook(audit_hook)