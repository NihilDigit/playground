from operator import add, sub
from operator import mul, truediv


def make_ternary_constraint(a, b, c, ab, ca, cb):
    """通用的三元约束，处理三个连接器变量之间的关系
    约束 ab(a, b)=c, ca(c, a)=b, cb(c, b)=a
    即：如何通过两个已知的变量计算第三个变量"""

    def new_value():
        """在连接器改变时尝试推导其他连接器的值"""
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)] # 从 a, b, c 中取出非空值
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))

    def forget_value():
        """连接器忘记值时清除当前约束对它的影响"""
        for connector in (a, b ,c):
            connector['forget'](constraint) # 移除每个连接器和当前约束的关联
    
    constraint = {
        'new_val': new_value,
        'forget': forget_value
        }

    for connector in (a, b ,c):
        connector['connect'](constraint) # 将当前约束与连接器连接

    return constraint

def adder(a, b, c):
    """加法器的约束"""
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    """乘法器的约束"""
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def constant(connector, value):
    """常量赋值"""
    constraint = {} # 常量不和任何其他连接器相关，约束为空
    connector['set_val'](constraint, value)
    return constraint

def inform_all_except(source, message, constraints):
    """
    连接器利用这个功能来通知和它相关的约束，
    message值可以为 new_value 或 forget
    调用约束中更新值的函数
    """
    for c in constraints:
        if c != source: # 不要通知发起通知的约束
            c[message]() # 调用 message 方法

def connector(name=None):
    """连接器是一个对象，当它被赋予/遗忘一个值时，唤醒所有相关的约束。
    每个被唤醒的约束框轮询它的连接器来尝试确定连接器的值"""
    informant = None # 保存给这个连接器赋值的约束
    constraints = [] # 保存与这个连接器相关的约束

    def set_value(source, value):
        nonlocal informant # 记录给连接器赋值的约束
        val = connector['val']
        if val is None:
            # 当前连接器为空，则设置给定的值
            informant, connector['val'] = source, value
            if name is not None: # 对于没有设置name的连接器（如常量），值的改变不输出到终端
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints) #通知所有相关的约束
        else:
            # 不允许二次赋值
            if val != value:
                print('Contradiction detected:', val, 'vs', value)
    
    def forget_value(source):
        nonlocal informant # 访问存储约束的变量
        if informant == source:
            # 设置这个值的约束要求忘记这个值，则执行
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    
    connector = {
        'val': None, # 连接器存储的值
        'set_val': set_value, # 给连接器设置值
        'forget': forget_value, # 重置连接器
        'has_val': lambda: connector['val'] is not None, # 连接器是否为空的判断
        'connect': lambda source: constraints.append(source) # 将一个已有约束连接到连接器
        }
    
    return connector

def converter(c, f):
    """用约束条件来连接 c 和 f 两个变量"""
    u, v, w, x, y = [connector() for _ in range(5)]
    multiplier(c, w, u) # c * w = u
    multiplier(v, x, u) # v * x = u
    adder(v, y, f) # v + y = f
    constant(w, 9) # w = 9
    constant(x, 5) # x = 5
    constant(y, 32) # y = 32
    # 9 * c = (f - 32) * 5

celsius = connector('Celsius')
fahrenheit = connector('Fahrenheit')

converter(celsius, fahrenheit)

celsius['set_val']('user', 75)
