import smartpy as sp

class Lottery(sp.Contract):
    def __init__(self):
        self.init(
            limit = 5,
            ticketToAddress = sp.map(tkey = sp.TNat, tvalue = sp.TAddress),
            id = 0,
            previousWinners = sp.list(t = sp.TAddress)
        )
    
    @sp.entry_point
    def buyTicket(self, qty):
        sp.verify(sp.utils.nat_to_tez(qty) == sp.amount)
        
        change = sp.local('change', sp.tez(0))
        canBuy = sp.local('canBuy', qty)
        remaining = sp.as_nat(self.data.limit - self.data.id)
        sp.if qty > remaining:
            canBuy.value = remaining
            change.value = sp.utils.nat_to_tez(sp.as_nat(qty - remaining))
        
        sp.for i in sp.range(1, canBuy.value + 1):
            self.data.ticketToAddress[self.data.id] = sp.sender
            self.data.id += 1

        sp.if change.value > sp.tez(0):
            sp.send(sp.sender, change.value)

        sp.if self.data.id == 5:
            self.selectWinner()
            self.resetLottery()
    
    def selectWinner(self):

        randomId = (sp.timestamp_from_utc_now() - sp.timestamp(0)) % 5

        sp.send(self.data.ticketToAddress[randomId], sp.tez(5))
        self.data.previousWinners.push(self.data.ticketToAddress[randomId])
        
    
    def resetLottery(self):
        self.data.id = 0
        sp.for i in sp.range(0, self.data.limit):
            del self.data.ticketToAddress[i]
        
            
@sp.add_test(name = "Lottery Test")
def test():

    aa = sp.test_account('A')
    bb= sp.test_account('B')
    cc = sp.test_account('C')
    dd = sp.test_account('D')
    ee = sp.test_account('E')
    
    scenario = sp.test_scenario()
    c = Lottery()
    scenario += c
    
    scenario.h1('Lottery Test')
    
    scenario += c.buyTicket(1).run(sender = aa, amount = sp.tez(1))
    scenario += c.buyTicket(1).run(sender = bb, amount = sp.tez(1))
    scenario += c.buyTicket(1).run(sender = cc, amount = sp.tez(1))
    scenario += c.buyTicket(1).run(sender = ee, amount = sp.tez(1))
    
    scenario.h3('Buy Multiple (Change)')
    scenario += c.buyTicket(3).run(sender = dd, amount = sp.tez(3))
    
    scenario.h3('Final Contract Balance')
    
    scenario.show(c.balance)
