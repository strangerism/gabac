"""GABAC library."""
import ctypes as ct
import numpy as np
import os
import sys

#libgabac_path = os.environ['LIBGABAC_PATH']
#libgabac = ct.cdll.LoadLibrary(libgabac_path)
import subprocess

process = subprocess.Popen("git rev-parse --show-toplevel".split(), stdout=subprocess.PIPE)
output, error = process.communicate()
root_path = output.strip().decode("utf-8")
libgabac = ct.cdll.LoadLibrary(os.path.join(
    root_path,
    'build/lib/libgabac.so'
))

r"""
c_bool 	    _Bool 	bool (1)
c_char 	    char 	1-character string
c_wchar 	    wchar_t 	1-character unicode string
c_byte 	    char 	int/long
c_ubyte 	    unsigned char 	int/long
c_short 	    short 	int/long
c_ushort 	    unsigned short 	int/long
c_int 	    int 	int/long
c_uint 	    unsigned int 	int/long
c_long 	    long 	int/long
c_ulong 	    unsigned long 	int/long
c_longlong 	    __int64 or long long 	int/long
c_ulonglong 	    unsigned __int64 or unsigned long long 	int/long
c_float 	    float 	float
c_double 	    double 	float
c_longdouble 	    long double 	float
c_char_p 	    char * (NUL terminated) 	string or None
c_wchar_p 	    wchar_t * (NUL terminated) 	unicode or None
c_void_p
[ct.c_void_p,
ct.c_size_t,
ct.c_uint,
ct.c_void_p,
ct.c_size_t,
ct.c_uint,
ct.c_void_p,
ct.c_void_p]
"""

### As Input
# unsigned char **const bitstream               bitstream = ct.pointer(ct.c_ubyte()
#                                               ct.pointer(bitstream))               
### As Output                        
# const uint64_t *const symbols                 symbols.ctypes.data_as(ct.POINTER(ct.c_uint64))
# int64_t *const symbols                        symbols.ctypes.data_as(ct.POINTER(ct.c_uint64))
# unsigned int *const binarizationParameters    binarization_parameters.ctypes.data_as(ct.POINTER(ct.c_uint))

class GABAC_RETURN:
    """Return Codes."""
    SUCCESS = 0
    FAILURE = 1

class GABAC_LOG_LEVEL:
    """
    Different logging urgency\n

    TRACE   : Log every step in great detail\n
    DEBUG   : Intermediate results\n
    INFO    : Expected Results\n
    WARNING : Suspicious events (may be an error)\n
    ERROR   : Handled errors\n
    FATAL   : Error causing application to terminate\n
    """
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

class GABAC_TRANSFORM:
    r"""
    gabac_transform_NONE        : Do nothing
    gabac_transform_EQUALITY    : Find equal values sequentially
    gabac_transform_MATCH       : Find larger sequence matches
    gabac_transform_RLE         : Find run lengths
    gabac_transform_LUT         : Remap symbols based on probability
    gabac_transform_DIFF        : Use differences between symbol values instead of symbols
    gabac_transform_CABAC       : coding based on cabac
    """
    NONE = 0
    EQUALITY = 1
    MATCH = 2
    RLE = 3
    LUT = 4
    DIFF = 5
    CABAC = 6

class GABAC_BINARIZATION:
    """
    BI = 0,  /**< @brief Binary */
    TU = 1,  /**< @brief Truncated Unary */
    EG = 2,  /**< @brief Exponential Golomb */
    SEG = 3,  /**< @brief Signed Exponential Golomb */
    TEG = 4,  /**< @brief Truncated Exponential Golomb */
    STEG = 5  /**< @brief Signed Truncated Exponential Golomb */
    """
    BI = 0
    TU = 1
    EG = 2
    SEG = 3
    TEG = 4
    STEG = 5

class GABAC_CONTEXT_SELCT:
    """
    BYPASS = 0,             /**< @brief Do not use arithmetic coding */
    ADAPTIVE_ORDER_0 = 1,   /**< @brief Current symbol only */
    ADAPTIVE_ORDER_1 = 2,   /**< @brief Use current + previous symbol */
    ADAPTIVE_ORDER_2 = 3    /**< @brief Use current + previous + before previous symbol */
    """
    BYPASS = 0
    ADAPTIVE_ORDER_0 = 1
    ADAPTIVE_ORDER_1 = 2
    ADAPTIVE_ORDER_2 = 3 

