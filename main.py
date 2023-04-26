# Выполнение основной логики программы: генерация данных, выполнение сортировок,
# подсчет времени, запись результатов и вывод результируещего графика

import copy
import timeit
import pandas as pd
from collections import defaultdict

import matplotlib.pyplot as plt


from Brak import Brak
from Generation import generation

from Find_a import merge_sort
from Find_a import simple_search
from Find_a import binary_search

# Задание величины генерируемых массивов
size = [100, 200, 300, 400, 500]

# Генерация браков (объектов типа Brak.py) и запись в файл Marrigies.xlsx
with pd.ExcelWriter("./Marrigies.xlsx") as writer:
    for i in size:
        pd.DataFrame(generation(i)).to_excel(writer, sheet_name=f"{i}", index=False)

marrigies = {}
for i in size:
    c = pd.read_excel('./Marrigies.xlsx', sheet_name=f'{i}').to_dict('records')
    marrige = []
    for empl in c:
        marrige.append(
            Brak(empl['ФИО_жениха'], empl['Д/р_жениха'], empl['ФИО_невесты'], empl['Д/р_невесты'], empl['Дата_брака'],
                 empl['ЗАГС'])
        )
    marrigies[i] = marrige

# массивы с временем поиска
time_simple = []
time_binary = []
time_binary_sort = []
time_key = []


""" сортировка данных, считанных из файла .xlsx"""
for j in size:
    names = [k.fio_hus for k in marrigies[j]]
    key = Brak('Виталий Борисович Нижнин', '06/07/1997', 'Марина Викторовна Адаховская', '24/02/1996', '13/03/2022', 1)
    # Поиск по ключу в массиве
    marrigie_multi_map = defaultdict(list)
    for marrigie in marrigies[j]:
        marrigie_multi_map[marrigie.fio_hus].append(marrigie)
    start1 = timeit.default_timer()
    print([(i.fio_hus, i.bd_hus, i.fio_wife, i.bd_wife, i.mar_date, i.num_zags) for i in marrigie_multi_map[key.fio_hus]])
    end1 = timeit.default_timer() - start1
    time_key.append(end1)
    # Простой поиск
    start2 = timeit.default_timer()
    simple_search(marrigies[j], key)
    end2 = timeit.default_timer() - start2
    time_simple.append(end2)

    # Бинарный поиск с сортировкой
    start3 = timeit.default_timer()
    merge_sort(marrigies[j], 0, len(marrigies[j]) - 1)
    binary_search(marrigies[j], 0, len(marrigies[j]), key)
    end3 = timeit.default_timer() - start3
    time_binary_sort.append(end3)

    """Бинарный поиск"""
    start4 = timeit.default_timer()
    binary_search(marrigies[j], 0, len(marrigies[j]), key)
    end4 = timeit.default_timer() - start4
    time_binary.append(end4)

print(f'time_simple = {time_simple}')
print(f'time_binary = {time_binary}')
print(f'time_binary_sort = {time_binary_sort}')
print(f'time_key = {time_key}')

x1 = [i*100 for i in time_simple]
x2 = [i*100 for i in time_binary]
x3 = [i*100 for i in time_binary_sort]

plt.style.use('ggplot')
plt.title('График времени сортировки')
plt.ylabel('Время умноженное на 100', color='gray')
plt.text(0.01, 0.105, 'Red line - simple search')
#plt.text(0.01, 0.105, '- simple search')

plt.text(0.01, 0.095, 'Green line - binary search')
#plt.text(0.01, 0.09, '- binary search')

plt.text(0.01, 0.085, 'Blue line - binary sort search')
#plt.text(0.01, 0.08, '- binary sort search')
x = [i/10 for i in range(len(size))]
plt.plot(x, x1, 'r-', x, x2, 'g-', x, x3, 'b-')
plt.show()
