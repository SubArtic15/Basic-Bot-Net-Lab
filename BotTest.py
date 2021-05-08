from multiprocessing import Process, Value
from string import ascii_uppercase
from itertools import permutations


def my_print(name, shared_value):
    if not shared_value.value:
        print("Shared Value is False")

        print(name, name == "CVB")

        if name == "CVB":
            print("Setting Shared Value to True")
            shared_value.value += 1

    else:
        print("Shared Value is True")



if __name__ == '__main__':
    IS_FOUND = Value('b', False)

    perms = list(permutations(ascii_uppercase, 3))

    ITER_SIZE = 500

    for start_index in range(0, len(perms), ITER_SIZE):
        print(start_index)
        proc_list = []
        for p in perms[start_index:start_index + ITER_SIZE]:
            proc_list.append(Process(target=my_print, args=("".join(p), IS_FOUND,)))

        for proc in proc_list:
            proc.start()

        for proc in proc_list:
            proc.join()
