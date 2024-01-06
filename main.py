class fiber1(fiber) :
    def generator(self): 
        print(f'starting {self.fiber_name}') 
        token = (yield 3) 
        self.sim.WAKE_FIBER("f2",data=10)
        token = (yield 0) 
        print(f'{self.fiber_name} was called with {token}')
        token = (yield 2) 
        self.sim.WAKE_FIBER("f2",data=11)
        token = (yield 0) 
        print(f'{self.fiber_name} was called with {token}')
        token = (yield 1) 
        for _ in range(1,10):
            token = (yield 3) 
        token = (yield "EXIT") 



def fiber2(fiber_name="_no_name_",sim=None): 
    print(f'starting {fiber_name}') 
    token = (yield 0) 
    print(f'{fiber_name} was called with {token}')
    token = (yield 7) 
    sim.WAKE_FIBER("f1",data=20)
    token = (yield 0) 
    print(f'{fiber_name} was called with {token}')
    token = (yield 5) 
    sim.WAKE_FIBER("f1",data=21)
    token = (yield "EXIT") 

from fiber_sim import *

def main():
    sim = simulation(90)
    sim.REGISTER("f1",fiber1("f1",sim)) 
    sim.REGISTER("f2",fiber2("f2",sim)) 
    sim.run_sim()

if __name__ == "__main__":
    main()