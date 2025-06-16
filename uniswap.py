import math


def price_to_tick(p):
    return math.floor(math.log(p, 1.0001))


index_c = price_to_tick(5000)
index_l = price_to_tick(4545)
index_u = price_to_tick(5500)
print(index_c, index_l, index_u)  # 85176 84222 86129

print(1.0001**85176)  # 4999.904785770063

q96 = 2**96


def price_to_sqrtp(p):
    return int(math.sqrt(p) * q96)


sqrtp_cur = price_to_sqrtp(5000)
sqrtp_low = price_to_sqrtp(4545)
sqrtp_upp = price_to_sqrtp(5500)
print(sqrtp_cur, sqrtp_low, sqrtp_upp)
# 5602277097478614198912276234240 5341294542274603406682713227264 5875717789736564987741329162240


def Liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return (amount * (pa * pb) / q96) / (pb - pa)


def Liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount * q96 / (pb - pa)


eth = 10**18
amount_eth = 1 * eth
amount_usdc = 5000 * eth

liq0 = Liquidity0(amount_eth, sqrtp_cur, sqrtp_upp)
liq1 = Liquidity1(amount_usdc, sqrtp_cur, sqrtp_low)
liq = int(min(liq0, liq1))
print(liq)  # 1517882343751509868544


# 根据最新的 Liquidity 更新 x 和 y 的值
def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * q96 * (pb - pa) / pa / pb)


def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * (pb - pa) / q96)


amount0 = calc_amount0(liq, sqrtp_upp, sqrtp_cur)
amount1 = calc_amount1(liq, sqrtp_low, sqrtp_cur)
print(amount0, amount1)  # 998976618347425408 5000000000000000000000


# 使用 42 USDC 购买 ETH
amount_in = 42 * eth
price_diff = (amount_in * q96) // liq
price_next = sqrtp_cur + price_diff
print("Next price: ", (price_next / q96) ** 2)
print("New sqrt price: ", price_next)
print("New tick: ", price_to_tick((price_next / q96) ** 2))
"""
Next price:  5003.913912782393
New sqrt price:  5604469350942327889444743441197
New tick:  85184
"""

amount_in = calc_amount1(liq, price_next, sqrtp_cur)
amount_out = calc_amount0(liq, price_next, sqrtp_cur)

print("USDC in: ", amount_in / eth)
print("ETH out: ", amount_out / eth)
"""
USDC in:  42.0
ETH out:  0.008396714242162444
"""

# 考虑卖出 ETH 的情况
# Swap ETH for USDC
amount_in = 0.01337 * eth

print(f"\nSelling {amount_in / eth} ETH")  # Selling 0.01337 ETH

price_next = int((liq * q96 * sqrtp_cur) // (liq * q96 + amount_in * sqrtp_cur))
print("New price: ", (price_next / q96) ** 2)
print("New sqrt price: ", price_next)
print("New tick: ", price_to_tick((price_next / q96) ** 2))
"""
New price:  4993.777388290041
New sqrt price:  5598789932670289186088059666432
New tick:  85163
"""

amount_in = calc_amount0(liq, price_next, sqrtp_cur)
amount_out = calc_amount1(liq, price_next, sqrtp_cur)

print("ETH in: ", amount_in / eth)
print("USDC out: ", amount_out / eth)
"""
ETH in:  0.013369999999998142
USDC out:  66.80838889019013
"""


# 将一个特定的 tick index 转换为 word position 和 bit position
def tick_to_word_and_bit(tick):
    word_pos = tick // 256
    bit_pos = tick % 256
    return word_pos, bit_pos


word_pos, bit_pos = tick_to_word_and_bit(85176)
print(word_pos, bit_pos)  # 332 184


# 将 word position 和 bit position 转换为 tick index
def word_and_bit_to_tick(word_pos, bit_pos):
    return word_pos * 256 + bit_pos


tick = word_and_bit_to_tick(word_pos, bit_pos)
print(tick)  # 85176

tick = 85176
word_pos = tick >> 8  # or tick // 2 ** 8
bit_pos = tick % 256
print(f"Word position: {word_pos}, Bit position: {bit_pos}")

tick = -200697
word_pos = tick >> 8  # or tick // 2 ** 8
word_pos1 = int(tick / 256)
bit_pos = tick % 256
print(f"Word position: {word_pos}, Bit position: {bit_pos}")
print(f"Word position: {word_pos1}, Bit position: {bit_pos}")
