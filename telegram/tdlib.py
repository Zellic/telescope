from ctypes.util import find_library
from ctypes import *
import json
import os
import sys
import platform

_log_message_callback_type = CFUNCTYPE(None, c_int, c_char_p)
LOG_ALL = True

class TDLib:
    _instance = None
    _tdjson_path = None
    _tdjson = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TDLib, cls).__new__(cls)
            cls._instance._load_tdjson()
            cls._instance._initialize_tdjson()
            cls._instance._set_log_message_callback()
        return cls._instance

    def _load_tdjson(self):
        if self._tdjson_path is None:
            self._tdjson_path = find_library('tdjson')
            if self._tdjson_path is None:
                osplatform = platform.system().lower()
                if osplatform == 'windows':
                    self._tdjson_path = os.path.join(os.path.dirname(__file__), "..", "natives", osplatform, "tdjson.dll")
                elif osplatform == 'linux':
                    self._tdjson_path = os.path.join(os.path.dirname(__file__), "..", "natives", osplatform, "lib", "libtdjson.so")
                else:
                    sys.exit("Can't find 'tdjson' library")
            self._tdjson = CDLL(self._tdjson_path)

    def _initialize_tdjson(self):
        self._td_create_client_id = self._tdjson.td_create_client_id
        self._td_create_client_id.restype = c_int
        self._td_create_client_id.argtypes = []

        self._td_receive = self._tdjson.td_receive
        self._td_receive.restype = c_char_p
        self._td_receive.argtypes = [c_double]

        self._td_send = self._tdjson.td_send
        self._td_send.restype = None
        self._td_send.argtypes = [c_int, c_char_p]

        self._td_execute = self._tdjson.td_execute
        self._td_execute.restype = c_char_p
        self._td_execute.argtypes = [c_char_p]

        self._td_set_log_message_callback = self._tdjson.td_set_log_message_callback
        self._td_set_log_message_callback.restype = None
        self._td_set_log_message_callback.argtypes = [c_int, _log_message_callback_type]

    # noinspection PyArgumentList
    @_log_message_callback_type
    @staticmethod
    def _on_log_message_callback(verbosity_level, message):
        if verbosity_level == 0:
            sys.exit('TDLib fatal error: %r' % message)

    def _set_log_message_callback(self):
        self._td_set_log_message_callback(2, self._on_log_message_callback)

    def td_execute(self, query):
        query = json.dumps(query).encode('utf-8')
        result = self._td_execute(query)
        if result:
            result = json.loads(result.decode('utf-8'))
        return result

    def create_client_id(self):
        return self._td_create_client_id()

    def send(self, client_id, query):
        if(LOG_ALL):
            print("=> " + repr(query))

        query = json.dumps(query).encode('utf-8')
        self._td_send(client_id, query)

    def receive(self):
        result = self._td_receive(1.0)
        if result:
            result = json.loads(result.decode('utf-8'))

            if(LOG_ALL):
                print("<= " + repr(result))
        return result
