__author__ = 'Michal'



def solve(result='money', *args): # ARGS[0] + ARGS[1] + ... == RESULT
    (keys, ) = init(result, args)
    print(keys)

def init(result, args):
    if not args or not result or not ''.join(args): # czy nikt mnie nie oszukuje
        raise ValueError

    keywords = args # lewa część równania
    result = 'money' # prawa część równania
    keys = ''.join(keywords) + result # sprowadź lewą część równania do jednego string
    keys = filter(function_or_None=lambda elem: elem if elem not in keys else None, iterable=keys) # usuń powtórzone litery
    if len(keys) > 10:
        print('nie do rozwiązania, liczba liter > 10')
    return (keys,)

def fenotyp(cecha, arg):
        if cecha is None:
            print("coś jest nie tak z funckją fenotypu")
            raise IndexError

def get_char(num):
    return chr(97 + num)
def get_num(char):
    return ord(char) - 97


if __name__ == "__main__":
    solve('send', 'more', result='monet')