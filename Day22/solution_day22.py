import lcg_crack
from lcgrandom import LcgRandom

DINS = "deal into new stack"
DWI = "deal with increment"
CUT = "cut"
DECK_SIZE = 10007
FOLLOW_CARD = 2019

with open('input_d22.txt', 'r') as input_file:
    card_ops = [s.rstrip() for s in input_file.readlines()]


def deal_into_new(cur_pos):
    return DECK_SIZE - cur_pos - 1


def cut(cur_pos, cut_nb_cards):
    if cut_nb_cards >= 0:
        if cur_pos <= cut_nb_cards - 1:
            return DECK_SIZE - cut_nb_cards + cur_pos
        else:
            return cur_pos - cut_nb_cards
    else:
        return cut(cur_pos, DECK_SIZE + cut_nb_cards)


def deal_with_inc(cur_pos, increment):
    new_pos = cur_pos * increment
    return new_pos % DECK_SIZE


def run_shuffle(pos):
    for line in card_ops:
        if line.startswith(DINS):
            pos = deal_into_new(pos)
            # print("deal new", pos)
        elif line.startswith(DWI):
            pos = deal_with_inc(pos, int(line.split()[-1]))
            # print("increment", int(line.split()[-1]), pos)
        elif line.startswith(CUT):
            pos = cut(pos, int(line.split()[-1]))
            # print("cut", int(line.split()[-1]), pos)
        else:
            print("ERROR")
    return pos


print("Solution part 1:", run_shuffle(FOLLOW_CARD))

# part 2

'''
Although I was exploring in the right direction with modinv and functions, the working solution for part two
should mainly be credited to https://www.reddit.com/user/mcpower_/ for his (at least for me ;-) ) clear
explanation, to https://github.com/sonneveld/advent-of-code/tree/master/advent19/22 for some code hints and,
as indicated by Sonneveld, to https://www.nayuki.io/page/fast-skipping-in-a-linear-congruential-generator

Shuffling a single card produces an LCG pseudorandom sequence.
1) Shuffle cards forwards a few times to determine first few items in sequence
2) Determine modulus, multiplier, increment. (We know modulus from number of cards)
3) Skip through LCG sequence to get final number.
We know cards repeat every NUM_CARDS shuffles, so we can skip ahead NUM_CARDS - NUM_SHUFFLES
Alternatively, we can skip -NUM_SHUFFLES cause the lib allows it. :)
'''
DECK_SIZE_P2 = 119315717514047
NUM_SHUFFLES = 101741582076661


def run_reverse_shuffle(card_ops, cur_pos):

    def rev_deal_into_new(c_pos):
        p_pos = DECK_SIZE_P2 - c_pos - 1
        return p_pos

    # positive is left
    def rev_cut(c_pos, cut_pos):
        p_pos = (c_pos + cut_pos) % DECK_SIZE_P2
        return p_pos

    def rev_deal_with_inc(c_pos, increment):
        for fudge in range(0, increment):
            (q,r) = divmod(fudge * DECK_SIZE_P2 + c_pos, increment)
            if r == 0:
                return q
        raise Exception("uh oh")

    pos = cur_pos
    for line in reversed(card_ops):
        if line.startswith(DINS):
            pos = rev_deal_into_new(pos)
            # print("deal new", pos)
        elif line.startswith(DWI):
            pos = rev_deal_with_inc(pos, int(line.split()[-1]))
            # print("increment", int(line.split()[-1]), pos)
        elif line.startswith(CUT):
            pos = rev_cut(pos, int(line.split()[-1]))
            # print("cut", int(line.split()[-1]), pos)
        else:
            print("ERROR")

    return pos


seed = 2020

# generate some numbers so we can figure out state
cur_pos = 0
states = []
for x in range(10):
    states.append(cur_pos)
    cur_pos = run_reverse_shuffle(card_ops, cur_pos)

# the known modulus is NUM_CARDS, since that is the period it repeats
modulus, multiplier, increment = lcg_crack.crack_unknown_multiplier(states, DECK_SIZE_P2)

# skip ahead
randfast = LcgRandom(multiplier, increment, modulus, seed)
randfast.skip(NUM_SHUFFLES)
print("Solution part 2:", randfast.get_state())