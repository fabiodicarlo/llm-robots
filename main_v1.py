from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from robot.ia_robot import IaRobot
import user_interaction

# simulation_time = 30
simulation_time = 60 * 60
chat_str = None

client = RemoteAPIClient()
sim = client.getObject('sim')
ia_robot = IaRobot(sim)

defaultIdleFps = sim.getInt32Param(sim.intparam_idle_fps)
sim.setInt32Param(sim.intparam_idle_fps, 0)


def chat_callback(user_input):
    global chat_str
    chat_str = user_input


if __name__ == '__main__':
    interaction_thread = user_interaction.UserInteractionThread(chat_callback)
    interaction_thread.start()

    client.setStepping(True)
    sim.startSimulation()

    while sim.getSimulationTime() < simulation_time:
        chat_str = ia_robot.brain(chat_str)
        client.step()

    sim.stopSimulation()
    sim.setInt32Param(sim.intparam_idle_fps, defaultIdleFps)
    # cv2.destroyAllWindows()

    interaction_thread.stop()
    interaction_thread.join()
