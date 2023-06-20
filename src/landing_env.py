import gymnasium as gym
import numpy as np
from PyFlyt import gym_envs
from wingman import cpuize, gpuize


class Environment:
    """
    Wrapper for the PyFlyt Rocket Landing environment
    """

    def __init__(self, cfg):
        super().__init__()

        self.env_name = "PyFlyt/Rocket-Landing-v0"

        # make the env
        self.env = gym.make(
            self.env_name, render_mode=("human" if cfg.display else None), ceiling=300.0
        )

        # compute spaces
        self.act_size = self.env.action_space.shape[0]
        self.obs_size = self.env.observation_space.shape[0]

        # constants
        self.device = cfg.device
        self.do_nothing = np.zeros((self.act_size))
        action_high = self.env.action_space.high
        action_low = self.env.action_space.low
        self._action_mid = (action_high + action_low) / 2.0
        self._action_scale = (action_high - action_low) / 2.0
        
        self.reward_options = tuple(map(float, cfg.reward_options.split(', ')))

        self.reset()

    def reset(self):
        self.state, _ = self.env.reset(options=self.reward_options)

        self.ended = False
        self.success = False
        self.cumulative_reward = 0.0
        self.cumulative_fitness = 0.0

        return self.state

    def step(self, action) -> tuple[np.ndarray, float, bool]:
        action = action.squeeze()
        assert (
            action.shape[0] == self.act_size
        ), f"Incorrect action sizes, expected {self.act_size}, got {action.shape[0]}"

        # denormalize the action
        action = action * self._action_scale + self._action_mid

        # step through the env
        self.state, reward, term, trunc, info = self.env.step(action)
        reward = float(reward)
        self.cumulative_reward += reward
        self.cumulative_fitness += info['fitness']
        self.success |= info["env_complete"]

        # if term or trunc or self.success:
        if term or trunc:
            self.ended = True

        return self.state, reward, term

    def evaluate(self, cfg, net=None):
        if net is not None:
            net.eval()

        # make the env
        self.env.close()
        self.env = gym.make(self.env_name, render_mode=None)
        self.reset()

        # store the list of eval performances here
        eval_scores = []

        while len(eval_scores) < cfg.eval_num_episodes:
            # get the action based on the state
            if net is not None:
                output = net.actor(gpuize(self.state, cfg.device).unsqueeze(0))
                action = net.actor.infer(*output)
                action = cpuize(action)[0]
            else:
                action = np.ones((self.act_size,)) * -1.0

            # get the next state and reward
            self.step(action)

            if self.ended:
                if cfg.eval_fitness:
                    eval_scores.append(self.cumulative_fitness)
                else:
                    eval_scores.append(self.cumulative_reward)
                    # eval_scores.append(float(self.success))
                self.reset()

        if cfg.eval_fitness:
            eval_score = np.sum(np.array(eval_scores))
        else:
            eval_score = np.mean(np.array(eval_scores))
        return eval_score

    def display(self, cfg, net=None):

        if net is not None:
            net.eval()

        # make the env
        self.env.close()
        self.env = gym.make(self.env_name, render_mode="human")
        self.reset()

        # gif parameters and variables
        gifs_save_path = "./rendered_gifs"
        total_gifs = 0
        frames = []

        while True:
            if net is not None:
                output = net.actor(gpuize(self.state, cfg.device).unsqueeze(0))
                # action = cpuize(net.actor.sample(*output)[0][0])
                action = cpuize(net.actor.infer(*output))
            else:
                action = np.ones((self.act_size,)) * -1.0

            self.step(action)

            # this captures the camera image for gif
            if cfg.render_gif:
                frames.append(self.env.render()[..., :3].astype(np.uint8))

            if self.ended:

                if cfg.render_gif:
                    from PIL import Image

                    print("-----------------------------------------")
                    print(f"Saving gif...")
                    print("-----------------------------------------")
                    frames = [Image.fromarray(frame) for frame in frames]
                    frames[0].save(
                        f"{gifs_save_path}/gif{total_gifs}.gif",
                        save_all=True,
                        append_images=frames[1:],
                        duration=1000 / 30,
                        loop=0,
                    )
                    frames = []
                    total_gifs += 1

                print("-----------------------------------------")
                print(f"Total Reward: {self.cumulative_reward}")
                print("-----------------------------------------")
                self.reset()
