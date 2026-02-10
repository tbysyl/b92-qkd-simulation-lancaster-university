import random
import math

key_length_sum = 0
eve = False
angle = math.pi / 4

def rng(n):
    key = []
    for bit in range(n):
        key.append(random.randint(0,1))

    return key

def overlap(theta):
    return math.cos(theta) ** 2

def bob_measure(alice_bit):
    p = 1 - overlap(angle)
    bob_bit = random.random()
    if alice_bit == 0:
        if bob_bit < p:
            return 0
        else:
            return None
    else:
        if bob_bit < p:
            return 1
        else:
            return None

def eve_attack(alice_bit):
    p = 1 - overlap(angle)
    if random.random() < p:
        return alice_bit
    else:
        return random.randint(0,1)

n = int(input("How many bits in the basis?: "))
average_num = int(input("How many runs to average?: "))

alice_base = rng(n)

for j in range(average_num):
    discards = 0
    bob_key = []
    alice_key = []
    for i in range(n):
        a = alice_base[i]
        b = bob_measure(alice_base[i])

        if b == None:
            discards += 1

        if eve:
            a = eve_attack(a)

        if b is not None:
            alice_key.append(a)
            bob_key.append(b)

        final_key = [a for a, b in zip(alice_key, bob_key) if a == b]

        if len(final_key) > 0:
            difference = len(alice_key) - len(final_key)
            qber = (difference / len(alice_key)) * 100
    
    print(f"[{j}]")
    print(f"Alice sent: {alice_key}")
    print(f"Bob received: {bob_key}")
    print(f"Received length: {len(alice_key)}")
    print(f"Fails: {discards}")
    print(f"Final key: {final_key}")
    print(f"Final key length: {len(final_key)}")
    print(f"QBER: {qber}%")

    key_length_sum += len(alice_key)

print(f"Average key length: {key_length_sum / average_num}")

