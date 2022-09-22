import functools
call_list = []

def add_to_call_list(func):
    call_list.append(func)

def on_call(obj:list) -> None:
    print(id(obj))

def main():
    for i in range(4):
        n = [i]
        print("id = ", id(n))
        # case1: 这种写法 n 都会绑定到最后一个
        # add_to_call_list(lambda: on_call(n))

        # case2: 使用默认参数，防止绑定到最后一个 n
        add_to_call_list(lambda n=n: on_call(n))

        # case2: 这种写法会绑定到不同的 n
        # add_to_call_list(functools.partial(on_call, n))

    for func in call_list:
        func()

main()

# case1 运行结果
# id =  2002560696128
# id =  2002561020096
# id =  2002560696128
# id =  2002561020096
# 2002561020096
# 2002561020096
# 2002561020096
# 2002561020096

# case2 运行结果
# id =  2422935184064
# id =  2422935184256
# id =  2422935184192
# id =  2422935184832
# 2422935184064
# 2422935184256
# 2422935184192
# 2422935184832
