from random import randint

class Bank: 
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.usedCoins = list()
        self.users = dict()

    def sign_coin(self, coin, ID):
        """ Blinded signature """
        return 0

    def validate_coin(self, coin, ID):
        """ Validate a coin from a user """
        return 0

    def register_user(self, name, id):
        """ Add user to bank with their wallet? """
        self.users[name] = id
        print(self.users)



class User: 
    def __init__(self, name):
        super().__init__()
        self.userName = name
        self.ID = random.randint(10000, 40000)
        self.wallet = dict()
        self.tk_quad = list()
        
    def add_coin(self, coin):
        if(coin is 0 or coin < 1):
            raise Exception("Coin is invalid")

        self.wallet[coin] = {}
        print(f"{self.userName} added a coin to wallet. Wallet size is now: {len(self.wallet)}")

    def two_k_quad(self, coin):
        """ Create the random number for the 2k quadruples """
        for i in range (0, 2000):
            self.tk_quad.append([])
        return 0

    def sign_coin(self):
        return 0

    def send_coing(self, user):
        return 0
    
    def recv_coin(self, coin, user):
        return 0
    
    def check_recvd_coin(self, coin, bank):
        return 0


if __name__ == '__main__':
    alice = User('Alice')
    bob = User('Bob')
    bank = Bank('TestBank')

    print(f"Users: {alice.userName} and {bob.userName}")

    bank.register_user(alice.userName, alice.ID)
    bank.register_user(bob.userName, bob.ID)
    
