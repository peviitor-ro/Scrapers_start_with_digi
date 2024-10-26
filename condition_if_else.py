
number1 = input('Scrie un numar: ')
number2 = input('Scrie al doilea numar: ')

number1 = int(number1)
number2 = int(number2)

# # condition if/else
# if number1 > number2:
#     print(f'number1 care este ->{number1} este mai mare decat number2, care este -> {number2}')
# elif number1 < number2:
#     print(f'number1 care este -> {number1} este mai mic decat number2, care este -> {number2}')
# # else number1 < number2:
# #     print('number1 este mai mic decat numbrer2')

mai_mare = number1 if number1 > number2 else number2
print(mai_mare)
