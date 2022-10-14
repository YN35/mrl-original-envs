from minerl.env.malmo import InstanceManager
from env import NativeSurvivalv0
import gym
import minerl  # noqa
import time




if __name__ == '__main__':

    # logs
    import coloredlogs
    import logging

    coloredlogs.install(level=logging.DEBUG)

    # clear logs
    import subprocess

    logging.debug("Deleting previous java log files...")
    subprocess.check_call("rm -rf logs/*", shell=True)

    # make env
    env_spec = NativeSurvivalv0(agent_count=2)

    # IF you want to use existing instances use this!
    # instances = [
    #     InstanceManager.add_existing_instance(9001),
    #     InstanceManager.add_existing_instance(9002)]
    instances = []

    env = env_spec.make(instances=instances)

    # iterate desired episodes
    for r in range(2):
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
            
            env.set_next_chat_message("/tp @a 100 200 100")
            # print(str(steps) + " actions: " + str(actions))

            obs, reward, done, info = env.step(actions)

            # log("reward: " + str(reward))
            # log("done: " + str(done))
            # log("info: " + str(info))
            # log(" obs: " + str(obs))

        logging.debug(f"Episode {r + 1}/{args.episodes} done: {steps} steps")
