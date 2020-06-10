def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def parse_address_by_street_num(address):
    street = ''
    number = ''
    for c in address:
        if c.isdigit():
            number += c
        else:
            street += c
    return street.rstrip(), number.rstrip()

# street, num = parse_address_by_street_num('קרן היסוד 10')
# assert street=='קרן היסוד'
