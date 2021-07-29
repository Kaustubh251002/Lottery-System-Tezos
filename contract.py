import smartpy as sp

class Lottery(sp.Contract):
    def __init__(self):
        self.init(
            userMap = sp.map(), 
            ticketToAddress = sp.map(tkey = sp.TNat, tvalue = sp.TAddress),
            previousWinners = sp.list(t = sp.TAddress), 
            idx = 0
            )
 

    @sp.entry_point
    def buyTicket(self, params):
        email = params.email
        self.data.userMap[email] = sp.record(
            name = params.name,
            number = params.number, 
        )
        # To assure one lottery ticket costs one tezos.
        sp.verify(sp.utils.nat_to_tez(sp.as_nat(params.qty)) == sp.amount)
        

        change = sp.local('change', sp.tez(0))
        canBuy = sp.local('canBuy', params.qty)
        remaining = sp.as_nat(5 - self.data.idx)
        sp.if sp.as_nat(params.qty) > remaining:
            canBuy.value = sp.to_int(remaining)
            change.value= sp.utils.nat_to_tez(sp.as_nat(params.qty - sp.to_int(remaining)))
        
        sp.for i in sp.range(1, canBuy.value + 1):
            self.data.ticketToAddress[self.data.idx] = sp.sender
            self.data.idx += 1

        sp.if change.value > sp.tez(0):
            sp.send(sp.sender, change.value)

        sp.if self.data.idx == 5:
            self.selectWinner()
            self.resetLottery()

    def selectWinner(self):
        randomId = sp.as_nat(sp.timestamp_from_utc_now() - sp.timestamp(0)) % self.data.idx
        sp.send(self.data.ticketToAddress[randomId], sp.tez(5))
        self.data.previousWinners.push(self.data.ticketToAddress[randomId])

    def resetLottery(self):
        self.data.idx = 0
        sp.for i in sp.range(0, self.data.idx):
            del self.data.ticketToAddress[self.data.idx]
        


if "templates" not in __name__:
    @sp.add_test(name = "LotteryTicket")
    def test():
        bhavya = sp.test_account('Bhavya')
        kaustubh= sp.test_account('Kaustubh')
        raman= sp.test_account('Raman')
        garv= sp.test_account('Garv')
        
        
        scenario = sp.test_scenario()
        c = Lottery()
        scenario += c
        
        scenario.h1('Lottery Test')
        
        scenario += c.buyTicket(qty = 1, email="bgoel4132@gmail.com", name="Bhavya Goel", number = 7042089702).run(sender = bhavya, amount = sp.tez(1))
        scenario += c.buyTicket(qty = 1, email="kmishra@gmail.com", name="Kaustubh Mishra", number = 7042089702).run(sender = kaustubh, amount = sp.tez(1))
        scenario += c.buyTicket(qty = 1, email="garv12@gmail.com", name="Garv Gupta", number = 7042089702).run(sender = garv, amount = sp.tez(1))
        scenario += c.buyTicket(qty = 1, email="raman56@gmail.com", name="Raman Sharma", number = 7042089702).run(sender = raman, amount = sp.tez(1))
        scenario += c.buyTicket(qty = 1, email="kmishra@gmail.com", name="Kaustubh Mishra", number = 7042089702).run(sender = kaustubh, amount = sp.tez(1))



        scenario.h3('Buy Multiple (Change)')
        scenario += c.buyTicket(qty = 3, email="bgoel4132@gmail.com", name="Bhavya Goel", number = 7042089702).run(sender = bhavya, amount = sp.tez(3))
        scenario += c.buyTicket(qty = 2, email="garv12@gmail.com", name="Garv Gupta", number = 7042089702).run(sender = garv, amount = sp.tez(2))
        
        scenario.h3('Final Contract Balance')
        
        scenario.show(c.balance)