class GABAC_OPERATION:
    """enum gabac_operation"""
    ENCODE = 0
    DECODE = 1
    ANALYZE = 2

class GABAC_STREAM_MODE:
    """ enum gabac_stream_mode"""
    FILE = 0
    BUFFER = 1




###-------Data Block-------###

class gabac_data_block(ct.Structure):
    r"""
    uint8_t *values;    /**<  @brief Actual data */
    size_t values_size; /**<  @brief Number of elements (not bytes, except if word_size = 1!) */
    uint8_t word_size;  /**<  @brief Number of bytes per element */
    """
    _fields_ = [
        ("values", ct.c_void_p),
        ("values_size", ct.c_size_t),
        ("word_size", ct.c_uint8),
    ]

# Arguments
#   gabac_data_block *block,
#   const void *data,
#   size_t size,
#   uint8_t wordsize
# Return
#   int gabac_data_block_init()
libgabac.gabac_data_block_init.argtypes = [
    #ct.c_void_p,
    ct.POINTER(gabac_data_block),
    ct.c_void_p,
    ct.c_size_t,
    ct.c_uint8
]
libgabac.gabac_data_block_init.restype = ct.c_int

# Arguments
#   gabac_data_block *block
# Return
#   int gabac_data_block_release()
libgabac.gabac_data_block_release.argtypes = [
    ct.c_void_p
]
libgabac.gabac_data_block_init.restype = ct.c_int

# Arguments
#   gabac_data_block *block
#   size_t size
# Return
#   int gabac_data_block_resize()
libgabac.gabac_data_block_resize.argtypes = [
    ct.c_void_p,
    ct.c_size_t
]
libgabac.gabac_data_block_resize.restype = ct.c_int

# Arguments
#   gabac_data_block *stream1
#   gabac_data_block *stream2
# Return
#   int gabac_data_block_swap()
libgabac.gabac_data_block_swap.argtypes = [
    ct.c_void_p,
    ct.c_void_p
]
libgabac.gabac_data_block_swap.restype = ct.c_int

# Arguments
#   gabac_data_block *drain,
#   gabac_data_block *source
# Return
#   int gabac_data_block_copy()
libgabac.gabac_data_block_copy.argtypes = [
    ct.c_void_p,
    ct.c_void_p
]
libgabac.gabac_data_block_copy.restype = ct.c_int

# Arguments
#   const gabac_data_block *block,
#   size_t index
# Return
#   uint64_t gabac_data_block_get()
libgabac.gabac_data_block_get.argtypes = [
    ct.c_void_p,
    ct.c_size_t
]
libgabac.gabac_data_block_get.restype = ct.c_uint64

# Arguments
#   const gabac_data_block *block,
#   size_t index,
#   uint64_t val
# Return
#   void gabac_data_block_set()   
libgabac.gabac_data_block_set.argtypes = [
    ct.c_void_p,
    ct.c_size_t
]
libgabac.gabac_data_block_set.restype = None

class GabacDataBlock(object):

    def __init__(self,
        #block,
        size:int,
        word_size:int,
        data=None,
    ):
        # uint8_t wordSize;
        # std::vector<uint8_t> data;

        self.word_size = word_size

        self.data_block = gabac_data_block()

        return_code = libgabac.gabac_data_block_init(
            #self.data_block,
            self.data_block.ctypes.data_as(ct.POINTER(gabac_data_block)),
            data,
            #data.ctypes.data_as(ct.POINTER(ct.char),
            size,
            word_size,
        )

        if return_code == GABAC_RETURN.FAILURE:
            raise("Failed to initialize GabacDataCode")

    def release(self):
        return_code = libgabac.gabac_data_block_init(
            self.data_block,
        )

        if return_code == GABAC_RETURN.FAILURE:
            raise("Failed to release memory of GabacDataCode")

    def __getitem__(self, index):
        return libgabac.gabac_data_block_get(
            self.data_block,
            index
        )

    def __setitem__(self, index, value):
        libgabac.gabac_data_block_set(
            self.data_block,
            index,
            value
        )

