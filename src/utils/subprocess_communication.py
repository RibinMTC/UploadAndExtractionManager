import subprocess
from subprocess import PIPE
import time
from datetime import datetime
import shlex


def open_log_file(log_file_path, file_mode='w'):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log_file = open(log_file_path, file_mode)
    log_file.truncate(0)
    log_file.write('\n************************************** ' + dt_string + ' ***********************************\n')
    log_file.flush()
    return log_file


def close_log_file(log_file):
    if log_file is not None:
        log_file.close()


def write_bytes_to_log_file(log_file_path, bytes_to_write, truncate=True):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(log_file_path, 'wb') as log_file:
        if truncate:
            log_file.truncate(0)
        log_file.write(
            ('\n************************************** ' + dt_string + ' ***********************************\n').encode(
                'utf-8'))
        log_file.write(bytes_to_write)
        log_file.flush()


def run_subprocess(cmd, cmd_dir=None, shell=False, log_file=None):

    if not shell:
        cmd = shlex.split(cmd)

    if log_file is None:
        output_capture = PIPE
    else:
        output_capture = log_file

    process_id = subprocess.Popen(cmd, shell=shell, cwd=cmd_dir, stdin=PIPE, stdout=output_capture,
                                  stderr=output_capture)
    return process_id


def run_command_on_subprocess(process_id, cmd):
    process_id.stdin.write((cmd + "\n").encode('utf-8'))
    process_id.stdin.flush()


def communicate_and_log_process_output(process_id, log_file_path_str):
    out, err = process_id.communicate()

    write_bytes_to_log_file(log_file_path_str, out)


def terminate_subprocess(process_id):
    process_id.terminate()


def kill_subprocess(process_id, kill_cmd=None):
    time.sleep(1)
    process_id.stdin.close()
    process_id.terminate()
    process_id.wait(timeout=0.2)
