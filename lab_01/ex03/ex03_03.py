def tao_tuple_tu_list(a):
    return tuple(a)
input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))
my_tuple = tao_tuple_tu_list(numbers)
print("List: ", numbers)
print("Tuple từ List: ", my_tuple)