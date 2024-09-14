def dec2bin_iter(og_num, array):
    """
    递归函数，将十进制非负整数转换为二进制表示（不包括符号位）
    :param og_num: 输入的十进制非负整数
    :param array: 用于存储二进制表示的数组，按从低位到高位的顺序存储
    :return: None，结果直接修改array参数
    """
    if og_num == 0:
        return
    array.append(og_num & 1)
    dec2bin_iter(og_num >> 1, array)


def bin_generator(og_num):
    """
    将十进制整数（包括负数）转换为其二进制补码表示
    :param og_num: 输入的十进制整数
    :return: 返回输入数字的二进制补码表示，包括符号位
    """
    temp = []
    dec2bin_iter(abs(og_num), temp)

    is_negative = og_num < 0

    if is_negative:
        # 对于负数，执行取反操作
        for i in range(len(temp)):
            temp[i] = 1 - temp[i]

        # 执行加1操作
        for i in range(len(temp)):
            if temp[i] == 0:
                temp[i] = 1
                break
            temp[i] = 0

    # 添加符号位并反转数组以得到正确的位顺序
    return [int(is_negative)] + temp[::-1]


def main():
    """
    主函数，处理用户输入并调用相应的转换函数
    """
    while (user_input := input("Input a DEC number and I'll give you its BIN format: ").lower()) != 'q':
        # 验证输入是否为有效的整数（正数或负数）
        if not ((user_input.startswith('-') and user_input[1:].isdigit()) or user_input.isdigit()):
            print(f"    {user_input} is not valid, Please enter a signed integer")
            print(f"    Press 'q' to exit")
            continue

        # 转换输入的十进制数为二进制补码
        converted_number = bin_generator(int(user_input))

        # 打印结果
        print(f'    DEC number {user_input} can be represented as BIN number 0b' + ''.join(
            map(str, converted_number)))
        print(f"    Press 'q' to exit")


if __name__ == '__main__':
    main()
    print('Program Ended Successfully')
