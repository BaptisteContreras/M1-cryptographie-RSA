import sympy
import random
import math
import sys
sys.setrecursionlimit(10**6)

class rsa:

    def exp_func(self, x, y):
        exp = bin(y)
        value = x

        for i in range(3, len(exp)):
            value = value * value
            if (exp[i:i + 1] == '1'):
                value = value * x
        return value

    def expmodrap(self, a, e, n):
        p = 1
        while e > 0:
            if e % 2 == 1:
                p = (p * a) % n
            a = (a * a) % n
            e = e // 2
        return p

    def encrypt(self, message, publicKey):
        #blocks = [glued[x*4:(4*x)+4].zfill(4) for x in range(math.ceil(len(glued)/4))]
        #return "".join([str(pow(int(str(ord(message[i])).zfill(3)), publicKey[0])%publicKey[1]) for i in range(len(message))])
        encrypted = "".join([str(ord(message[i])).zfill(3) for i in range(len(message)) ])
        print("plain ord : " + encrypted)
        return self.expmodrap(int(encrypted), publicKey[0], publicKey[1])


    def decrypt(self, encrypted, privateKey):
        (p, q, d) = privateKey
        n = p * q

        message = str(self.expmodrap(encrypted,d,n))
        if(len(message)%3 != 0):
            message = "0"+message
        print("plain decrypted : " + message)
        block = [chr(int(message[x*3:(3*x)+3].zfill(3))) for x in range(math.ceil(len(str(message))/3))]

        return ''.join(block)

    ## a = 47, b = 35
    ## 47 = 35 * 1 + 12
    def euclide_etendu(self, a, b, coef):

        _a = b
        _b = a % b
        q = int(a // b)

        if (_b == 0):
            return coef

        current = len(coef)
        u = coef[current - 2][0] - (q * coef[current - 1][0])
        v = coef[current - 2][1] - (q * coef[current - 1][1])
        coef.append([u, v])
        return self.euclide_etendu(_a, _b, coef)

    def generateKey(self, k):
        p = sympy.randprime(pow(2, (k / 2) - 1), pow(2, (k / 2)) - 1)
        q = sympy.randprime(pow(2, (k / 2) - 1), pow(2, (k / 2)) - 1)
        while p == q:
            p = sympy.randprime(pow(2, (k / 2) - 1), pow(2, (k / 2)) - 1)
            q = sympy.randprime(pow(2, (k / 2) - 1), pow(2, (k / 2)) - 1)

        print("p : " + str(p))
        print("q : " + str(q))

        n = p * q

        print('N : ' + str(n))

        phiN = (p - 1) * (q - 1)

        d = -1
        e = 3
        usedE = []
        while d < 0:
            while sympy.gcd(e, phiN) != 1 or e in usedE:
                e = random.randint(2, phiN - 1)
            usedE.append(e)
            d = self.euclide_etendu(e, phiN, [[1, 0], [0, 1]])
            d = d[len(d) - 1][0]



        print('phiN : ' + str(phiN))
        print('e : ' + str(e))

        print('d : ' + str(d))
        print('------- Génération end ----------')
        return (e, n), (p, q, d)


def test():
    k = input("Taille de la clé (2000 max conseillé) : ")
    r = rsa()
    publicK, privateK = r.generateKey(int(k))
    message = "Hello"
    cipher = r.encrypt(message, publicK)
    print("cipher : " + str(cipher))
    decrypt = r.decrypt(cipher,privateK)
    print("decrypt : " + str(decrypt))


def handle():
    mode = input("Mode (1:test / 2:interactive) \n ====>")
    if int(mode) == 1:
        test()
    else:
        interactive()

def interactive():
    m = int(input("Action : \n générer PublicKey :1 \n générer PrivateKey :2 \n encrypter :3 \n décrypter :4 \n ===> "))
    r = rsa()
    if m == 1:
        k = input("Taille de la clé (2000 max conseillé) : ")
        public, private = r.generateKey(int(k))
        print("clé publique" + str(public))
    elif m ==2:
        k = input("Taille de la clé (2000 max conseillé) : ")
        public, private = r.generateKey(int(k))
        print("clé privée" + str(private))
    elif m ==3:
        e = input("e :")
        n = input("n :")
        msg = input("Votre message : ")
        encrypted = r.encrypt(msg, (e,n))
        print(encrypted)
    else:
        p = int(input("p :"))
        q = int(input("q :"))
        d = int(input("d :"))
        encrypted = int(input("Votre message encrypté : "))
        print(r.decrypt(encrypted,(p,q,d)))

handle()
