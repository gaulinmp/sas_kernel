# -*- coding: utf-8 -*-
import time

from ipykernel.kernelbase import Kernel
from pexpect import spawn, EOF, TIMEOUT

__version__ = '0.0.2'


class SASKernel(Kernel):
    implementation = 'sas_kernel'
    implementation_version = __version__

    @property
    def language_version(self):
        return "9.4";

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = "Welcome to Jupyter SAS Kernel!"
        return self._banner

    language_info = {'name': 'sas',
                     'codemirror_mode': 'SQL',
                     'mimetype': 'text/plain',
                     'file_extension': '.sas'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_sas()

    def _start_sas(self):
        try:
            self.saswrapper = spawn('sas', ['-nodms', '-terminal',])
            self.saswrapper.send("OPTIONS NONUMBER NODATE PAGESIZE=MAX;")
            self.saswrapper.send("TITLE;")
            discard = self._smart_read(30)
        finally:
            pass

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            numsent = self._smart_send(code)
            output = self._smart_read(10)
        except KeyboardInterrupt:
            #self._smart_send("ENDSAS;")
            self.saswrapper.sendintr()
            interrupted = True
            self.saswrapper.expect([EOF])
            output = self.saswrapper.before
        except EOF:
            output = 'SAS HAS ALREADY QUIT. Try restarting kernel.'
            interrupted = True

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)


        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}


    def _smart_send(self, sendable):
        try:
            length = len(sendable)
            if length <= 0:
                return 0
        except AttributeError:
            return 0
        nsent = sum([self.saswrapper.send(sendable[i*200:(i+1)*200])
                     for i in range(int(length / 200)+1)])
        if sendable[-1] not in ('\r', '\n', b'\r', b'\n', ):
            self.saswrapper.send('\n')
            nsent += 1
        return nsent

    def _smart_read(self, timeout):
        """Read return response. Timeout in seconds."""
        # maximum time allowed to read the first response
        first_char_timeout = timeout * 0.5

        # maximum time allowed between subsequent characters
        inter_char_timeout = timeout * 0.1

        # maximum time for reading the entire prompt
        total_timeout = timeout * 3.0

        prompt = b''
        begin = time.time()
        expired = 0.0
        t_o = first_char_timeout

        while expired < total_timeout:
            try:
                prompt += self.saswrapper.read_nonblocking(size=1, timeout=t_o)
                expired = time.time() - begin # updated total time expired
                t_o = inter_char_timeout
            except TIMEOUT:
                break

        return prompt.decode('utf-8', errors='ignore')


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SASKernel)
