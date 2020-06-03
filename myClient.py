import threading
import ctypes
import time
import socket



class thread_with_exception(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = ('192.168.1.11', 10000)
        self.message =" "

    def run(self):
        while True:
          time.sleep(4)
          if self.message != " ":
              try:
                  self.sock.connect(self.serverAddress)
                  try:
                      tosend = self.message.encode()
                      print("sending {}".format(self.message))
                      self.sock.sendall(tosend)
                  finally:
                      print("Closing Socket")
                      self.sock.close()
                      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                      self.message = " "
              except:
                  print("No connections to make")
              finally:
                  print("Has ended")
          else:
            print("No message to send")

    def get_id(self):
        if hasattr(self,'_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def raise_exception(self):
        thread_id = self.get_id()
        self.sock.close()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,0)
            print("Exception was raised")
    def sendMessage(self,message):
      self.message += message + "\n"




