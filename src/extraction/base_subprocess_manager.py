import abc
from src.utils.subprocess_communication import open_log_file, run_subprocess, close_log_file, run_command_on_subprocess


class SubprocessManager(metaclass=abc.ABCMeta):

    def __init__(self, process_base_path_str, process_start_cmd):
        self.process_log_file_path_str = process_base_path_str + "/log.txt"
        self.__process_log_file = open_log_file(self.process_log_file_path_str)
        self.__process_base_path_str = process_base_path_str
        self.__process_start_cmd = process_start_cmd
        self._start_process()

    def __del__(self):
        if self.__process is not None:
            self.__process.communicate()

        if self.__process_log_file is not None:
            close_log_file(self.__process_log_file)

    @abc.abstractmethod
    def _setup_config(self, server_config_data):
        pass

    def _start_process(self):
        self.__process = run_subprocess(cmd=self.__process_start_cmd, cmd_dir=self.__process_base_path_str,
                                        shell=False,
                                        log_file=self.__process_log_file)

    def _run_command_on_process(self, command):
        if self.__process is not None:
            run_command_on_subprocess(self.__process, command)

    def _communicate_with_process(self):
        self.__process.communicate()
