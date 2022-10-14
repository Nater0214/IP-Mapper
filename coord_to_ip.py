# coord_to_ip.py
# Converts a big image coordinate to an ip address

while True:
    try:
        x, y = input("Coords: ").split(',')
        x, y = int(x), int(y)
    except ValueError:
        pass

    a = x // 256
    b = x % 256
    c = y // 256
    d = y % 256
    print(f"{a}.{b}.{c}.{d}")