from audioop import mul
from strategies.BaseBot import BaseBot
from typing import Optional
from classes.RoundClass import Round
from classes.BetClass import Bet, Direction

from classes.RoundClass import Round
from typing import Optional, List
from classes.BetClass import Bet
from contracts.prediction import claim, get_current_epoch, get_history
import time



# NOTE: Class must be named Bot
class Bot(BaseBot):

    already_bet = False
    multiplier = 1
    last_bet = None

    def get_bet(self, upcoming: Round) -> Optional[Bet]:
        oracle = self.oracle_history[-1].answer
        self.history = get_history()
        #import pdb; pdb.set_trace()


        # tutaj pobieraby ostatniego zwyciężce
        completed = [r for r in self.history if r.oracleCalled]
        not_completed = [r for r in self.history if not r.oracleCalled]
        actual_bet = not_completed[-2]


        direction = Direction.BEAR
        if upcoming.bullAmount < upcoming.bearAmount:
            direction = Direction.BULL

        timestamp = time.time()
        msg = "Do akcji jeszcze {} sek, bull:{:.2f}, bear:{:.2f} epoch:{} oracle:{:.2f} lock_price:{:.2f}, diff:{:.2f} stawiamy na {}"
        to_action = int(upcoming.lockTimestamp - timestamp)
        if not self.already_bet:
            print(msg.format(
                to_action, 
                upcoming.bullAmount, 
                upcoming.bearAmount, 
                upcoming.epoch, 
                oracle, 
                actual_bet.lockPrice,
                oracle - actual_bet.lockPrice,
                direction)) 



        if upcoming.lockTimestamp - timestamp < 10:
            print('mnie niz 10')
            if self.already_bet:
                print('juz postawione, spadam')
                return
            if not self.last_bet:
                print('nie było, tworze kontrakt')
                self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
                self.already_bet = True
                print(self.last_bet)
            else:
                print('był kontrakt', self.last_bet)

                if oracle < actual_bet.lockPrice:
                    last_direction = direction.BEAR
                    if self.last_bet.direction == direction.BEAR:
                        self.multiplier = 1
                    else:
                        self.multiplier = self.multiplier * 2
                else:
                    last_direction = direction.BULL
                    if self.last_bet.direction == direction.BULL:
                        self.multiplier = 1
                    else:
                        self.multiplier = self.multiplier * 2

                self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth * self.multiplier, epoch=upcoming.epoch)
                print("Stawiamy na {}, stawka {}".format(direction, self.bet_size_eth * self.multiplier))
                print(self.last_bet)
                self.already_bet = True

        else:
            if self.already_bet:
                self.already_bet = False
                    
        #     if self.last_bet: # już postawiliśmy poprzednio, sprawdzamy czy wygraliśmy
        #         if self.last_bet.direction == last_winner_bet.winner:
        #             print("Stawiamy na {}, ostatnio wygrał {}, stawka {}".format(direction, last_winner_bet.winner, self.bet_size_eth * self.multiplier))
        #             self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth * self.multiplier, epoch=upcoming.epoch)
        #             self.already_bet = True
        #             self.multiplier = 1
        #         else:
        #             print("Stawialiśmy na {}, ale ostatnio wygrał {}".format(direction, last_winner_bet.winner))
        #             print("Podnosimy stawkę")
        #             self.multiplier *= 2
        #             return
        #     else: # pierwse postawienie beta, na cokolwiek
        #         print("Stawiamy na {}, stawka {}".format(direction, self.bet_size_eth * self.multiplier))
        #         self.last_bet = Bet(direction=direction, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
        #         print(self.last_bet)
        #         self.already_bet = True

        # else:

        #     self.already_bet = False


# from web3_provider import web3
# from web3.middleware import geth_poa_middleware
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)
# block = web3.eth.get_block('latest')
# block