class gabac_stream(ct.Structure):
    r"""
    void *data;
    gabac_stream_mode input_mode;
    """
    _fields_ = [
        ("data", ct.c_void_p),
        ("gabac_stream_mode", ct.c_uint)
    ]

# Arguments
#   gabac_stream *stream,
#   const char *filename,
#   size_t filename_size,
#   int write
# Return
#   int gabac_stream_create_file(
libgabac.gabac_stream_create_file.argtypes = [
    ct.c_void_p,
    ct.c_void_p,
    ct.c_size_t,
    ct.c_int
]
libgabac.gabac_stream_create_file.restype = ct.c_int

# Arguments
#   gabac_stream *stream,
#   gabac_data_block *block
# Return
#   int gabac_stream_create_buffer(
libgabac.gabac_stream_create_buffer.argtypes = [
    ct.c_void_p,
    ct.c_void_p,
]
libgabac.gabac_stream_create_buffer.restype = ct.c_int

# Arguments
#   gabac_stream *stream,
#   gabac_data_block *block
# Return
#   int gabac_stream_swap_block(
libgabac.gabac_stream_swap_block.argtypes = [
    gabac_stream,
    gabac_data_block
]
libgabac.gabac_stream_swap_block.restype = ct.c_int

# Arguments
#   gabac_stream *stream,
#   FILE **file
# Return
#   int gabac_stream_swap_file(
# TODO: Check datatype for file
libgabac.gabac_stream_swap_file.argtypes = [
    gabac_stream,
    ct.c_void_p
]
libgabac.gabac_stream_swap_file

# Arguments
#   gabac_stream *stream
# Return
#   int gabac_stream_release(
libgabac.gabac_stream_release.argtypes = [
    gabac_stream
]
libgabac.gabac_stream_release.restype = ct.c_int

class GabacStream(object):
    def __init__(self,
        write,
        filename="",
    ):
        
        self.stream = gabac_stream()
        
        libgabac.gabac_stream_create_file(
            self.stream,
            filename,
            len(filename),
        )

class gabac_io_config(ct.Structure):
    r"""
    gabac_stream input
    gabac_stream output
    gabac_stream log
    gabac_log_level log_level
    size_t blocksize
    """
    _fields_ = [
        ("input", gabac_stream),
        ("output", gabac_stream),
        ("log", gabac_stream),
        ("log_level", ct.c_uint),
        ("blocksize", ct.c_size_t),
    ]

# gabac_execute_transform
# -----------------------------------------------------------------------------

# Arguments
#   uint8_t transformationID,
#   const uint64_t *param,
#   int inverse,
#   gabac_data_block *input
# Return
#   int gabac_execute_transform(
libgabac.gabac_execute_transform.argtypes = (
    [ct.c_uint8,
    ct.c_void_p,
    ct.c_int,
    ct.c_void_p]
)

libgabac.gabac_execute_transform.restype = ct.c_int

def gabac_execute_transform(
    transformation_id,
    params,
    inverse,
    input_gabac_data_block,
):
    # uint8_t transformationID,
    # const uint64_t *param,
    # int inverse,
    # gabac_data_block *input
    return_code = libgabac.gabac_execute_transform(
        transformation_id,
        params.ctypes.data_as(ct.POINTER(ct.c_uint64)),
        inverse,
        input_gabac_data_block.ctypes.data_as(ct.POINTER(gabac_data_block))
    )

    if return_code == GABAC_RETURN.FAILURE:
        sys.exit("error: gabac_encode() failed")

    return input_gabac_data_block

# gabac_run
# -----------------------------------------------------------------------------

# gabac_operation operation     enum
# gabac_io_config *io_config,
# const char *config_json,
# size_t json_length
libgabac.gabac_run.argtypes = (
    [ct.c_uint,
    ct.c_void_p,
    ct.c_void_p,
    ct.c_size_t]
)

libgabac.gabac_run.restype = ct.c_int

def gabac_run(
    operation,
    io_config,
    config_json
):

    io_config = ct.pointer(gabac_io_config)

    return_code = libgabac.gabac_run(
        operation,
        io_config.ctypes.data_as(ct.POINTER(gabac_io_config)),
        config_json.ctypes.data_as(ct.POINTER(ct.c_char)),
        len(config_json)
    )

    if return_code == GABAC_RETURN.FAILURE:
        sys.exit("error: gabac_run() failed")

