
import ctypes






cFunctions = ctypes.CDLL("./CSim.so")

test = cFunctions.testFunction
test.restype=ctypes.c_int
c = (ctypes.c_int*3) (1,3,4)
print(len(c))
print(test(c,len(c)))


libHandle = cFunctions._handle
del cFunctions
ctypes.windll.kernel32.FreeLibrary(libHandle)
