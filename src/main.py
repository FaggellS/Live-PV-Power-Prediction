from simulation import Simulator
from gui.gui_manager import GUI



def startSimulation():

    

    simulator = Simulator()

    gui = GUI(simulator)

    

    gui.run()