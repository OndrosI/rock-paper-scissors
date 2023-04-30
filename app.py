import random
import plotly.graph_objs as go
from plotly.subplots import make_subplots

N = int(input("Zadejte počet hráčů: "))
M = int(input("Zadejte počet soupeřů, proti kterým hraje každý hráč: "))
K = int(input("Zadejte počet kol: "))
X = int(input("Vyrvoření nové generace hráčů: 1 - ANO, 0 - NE: "))

# Definice strategií hráčů
STRATEGIES = ['tit_for_tat', 'random', 'paper', 'rock']

# Funkce pro výpočet výsledku hry kámen-nůžky-papír
def get_score(player1, player2):
    if player1 == player2:
        return 0
    elif (player1 == 'rock' and player2 == 'scissors') or (player1 == 'paper' and player2 == 'rock') or (player1 == 'scissors' and player2 == 'paper'):
        return 1
    else:
        return -1

def init_strategy_choise(strategy):
    if strategy == 'paper':    
        choice = 'paper'
    elif strategy == 'rock':
        choice = 'rock'
    else:
        choice = random.choice(['rock', 'paper', 'scissors'])   
    return choice    

# Třída hráče
class Player:
    def __init__(self, strategy, index):
        self.strategy = strategy
        self.score = 0
        self.index = index
        self.choise = init_strategy_choise(strategy)
        self.history = [self.choise]
    
    # Metoda pro zahrání kola
    def play(self, opponents):
        scoress = []
        for opponent in opponents:
            if self.strategy == 'tit_for_tat':
                if 1 < len(opponent.history):
                    self.choise = opponent.history[-2]
                else:
                    self.choise = random.choice(['rock', 'paper', 'scissors'])
            elif self.strategy == 'random':
                self.choise = random.choice(['rock', 'paper', 'scissors'])
            elif self.strategy == 'paper':    
                self.choise = 'paper'
            else:
                self.choise = 'rock'
            #print("hraje ", opponent.index)
            scoress.append(get_score(self.choise, opponent.choise)) 
            self.history.append(self.choise)   
        
        #scores = [get_score(self.choise, opponent.choise) for opponent in opponents]
        self.score += sum(scoress)
    
    # Metoda pro křížení dvou hráčů a vytvoření potomka s malou pravděpodobností mutace strategie
    def crossover(self, other):
        if random.random() < 0.05:
            new_strategy = other.strategy
        else:
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
for i in range(K):
    # Hra každého hráče proti M soupeřům
    for j, player in enumerate(players):
        opponents = random.sample(players[:j] + players[j+1:], M)
        player.play(opponents)
        scores[j].append(player.score)
    
    if X==1: 
        # Evoluční krok
        players = evolve(players)
    
    fig1 = make_subplots(rows=1, cols=1, subplot_titles=[f'Kolo {i+1}'])

    for x, player_scores in enumerate(scores):
        fig1.add_trace(go.Scatter(y=player_scores, name=f'Player {x+1}, str: {players[x].strategy}'), row=1, col=1)
    
    fig1.update_layout(title=f'Kolo {i+1} hry kámen-nůžky-papír - výsledky',
                  xaxis_title='Kolo',
                  yaxis_title='Skóre')
    fig1.show()    

# Vykreslení výsledků
fig = make_subplots(rows=1, cols=N, subplot_titles=[f'{player.strategy}' for i, player in enumerate(players)])

for i, player_scores in enumerate(scores):
    fig.add_trace(go.Scatter(y=player_scores, name=f'Player {i+1}'), row=1, col=i+1)

fig.update_layout(title='Hra kámen-nůžky-papír - výsledky',
                  xaxis_title='Kolo',
                  yaxis_title='Skóre')

fig.show()
