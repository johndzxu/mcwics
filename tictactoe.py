from pprint import pprint
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)  # 0: empty, 1: 'X', -1: 'O'
        self.current_player = 1  # Player 1 starts

    def available_actions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def make_move(self, action):
        if self.board[action] == 0:
            self.board[action] = self.current_player
            self.current_player *= -1  # Switch player
            return True
        return False

    def make_random_move(self):
        available_actions = self.available_actions()
        random_action = available_actions[np.random.randint(len(available_actions))]
        self.make_move(random_action)

    def check_winner(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3:
                return self.board[i, 0]
            elif abs(sum(self.board[:, i])) == 3:
                return self.board[0, i]
        if abs(sum([self.board[i, i] for i in range(3)])) == 3 or abs(sum([self.board[i, 2 - i] for i in range(3)])) == 3:
            return self.board[1, 1]
        if not any(0 in row for row in self.board):
            return 0  # Draw
        return None  # Game continues

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1

class QLearningAgent:
    def __init__(self, learning_rate=0.2, discount_factor=1, epsilon=1, epsilon_decay=0.99):
        self.q_table = {}  # Initialize Q-table
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def get_q_value(self, state, action):
        return self.q_table.get((tuple(map(tuple, state)), action), 0)

    def choose_action(self, state, available_actions):
        if np.random.rand() < self.epsilon:
            return available_actions[np.random.choice(len(available_actions))]
        q_values = [self.get_q_value(state, action) for action in available_actions]
        max_q = max(q_values)

        actions_with_max_q = [action for action, q in zip(available_actions, q_values) if q == max_q]
        return actions_with_max_q[np.random.choice(len(actions_with_max_q))]

    def update_q_table(self, old_state, action, reward, new_state):
        old_q = self.get_q_value(old_state, action)
        max_future_q = max([self.get_q_value(new_state, a) for a in TicTacToe().available_actions()], default=0)
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * max_future_q - old_q)
        self.q_table[(tuple(map(tuple, old_state)), action)] = new_q

    def update_epsilon(self):
        if self.epsilon * self.epsilon_decay > 0.25:
            self.epsilon *= self.epsilon_decay

    def export_qtable(self):
        with open('qtable', 'w') as file:
            pprint(self.q_table, stream=file)

    def import_qtable(self, qtable_file):
        with open(qtable_file, 'r') as file:
            self.q_table = eval(file.read())

def train_agent_o(agent, episodes=10000):
    for episode in range(episodes):
        game = TicTacToe()
        
        while True:
            old_state = np.copy(game.board)
            action = agent.choose_action(old_state, game.available_actions())
            game.make_move(action)

            winner = game.check_winner()
            if winner is not None:
                # Game ended, update Q-table
                reward = -1
                if winner == 1:
                    reward = 1
                agent.q_table[(tuple(map(tuple, old_state)), action)] = reward
                break
            else:
                game.make_random_move()
                winner = game.check_winner()
                reward = 0
                if winner == -1:
                    reward = -1
                new_state = np.copy(game.board)
                agent.update_q_table(old_state, action, reward, new_state)

        agent.update_epsilon()  # Decay epsilon after each episode

    return agent

def train_agent_x(agent, episodes=10000):
    for episode in range(episodes):
        game = TicTacToe()
        
        game.make_random_move()
        while True:
            old_state = np.copy(game.board)
            action = agent.choose_action(old_state, game.available_actions())
            game.make_move(action)

            winner = game.check_winner()

            if winner is not None:
                if winner == -1:
                    reward = 1
                elif winner == 0:
                    reward = 0.5
                else:
                    reward = -1
                agent.q_table[(tuple(map(tuple, old_state)), action)] = reward
                break
            else:
                game.make_random_move()
                winner = game.check_winner()
                if winner == 1:
                    reward = -1
                elif winner == 0:
                    reward = 0.5
                else:
                    reward = 0
                new_state = np.copy(game.board)
                agent.update_q_table(old_state, action, reward, new_state)
                if winner is not None:
                    break
        agent.update_epsilon()  # Decay epsilon after each episode

    return agent

