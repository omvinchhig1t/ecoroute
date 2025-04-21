import pandas as pd
import numpy as np
from scipy.spatial import distance

class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = np.zeros((n_states, n_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state, valid_actions):
        if np.random.rand() < self.epsilon:
            return np.random.choice(valid_actions)
        else:
            return np.argmax(self.q_table[state, valid_actions])

    def update(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state, best_next_action]
        self.q_table[state, action] += self.alpha * (td_target - self.q_table[state, action])



class EcoFriendlyRouteEnv:
    def __init__(self, waypoints, time_factor=1.0):
        self.waypoints = waypoints
        self.start = 0
        self.end = len(waypoints) - 1
        self.current_state = self.start
        self.time_factor = time_factor  # More time allows better optimization

    def reset(self):
        self.current_state = self.start
        return self.current_state

    def step(self, action):
        next_state = action
        base_reward = self.waypoints.iloc[next_state]['Eco_Friendly_Score']
        random_variation = np.random.uniform(-0.5, 0.5)
        time_penalty = self.time_factor / (next_state + 1)
        reward = base_reward - time_penalty + random_variation
        done = (next_state == self.end)
        self.current_state = next_state
        return next_state, reward, done

    def available_actions(self):
        return list(range(len(self.waypoints)))

def train(env, agent, episodes=500):
    for _ in range(episodes):
        state = env.reset()
        done = False
        while not done:
            actions = env.available_actions()
            action = agent.choose_action(state, actions)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state

def nearest_neighbor_route(waypoints):
    unvisited = set(range(len(waypoints)))
    route = [0]
    unvisited.remove(0)

    while unvisited:
        last = route[-1]
        nearest = min(unvisited, key=lambda x: distance.euclidean(
            (waypoints.iloc[last]['Latitude'], waypoints.iloc[last]['Longitude']),
            (waypoints.iloc[x]['Latitude'], waypoints.iloc[x]['Longitude'])
        ))
        route.append(nearest)
        unvisited.remove(nearest)

    return [waypoints.iloc[i][['Latitude', 'Longitude']].tolist() for i in route]

def load_waypoints(Eco_Friendly_Routes):
    return pd.read_excel("Eco_Friendly_Routes.xlsx")
