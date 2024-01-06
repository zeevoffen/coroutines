import queue
#from queue import PriorityQueue
from dataclasses import dataclass, field
import logging

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class EventEntry() :
    def __init__(self,prio,fiber):
      self.prio = prio
      self.fiber = fiber

    def __lt__(self, other):
      return self.prio < other.prio



class fiber :
    def __init__(self,fiber_name="_no_name_",_simulation=None)  :
       self.fiber_name=fiber_name
       self.sim=_simulation
       self.generator_iterator = self.generator()

    def __next__(self):
        return next(self.generator_iterator)

    def send(self,*argv):
        return self.generator_iterator.send(argv)
    
    def close(self,*argv):
        return self.generator_iterator.close()

    def generator(self): 
        pass

#class fiber1(fiber) :
#    def generator(self): 
#        print(f'starting {self.fiber_name}') 
#        token = (yield 3) 
#        self.sim.WAKE_FIBER("f2",data=10)
#        token = (yield 0) 
#        print(f'{self.fiber_name} was called with {token}')
#        token = (yield 2) 
#        self.sim.WAKE_FIBER("f2",data=11)
#        token = (yield 0) 
#        print(f'{self.fiber_name} was called with {token}')
#        token = (yield 1) 
#        for _ in range(1,10):
#            token = (yield 3) 
#        token = (yield "EXIT") 
#
#
#
#def fiber2(fiber_name="_no_name_",sim=None): 
#    print(f'starting {fiber_name}') 
#    token = (yield 0) 
#    print(f'{fiber_name} was called with {token}')
#    token = (yield 7) 
#    sim.WAKE_FIBER("f1",data=20)
#    token = (yield 0) 
#    print(f'{fiber_name} was called with {token}')
#    token = (yield 5) 
#    sim.WAKE_FIBER("f1",data=21)
#    token = (yield "EXIT") 


class simulation :
    def __init__(self,duration) -> None:
        self._duration=duration
        self.current_time = 0
        self.all_fibers={}
        self.fiber_to_name={}
        self.pq = queue.PriorityQueue() 
        self.aq = queue.Queue()

    def WAKE_FIBER(self,fiber_name,**kwargs):
        print(f'wake -> {fiber_name} {kwargs}')
        self.aq.put({"fiber":self.all_fibers[fiber_name],"args":kwargs})

    def WAIT(self,time,fiber) :
        print(f'waiting for {fiber} until {self.current_time+time}') 
        self.pq.put((self.current_time+time,EventEntry(self.current_time+time,fiber)))

    def STOP_FIBER(self,fiber) :
        print(f'stoping {self.fiber_to_name[fiber]} ')
        fiber.close()

    def REGISTER(self,name,fiber):
        print(f'registering {fiber}')
        self.all_fibers[name]=fiber
        self.fiber_to_name[fiber]=name
        self.pq.put((0,EventEntry(0,fiber)))

    def stop_sim(self):
        print (f'{bcolors.WARNING}DONE{bcolors.ENDC}')

    def run_sim(self):
        while not self.pq.empty():
            prq = self.pq.get()
            self.current_time = prq[0]
            if (self.current_time >= self._duration):
                self.stop_sim()
                return
            fiber = prq[1].fiber
            nxt_time = fiber.__next__()
            if (type(nxt_time) is str):
                if nxt_time=="EXIT":
                    self.STOP_FIBER(fiber)
            else:    
                print (f'time is {bcolors.OKBLUE}{self.current_time}{bcolors.ENDC}: running {self.fiber_to_name[fiber]} next time:{self.current_time+nxt_time}')
                if nxt_time>0 :
                   self.WAIT(nxt_time,fiber)
            while not self.aq.empty():
               af=self.aq.get()
               fib = af["fiber"]
               arg = af["args"]
               nt = fib.send(arg)
               self.WAIT(nt,fib)

        self.stop_sim()

#def main():
#    sim = simulation(90)
#    sim.REGISTER("f1",fiber1("f1",sim)) 
#    sim.REGISTER("f2",fiber2("f2",sim)) 
#    sim.run_sim()
#
#if __name__ == "__main__":
#    main()