def test_agent_o(agent, test_episodes=1000):
    agent.epsilon = 0
    win_count = 0
    draw_count = 0

    for _ in range(test_episodes):
        game = TicTacToe()
        
        while True:
            if game.current_player == 1:
                action = agent.choose_action(state, game.available_actions())
                game.make_move(action)
            else:
                game.make_random_move()

            winner = game.check_winner()
            if winner is not None:
                if winner == 1:
                    win_count += 1
                elif winner == 0:  # Draw
                    draw_count += 1
                break

    win_rate = win_count / test_episodes
    draw_rate = draw_count / test_episodes
    loss_rate = 1 - (win_rate + draw_rate)
    return win_rate, draw_rate, loss_rate

def test_agent_x(agent, test_episodes=1000):
    agent.epsilon = 0
    win_count = 0
    draw_count = 0

    for _ in range(test_episodes):
        game = TicTacToe()
        
        while True:
            if game.current_player == 1:
                game.make_random_move()
            else:
                action = agent.choose_action(game.board, game.available_actions())
                game.make_move(action)

            winner = game.check_winner()
            if winner is not None:
                if winner == -1:
                    win_count += 1
                elif winner == 0:
                    draw_count += 1
                break

    win_rate = win_count / test_episodes
    draw_rate = draw_count / test_episodes
    loss_rate = 1 - (win_rate + draw_rate)
    return win_rate, draw_rate, loss_rate

def test_agents(agent_o, agent_x, test_episodes=1000):
    agent_o.epsilon = 0
    agent_x.epsilon = 0
    win_count = 0
    draw_count = 0

    for _ in range(test_episodes):
        game = TicTacToe()
        
        while True:
            if game.current_player == 1:
                action = agent_o.choose_action(game.board, game.available_actions())
                game.make_move(action)
            else:
                action = agent_x.choose_action(game.board, game.available_actions())
                game.make_move(action)

            winner = game.check_winner()
            if winner is not None:
                if winner == 1:
                    win_count += 1
                elif winner == 0:  # Draw
                    draw_count += 1
                break

    win_rate = win_count / test_episodes
    draw_rate = draw_count / test_episodes
    loss_rate = 1 - (win_rate + draw_rate)
    return win_rate, draw_rate, loss_rate


def get_user_move():
    user_input = input("Enter the row and column indices separated by a comma (e.g., 1,2): ")
    row_index, col_index = map(int, user_input.strip().split(','))
    return row_index, col_index

def make_user_move(game):
    user_move = get_user_move()
    while user_move not in game.available_actions():
        user_move = get_user_move()

    game.make_move(user_move)


def play(agent, agent_type):
    agent.epsilon = 0
    game = TicTacToe()
    while True:
        if agent_type == -1:
            print(game.board)
            make_user_move(game)
        while game.check_winner() == None:
            if game.current_player == agent_type*-1:
                print(game.board)
                make_user_move(game)
            else:
                state = np.copy(game.board)
                action = agent.choose_action(state, game.available_actions())
                game.make_move(action)

        if game.check_winner() == agent_type*-1:
            print("You won!!!")
        elif game.check_winner() == agent_type:
            print("You lost!!!")
        elif game.check_winner() == 0:
            print("Tie!!!")

        game.reset()

        
if __name__ == '__main__':
    agent_o = QLearningAgent()
    agent_x = QLearningAgent()
    agent_o.import_qtable('qtable_o')
    agent_x.import_qtable('qtable_x')

    #train_agent_o(agent_o, 300000)
    #train_agent_x(agent_x, 300000)
    #agent_o.export_qtable()

    print("Agent O:")
    win_rate, draw_rate, loss_rate = test_agents(agent_o, agent_x)
    print(f"Win Rate: {win_rate:.2f}, Draw Rate: {draw_rate:.2f}, Loss Rate: {loss_rate:.2f}")

    #print("Agent X:")
    #win_rate, draw_rate, loss_rate = test_agent_x(agent_x)
    #print(f"Win Rate: {win_rate:.2f}, Draw Rate: {draw_rate:.2f}, Loss Rate: {loss_rate:.2f}")
