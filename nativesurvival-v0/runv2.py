from minerl.env.malmo import InstanceManager
from env import NativeSurvivalv0
import gym
import minerl  # noqa
import argparse
import time
import os




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--single', action="store_true", help='use the single agent default xml')
    parser.add_argument('--port', type=int, default=None, help='the port of existing client or None to launch')
    parser.add_argument('--episodes', type=int, default=2, help='the number of resets to perform - default is 1')
    args = parser.parse_args()

    # logs
    import coloredlogs
    import logging

    coloredlogs.install(level=logging.DEBUG)

    # clear logs
    import subprocess

    logging.debug("Deleting previous java log files...")
    subprocess.check_call("rm -rf logs/*", shell=True)
    
    agent_num = 4

    env_spec = NativeSurvivalv0(agent_count=agent_num)
        
    #make instance
    insta = []
    # ports = []
    # for i in range(agent_num):
    #     inst, port = InstanceManager.get_instance(os.getpid(), instance_id=i)
    #     inst.create_multiagent_instance_socket(socktime=60.0 * 4)
    #     insta.append(inst)
    #     ports.append(port)

    # IF you want to use existing instances use this!
    instances = [
        InstanceManager.add_existing_instance(10000),
        InstanceManager.add_existing_instance(10001),
        InstanceManager.add_existing_instance(10002)]
    # instances = list(range(4))

    env = env_spec.make(instances=instances)

    # iterate desired episodes
    for r in range(args.episodes):
        logging.debug(f"Reset for episode {r + 1}")
        env.reset()
        
        # actions = {}
        # env.set_next_chat_message("/tp @a 0 300 0")
        # env.step(actions)
        
        steps = 0

        done = False
        actor_names = env.task.agent_names
        while not done:
            steps += 1
            env.render()

            actions = env.action_space.no_op()
            for agent in actions:
                actions[agent]["forward"] = 1
                actions[agent]["attack"] = 1
                actions[agent]["camera"] = [0, 0.1]
                # if agent == 0:
                #     actions[agent]["chat"] = "/summon creeper"
            
            # env.set_next_chat_message("/tp @a 100 200 100")
            # print(str(steps) + " actions: " + str(actions))

            obs, reward, done, info = env.step(actions)

            # log("reward: " + str(reward))
            # log("done: " + str(done))
            # log("info: " + str(info))
            # log(" obs: " + str(obs))

        logging.debug(f"Episode {r + 1}/{args.episodes} done: {steps} steps")
