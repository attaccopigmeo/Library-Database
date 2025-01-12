import pandas as pd


# Функция сравнения, возвращает True, если пара книг имеет правильный порядок по ключу из пункта 1
def compare_key1(book1, book2):
    author1, year1, cnt1 = book1['author'], book1['release_year'], book1['copies_amount']
    author2, year2, cnt2 = book2['author'], book2['release_year'], book2['copies_amount']
    # Сравниваем по авторам
    if author1 < author2:
        return True
    elif author1 > author2:
        return False
    # Если авторы одинаковы, сравниваем по годам
    elif year1 > year2:
        return True
    elif year1 < year2:
        return False
    # Если годы равны, сравниваем по количествам экземпляров
    elif cnt1 > cnt2:
        return True
    else:
        return False


# Функция сравнения, возвращает True, если пара книг имеет правильный порядок по ключу из пункта 2
def compare_key2(book1, book2):
    pub1, name1 = book1['publisher'], book1['name']
    pub2, name2 = book2['publisher'], book2['name']
    # Сравниваем по издателям
    if pub1 > pub2:
        return True
    elif pub1 < pub2:
        return False
    # Если издатели одинаковы, сравниваем по названиям
    elif name1 < name2:
        return True
    else:
        return False


# Функция сравнения, возвращает True, если пара книг имеет правильный порядок по ключу из пункта 3
def compare_key3(book1, book2):
    year1, author1 = book1['release_year'], book1['author']
    year2, author2 = book2['release_year'], book2['author']
    # Сравниваем по годам
    if year1 > year2:
        return True
    elif year1 < year2:
        return False
    # Если годы одинаковы, сравниваем по авторам
    elif author1 < author2:
        return True
    else:
        return False


# comparator - функция, возвращающая True,
# если пара книг в правильном порядке по требуемому ключу

def heapify(arr, n, i, comparator): # Ф-ция для преобразования поддерева в кучу
    # arr - массив
    # n - размер массива
    # i - индекс текущего узла
    largest = i  # Изначально считаем, что корень — наибольший
    left = 2 * i + 1  # Левый потомок
    right = 2 * i + 2  # Правый потомок

    # Если левый потомок больше корня
    if left < n and not comparator(arr[left], arr[largest]):
        largest = left

    # Если правый потомок больше "самого большого" на текущий момент
    if right < n and not comparator(arr[right], arr[largest]):
        largest = right

    # Если "самый большой" изменился, меняем местами и продолжаем
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Рекурсивно перестраиваем затронутое поддерево
        heapify(arr, n, largest, comparator)


def heap_sort(arr, comparator): # Основная ф-ция пирамидальной сортировки

    n = len(arr)

    # Построение кучи (преобразование массива в кучу)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, comparator)

    # Извлечение элементов из кучи по одному
    for i in range(n - 1, 0, -1):
        # Меняем корень (максимум) с последним элементом
        arr[i], arr[0] = arr[0], arr[i]
        # Вызываем heapify на уменьшенной куче
        heapify(arr, i, 0, comparator)


library = []
f = open('library.csv', 'r')
f.readline() # Пропускаем строку с заголовками
for record in f:
    author,name,publisher,release_year,pages_number,copies_amount = record.split(',')
    book = {
        'author': author,
        'name': name,
        'publisher': publisher,
        'release_year': int(release_year),
        'pages_number': int(pages_number),
        'copies_amount': int(copies_amount)
    }
    library.append(book)

print("Программа считывает исходную информацию из файла и позволяет на основе неё создавать следующие отчёты:")
print("1) Полный список всех книг, который будет отсортирован по следующему ключу: автор (по возрастанию) + год выпуска (по убыванию) + количество экземпляров (по убыванию);")
print("2) Список всех книг определённого автора, отсортированный по следующему ключу: издательство (по убыванию) + название (по возрастанию);")
print("3) Список всех книг, выпущенных в период с N1 до N2 года, отсортированный по следующему ключу: год выпуска (по убыванию) + автор (по возрастанию).")
print("\n")
choice = int(input('Введите номер варианта отчёта (одна цифра от 1 до 3): '))
comparator = None
while True:
    match choice:
        case 1:
            comparator = compare_key1
        case 2:
            comparator = compare_key2
            # Выбираем книги определённого автора
            author = input("Введите фамилию автора: ")
            library = list(filter(lambda x: x['author'].lower() == author.lower(), library))
            if len(library) == 0:
                print("Данного автора нет в библиотеке, попробуйте снова.")
                continue
        case 3:
            comparator = compare_key3
            first_year = int(input("Введите начальный год: "))
            last_year = int(input("Введите конечный год: "))
            library = list(filter(
                lambda x: first_year <= x['release_year'] and x['release_year'] <= last_year,
                library
            ))
            if len(library) == 0:
                print("Книг, изданных в эти годы нет в библиотеке, попробуйте снова.")
                continue
        case _:
            print("Неправильный номер отчёта! Введите номер отчета снова.")
            continue
        

    heap_sort(library, comparator)

    df = pd.DataFrame(library)
    if len(library) == 0:
        df = pd.DataFrame(columns = ['Автор', 'Название', 'Издатель', 'Год издания', 'Количество страниц', 'Количество экземпляров'])
    else:
        df.columns = ['Автор', 'Название', 'Издатель', 'Год издания', 'Количество страниц', 'Количество экземпляров']
    print(df)
    answer = input("Хотите ли Вы снова выбрать отчет? (y/n)")
    if answer == "n":
        break