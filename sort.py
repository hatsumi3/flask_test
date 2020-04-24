import random

def sort_add_num(list_, num):
    for x in sorted(list_):
        yield x + num

if __name__ == "__main__":
    
    list_ = [random.randint(0, 100) for _ in range(10)]
    print(list_)
    for x in sort_add_num(list_, 10):
        print(x)

    print(list(sort_add_num(list_, 10)))