from enum import Enum
import logging

from .runtime import Runtime
from .dds_binding import *

class DDS_LC(Enum):

    # Fatal error condition. Immediate abort on sink return.
    LC_FATAL = 1
    
    #  Error condition.
    LC_ERROR = 2
    
    # Warning condition.
    LC_WARNING = 4
    
    # Informational message.
    LC_INFO = 8
    
    # Debug/trace messages related to configuration settings.
    LC_CONFIG = 16
    
    # Debug/trace messages related to node discovery.
    LC_DISCOVERY = 32
    
    # Currently unused.
    LC_DATA = 64
    
    # Debug/trace messages for which no specialized category exists (yet).
    LC_TRACE = 128
    
    # Debug/trace messages related to receive administration.
    LC_RADMIN = 256
    
    # Debug/trace messages related to timing.
    LC_TIMING = 512
    
    # Debug/trace messages related to send administration.
    LC_TRAFFIC = 1024
    
    # Currently unused.
    LC_TOPIC = 2048
    
    # Debug/trace messages related to TCP communication.
    LC_TCP = 4096
    
    # Debug/trace messages related to parameter list processing.
    LC_PLIST = 8192
    
    # Debug/trace messages related to the writer history cache.
    LC_WHC = 16384
    
    # Debug/trace messages related to throttling.
    LC_THROTTLE = 32768
    
    # Reader history cache.
    LC_RHC = 65536
    # Include content in traces.
    LC_CONTENT = 131072
    
    LC_ALL = LC_FATAL | LC_ERROR | LC_WARNING | LC_INFO | LC_CONFIG | LC_DISCOVERY | LC_DATA | LC_TRACE | LC_TIMING | LC_TRAFFIC | LC_TCP | LC_THROTTLE |  LC_CONTENT

    LOG_MASK = LC_FATAL | LC_ERROR | LC_WARNING | LC_INFO
    
    TRACE_MASK = ~LOG_MASK 

class DDSLogger:
    class __SingletonLogger:
        def __init__(self, file_name=None, debug_flag=False):
            
            self.rt = Runtime.get_runtime()

            if file_name is None:
                self.log_file = 'cddspy.log'
            else:
                self.log_file = file_name

            self.debug_flag = debug_flag

            log_format = '[%(asctime)s] - [%(levelname)s] > %(message)s'
            log_level = logging.DEBUG

            self.logger = logging.getLogger(__name__ + '_cddspy.log')

            self.logger.setLevel(log_level)
            formatter = logging.Formatter(log_format)
            if not debug_flag:
                log_filename = self.log_file
                handler = logging.FileHandler(log_filename)
            else:
                handler = logging.StreamHandler(sys.stdout)

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        def info(self, caller, message):
            # self.logger.info(str('< %s > %s') % (caller, message))
            self.rt.ddslib.DDS_INFO(str('< %s > %s') % (caller, message))

        def warning(self, caller, message):
            self.logger.warning(str('< %s > %s') % (caller, message))

        def error(self, caller, message):
            self.logger.error(str('< %s > %s') % (caller, message))

        def debug(self, caller, message):
            self.logger.debug(str('< %s > %s') % (caller, message))
        
        def trace( self, caller, message):
            self.rt.ddslib.DDS_CTRACE(str('< %s > %s') % (caller, message))
            
        def get_log_mask (self):
            return self.rt.ddslib.dds_get_log_mask(self.handle)

    instance = None
    enabled = True

    def __init__(self, file_name=None, debug_flag=False):

        if not DDSLogger.instance:
            DDSLogger.instance = DDSLogger.__SingletonLogger(file_name, debug_flag)
        self._enabled= True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        
    @property
    def enabled (self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, is_enabled = True):
        self._enabled = bool(is_enabled)

    def info(self, caller, message):
        if self.enabled:
            self.instance.info(caller, message)

    def warning(self, caller, message):
        if self.enabled:
            self.instance.warning(caller, message)

    def error(self, caller, message):
        if self.enabled:
            self.instance.error(caller, message)

    def debug(self, caller, message):
        if self.enabled:
            self.instance.debug(caller, message)


logger = DDSLogger()
