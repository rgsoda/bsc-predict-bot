from strategies.BaseBot import BaseBot
from typing import Optional
from classes.RoundClass import Round
from classes.BetClass import Bet, Direction

from classes.RoundClass import Round
from typing import Optional, List
from classes.BetClass import Bet
import time



# NOTE: Class must be named Bot
class Bot(BaseBot):

    already_bet = False
    multiplier = 1
    last_bet = None

    def get_bet(self, upcoming: Round) -> Optional[Bet]:

        timestamp = time.time()
        msg = "Do akcji jeszcze {} sek, bull:{}, bear:{} epoch:{}"
        to_action = upcoming.lockTimestamp - timestamp
        print(msg.format(to_action, upcoming.bullAmount, upcoming.bearAmount, upcoming.epoch)) 


        incoming_bet = upcoming
        actual_bet = None
        last_winner_bet = None


        # tutaj pobieraby ostatniego zwyciężce
        completed = [r for r in self.history if r.oracleCalled]
        not_completed = [r for r in self.history if not r.oracleCalled]
        if len(completed) > 0:
            last_winner_bet = completed[-1]


        actual_bet = not_completed[-2]


        print("incoming_bet", incoming_bet)
        print("actual_bet", actual_bet)
        print("last winner", last_winner_bet)

        return 
        if upcoming.lockTimestamp - timestamp < 10:
            if self.already_bet:
                return
            print("tutaj będzie bet, bo mniej niż 10sekjund")

            # sprawdzamy gdzie aktualnie jest wiecej/mniej
            direction = Direction.BEAR
            if upcoming.bullAmount < upcoming.bearAmount:
                direction = Direction.BULL


            if self.last_bet: # już postawiliśmy poprzednio, sprawdzamy czy wygraliśmy
                if self.last_bet.direction == last_winner.winner:
                    print("Stawiamy na {}, ostatnio wygrał {}, stawka {}".format(direction, last_winner.winner, self.bet_size_eth * self.multiplier))
                   #self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth * self.multiplier, epoch=upcoming.epoch)
                    self.already_bet = True
                    self.multiplier = 1
                else:
                    print("Stawialiśmy na {}, ale ostatnio wygrał {}".format(direction, last_winner.winner))
                    print("Podnosimy stawkę")
                    self.multiplier *= 2
                    return
            else: # pierwse postawienie beta, na cokolwiek
                #self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
                pass

        else:
            self.already_bet = False 