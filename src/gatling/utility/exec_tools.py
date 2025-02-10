import subprocess
import os


def execute_commands(cmds, block=True):
    """
    Executes a list of commands in a new cmd window and optionally blocks until they complete.

    Args:
        cmds (list of str): List of commands to execute.
        block (bool): If True, the function will block until the commands finish.
                      If False, the function will return immediately with the PID.

    Returns:
        int: The PID of the created process.
    """
    try:
        # si = subprocess.STARTUPINFO()
        # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # si.wShowWindow = win32con.SW_HIDE  # 不显示窗口
        # 将命令列表组合成一个以 & 连接的字符串
        combined_cmds = " & ".join(cmds)

        # 构造完整的 cmd 命令
        full_command = f'cmd /c "{combined_cmds}"'

        # 启动新进程
        process = subprocess.Popen(
            full_command,
            creationflags=subprocess.CREATE_NEW_CONSOLE,  # 打开新窗口
            shell=False
        )

        linewidth = 16
        print(f"pid = {process.pid} , executing:")
        print("=" * linewidth)
        for cmd in cmds:
            print(cmd)
        print("=" * linewidth)

        if block:
            # 等待子进程完成
            process.wait()

        # 返回进程的 PID
        return process
    except Exception as e:
        print(f"Error: {e}")
        return None


def run_python_script(script_path: str, script_args: str, block=True):
    """
    Executes a Python script in a new cmd window with an optional virtual environment activation.

    Args:
        script_path (str): Path to the Python script to execute.
        script_args (str): Arguments to pass to the Python script.
        block (bool): If True, the function will block until the script completes.
                      If False, the function will return immediately with the PID.

    Returns:
        int: The PID of the created process.
    """
    try:
        # 从环境变量中获取虚拟环境路径（如果有）
        venv_dir = os.environ.get('VIRTUAL_ENV', '')

        # 构造激活虚拟环境和运行脚本的命令
        if venv_dir:
            activate_cmd = f'{venv_dir}\\Scripts\\activate'
            python_cmd = f'python {script_path} {script_args}'
            cmds = [activate_cmd, python_cmd]
        else:
            # 如果没有虚拟环境，直接运行 Python 脚本
            cmds = [f'python {script_path} {script_args}']

        # 调用 execute_commands 执行命令
        process = execute_commands(cmds, block=block)

        return process
    except Exception as e:
        print(f"Error: {e}")
        return None


def kill_process(pid):
    """
    Kills a process and all its child processes using taskkill via os.system.

    Args:
        pid (int): The PID of the process to terminate.
    """
    try:
        # 构造 taskkill 命令
        command = f"taskkill /PID {pid} /F /T"

        # 使用 os.system 执行命令
        result = os.system(command)

        # 判断返回码
        if result == 0:
            print(f"Successfully killed PID {pid} and its child processes.")
        else:
            print(f"Failed to kill PID {pid}.")
    except Exception as e:
        print(f"An error occurred while killing the process: {e}")


# CMD_cd_root = f'cd {preset.}'

if __name__ == '__main__':
    pass
    proc = execute_commands(["timeout /t 10"], block=True)
    print(proc.pid)
