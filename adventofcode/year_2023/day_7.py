from adventofcode.year_2023.puzzle2023 import Puzzle2023
from collections import Counter

CARD_VALUE = {
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'T' : 10, 
    'J' : 11,
    'Q' : 12,
    'K' : 13,
    'A' : 14
}

CARD_VALUE_JOKER = {
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'T' : 10, 
    'J' : 1,
    'Q' : 12,
    'K' : 13,
    'A' : 14
}
    
HAND_TYPE = {
    "high card" : 0,
    "one pair" : 1,
    "two pairs" : 2,
    "three of a kind" : 3,
    "full house" : 4,
    "four of a kind" : 5,
    "five of a kind" : 6,
}

class Card():
    def __init__(self, symbol, card_values = CARD_VALUE):
        self.card_values = card_values
        if symbol not in card_values:
            raise ValueError(f"Invalid card symbol : {symbol}")
        self.symbol = symbol
        
    @property
    def value(self):
        return self.card_values[self.symbol]
        
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __ne__(self, other):
        return self.symbol != other.symbol
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __repr__(self) -> str:
        return f"{self.symbol}"

class Hand:
    def __init__(self, cards, joker = False):
        self.joker = joker
        self.cards = [Card(card, card_values=CARD_VALUE_JOKER if joker else CARD_VALUE) for card in cards]
        
    def __repr__(self) -> str:
        return f"Hand ({''.join(str(card) for card in self.cards)})"
    
    def get_counter(self):
        count = Counter(card.symbol for card in self.cards)
        if self.joker :
            cnt_joker = count['J']
            if cnt_joker == 5 :
                return count
            count = {k : v for k, v in count.items() if k != 'J'}
            max_cnt = max(count.values()) 
            for k, v in count.items():
                if v == max_cnt :
                    count[k] += cnt_joker
                    break
        return count
    
    @property
    def type(self) : 
        cnt_vals = self.get_counter().values()
        if 5 in cnt_vals : 
            return "five of a kind"
        elif 4 in cnt_vals :
            return "four of a kind"
        elif 3 in cnt_vals :
            if 2 in cnt_vals :
                return "full house"
            else :
                return "three of a kind"
        elif 2 in cnt_vals :
            if len(cnt_vals) == 3 :
                return "two pairs"
            else :
                return "one pair"
        else :
            return "high card"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return False
        return ''.join(str(card) for card in self.cards) == ''.join(str(card) for card in other.cards)
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return False
        return ''.join(str(card) for card in self.cards) != ''.join(str(card) for card in other.cards)
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
           raise ValueError(f"Cannot compare {self} with {other}")
        if self.type == other.type :
            for i, card in enumerate(self.cards):
                if card > other.cards[i] :
                    return True
                elif card < other.cards[i] :
                    return False
            return False
        return HAND_TYPE[self.type] > HAND_TYPE[other.type]
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise ValueError(f"Cannot compare {self} with {other}")
        if self.type == other.type :
            for i, card in enumerate(self.cards):
                if card >= other.cards[i] :
                    return True
                elif card < other.cards[i] :
                    return False
            return True
        return HAND_TYPE[self.type] >= HAND_TYPE[other.type]
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise ValueError(f"Cannot compare {self} with {other}")
        if self.type == other.type :
            for i, card in enumerate(self.cards):
                if card < other.cards[i] :
                    return True
                elif card > other.cards[i] :
                    return False
            return False
        return HAND_TYPE[self.type] < HAND_TYPE[other.type]

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            raise ValueError(f"Cannot compare {self} with {other}")
        if self.type == other.type :
            for i, card in enumerate(self.cards):
                if card <= other.cards[i] :
                    return True
                elif card > other.cards[i] :
                    return False
            return True
        return HAND_TYPE[self.type] <= HAND_TYPE[other.type]

class Puzzle7(Puzzle2023):
    def __init__(self):
        super().__init__(7)
        
    def parse_input(self, joker = False):
        res = []
        for line in self.input:
            cards, bid = line.strip().split(' ')
            res.append({"hand" : Hand(cards, joker), "bid" : int(bid)})
        return res
            
    def run_part1(self):    
        games = sorted(self.parsed_input, key = lambda game : game['hand'])
        return sum(game['bid'] * (i + 1) for i, game in enumerate(games)) 
    
    def run_part2(self):
        games = self.parse_input(joker = True)
        games = sorted(games, key = lambda game : game['hand'])
        return sum(game['bid'] * (i + 1) for i, game in enumerate(games)) 

puzzle = Puzzle7()
puzzle.run()