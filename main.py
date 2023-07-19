from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from processor import Processor
from sensor import ChatSimulation
import cv2

# simulation_time = 30
simulation_time = 60 * 60

client = RemoteAPIClient()
sim = client.getObject('sim')
robot = Processor(sim)

chat_str = None


def chat_callback(user_input):
    global chat_str
    chat_str = user_input


if __name__ == '__main__':
    defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
    sim.setInt32Param(sim.intparam_idle_fps, 0)

    client.setStepping(True)
    sim.startSimulation()

    interaction_thread = ChatSimulation(chat_callback)
    interaction_thread.start()

    while sim.getSimulationTime() < simulation_time:
        chat_str = robot.brain(chat_str)
        client.step()

    sim.stopSimulation()
    sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)
    cv2.destroyAllWindows()

    interaction_thread.stop()
    interaction_thread.join()
