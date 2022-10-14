from minerl.herobraine.hero.handlers.agent.quit import AgentQuitFromPossessingItem
from minerl.herobraine.hero.handlers.agent.actions.equip import EquipAction
from minerl.herobraine.hero.mc import MS_PER_STEP, STEPS_PER_MS
from minerl.herobraine.env_specs.simple_embodiment import SimpleEmbodimentEnvSpec
from minerl.herobraine.hero.handler import Handler
from minerl.herobraine.hero import handlers
from typing import Dict, List, Optional, Union
from gym import spaces

# from chat import ChatAction


ENV_DOC = """
native survival envirinment
"""

ENV_LENGTH = 80000000

none = 'none'
other = 'other'

class NativeSurvivalv0(SimpleEmbodimentEnvSpec):
    def __init__(self,
                 *args,
                 max_episode_steps=60000,
                 **kwargs):
        # 6000 for obtain iron  (5 mins)
        # 18000 for obtain diamond (15 mins)
        # self.dense = dense
        # if self.dense:
        #     self.reward_text = "every time it obtains an item"
        # else:
        #     self.reward_text = "only once per item the first time it obtains that item"
        # self.reward_schedule = reward_schedule

        super().__init__(*args,
                         name='NativeSurvival-v0',
                         max_episode_steps=max_episode_steps,
                         **kwargs
                         )

    def create_observables(self) -> List[Handler]:
        # TODO: Parameterize these observations.
        return super().create_observables() + [
            handlers.FlatInventoryObservation([
                'dirt',
                'coal',
                'torch',
                'log',
                'planks',
                'stick',
                'crafting_table',
                'wooden_axe',
                'wooden_pickaxe',
                'stone',
                'cobblestone',
                'furnace',
                'stone_axe',
                'stone_pickaxe',
                'iron_ore',
                'iron_ingot',
                'iron_axe',
                'iron_pickaxe'
            ]),
            handlers.EquippedItemObservation(items=[
                'air', 'wooden_axe', 'wooden_pickaxe', 'stone_axe', 'stone_pickaxe', 'iron_axe', 'iron_pickaxe', none,
                # TODO (R): REMOVE NONE FOR MINERL-v1
                other
            ], _default='air', _other=other),
        ]

    def create_actionables(self):
        # TODO (R): MineRL-v1 use invalid (for data)
        return super().create_actionables() + [
            handlers.ChatAction(),
            handlers.PlaceBlock([none, 'dirt', 'stone', 'cobblestone', 'crafting_table', 'furnace', 'torch'],
                                _other=none, _default=none),
            handlers.EquipAction([none, 'air', 'wooden_axe', 'wooden_pickaxe', 'stone_axe', 'stone_pickaxe', 'iron_axe',
                                  'iron_pickaxe'], _other=none, _default=none),
            handlers.CraftAction([none, 'torch', 'stick', 'planks', 'crafting_table'], _other=none, _default=none),
            handlers.CraftNearbyAction(
                [none, 'wooden_axe', 'wooden_pickaxe', 'stone_axe', 'stone_pickaxe', 'iron_axe', 'iron_pickaxe',
                 'furnace'], _other=none, _default=none),
            handlers.SmeltItemNearby([none, 'iron_ingot', 'coal'], _other=none, _default=none),
            # As apart of pervious todo
            # this should be handlers.SmeltItem([none, 'iron_ingot', 'coal', other]), but this is not supported by mineRL-v0

        ]

    def create_rewardables(self) -> List[Handler]:
        return [
            handlers.RewardForCollectingItems([
                dict(type="log", amount=1, reward=1.0),
            ])
        ]

    def create_agent_start(self) -> List[Handler]:
        return []

    def create_agent_handlers(self) -> List[Handler]:
        return []

    def create_server_world_generators(self) -> List[Handler]:
        return [handlers.DefaultWorldGenerator(force_reset=False)]

    def create_server_quit_producers(self) -> List[Handler]:
        return []

    def create_server_decorators(self) -> List[Handler]:
        return []

    def create_server_initial_conditions(self) -> List[Handler]:
        return [
            handlers.TimeInitialCondition(
                start_time=6000,
                allow_passage_of_time=True,
            ),
            handlers.SpawningInitialCondition(
                allow_spawning=True
            )
        ]

    def is_from_folder(self, folder: str):
        return folder == 'nativesurvival'

    def get_docstring(self):
        return ""
    
    def determine_success_from_rewards(self):
        return []

    # def determine_success_from_rewards(self, rewards: list) -> bool:
    #     # TODO: Convert this to finish handlers.
    #     rewards = set(rewards)
    #     allow_missing_ratio = 0.1
    #     max_missing = round(len(self.reward_schedule) * allow_missing_ratio)

    #     # Get a list of the rewards from the reward_schedule.
    #     reward_values = [
    #         s['reward'] for s in self.reward_schedule
    #     ]

    #     return len(rewards.intersection(reward_values)) \
    #            >= len(reward_values) - max_missing