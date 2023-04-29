import numpy as np
import random
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# N - počet hráčů
# M - počet soupeřů, proti kterým hraje každý hráč
N = 10
M = 5

# Definice strategií hráčů
STRATEGIES = ['tit for tat', 'random', 'rock', 'paper']

# Funkce pro výpočet výsledku hry kámen-nůžky-papír
def get_score(player1, player2):
    if player1 == player2:
        return 0
    elif (player1 == 'rock' and player2 == 'scissors') or (player1 == 'paper' and player2 == 'rock') or (player1 == 'scissors' and player2 == 'paper'):
        return 1
    else:
        return -1

# Třída hráče
class Player:
    def __init__(self, strategy, index):
        self.strategy = strategy
        self.score = 0
        self.index = index
    
    # Metoda pro zahrání kola
    def play(self, opponents):
        choices = [opponent.strategy for opponent in opponents]
        opponentPlayers = [opponent.index for opponent in opponents]
        
        print(opponentPlayers)
        
        if self.strategy == 'tit for tat':
            if len(choices) == 0:
                choice = random.choice(['rock', 'paper', 'scissors'])
            else:
                choice = choices[-1]
        elif self.strategy == 'random':
            choice = random.choice(['rock', 'paper', 'scissors'])
        elif self.strategy == 'paper':    
            choice = 'paper'
        else:
            choice = 'rock'
        
        scores = [get_score(choice, opponent.strategy) for opponent in opponents]
        self.score += sum(scores)
    
    # Metoda pro křížení dvou hráčů a vytvoření potomka s malou pravděpodobností mutace strategie
    def crossover(self, other):
        if random.random() < 0.5:
            new_strategy = self.strategy
        else:
            new_strategy = other.strategy
        
        if random.random() < 0.05:
            new_strategy = random.choice(STRATEGIES)
        
        return Player(new_strategy, self.index)

# Funkce pro evoluční krok
def evolve(players):
    # Seřazení hráčů podle skóre
    players = sorted(players, key=lambda p: p.score, reverse=True)
    
    # Vytvoření nové generace hráčů
    new_players = [players[0]]
    for i in range(1, N):
        parent1 = players[random.randint(0, int(N/2))]
        parent2 = players[random.randint(0, int(N/2))]
        child = parent1.crossover(parent2)
        new_players.append(child)
    
    return new_players

# Inicializace hráčů
players = [Player(random.choice(STRATEGIES), i) for i in range(N)]

# Hlavní smyčka hry
scores = [[] for i in range(N)]
for i in range(20):
    print(f'Kolo: {i}')
    # Hra každého hráče proti M soupeřům
    for j, player in enumerate(players):
        print(f'   Hráč {j+1} proti:')
        opponents = random.sample(players[:j] + players[j+1:], M)
        player.play(opponents)
        scores[j].append(player.score)
    
    # Evoluční krok
    #players = evolve(players)

# Vykreslení výsledků
fig = make_subplots(rows=1, cols=N, subplot_titles=[f'Player {i+1} Strategie: {player.strategy}' for i, player in enumerate(players)])

for i, player_scores in enumerate(scores):
    fig.add_trace(go.Scatter(y=player_scores, name=f'Player {i+1}'), row=1, col=i+1)

fig.update_layout(title='Hra kámen-nůžky-papír - výsledky',
                  xaxis_title='Kolo',
                  yaxis_title='Skóre')

fig.show()
