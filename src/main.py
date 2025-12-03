from simulation import Simulator
from gui.gui_manager import GUI



def startSimulation():

    

    simulator = Simulator()

    gui = GUI(simulator)

    

    gui.run()




if __name__ == "__main__":
    simulator = Simulator()

    gui = GUI(simulator)

    

    gui.run()