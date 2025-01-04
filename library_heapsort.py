import pandas as pd
import numpy as np


def heapify(arr, n, i): # Ф-ция для преобразования поддерева в кучу
    # arr - массив
    # n - размер массива
    # i - индекс текущего узла
    largest = i  # Изначально считаем, что корень — наибольший
    left = 2 * i + 1  # Левый потомок
    right = 2 * i + 2  # Правый потомок

    # Если левый потомок больше корня
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Если правый потомок больше "самого большого" на текущий момент
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Если "самый большой" изменился, меняем местами и продолжаем
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Рекурсивно перестраиваем затронутое поддерево
        heapify(arr, n, largest)


def heap_sort(arr): # Основная ф-ция пирамидальной сортировки

    n = len(arr)

    # Построение кучи (преобразование массива в кучу)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Извлечение элементов из кучи по одному
    for i in range(n - 1, 0, -1):
        # Меняем корень (максимум) с последним элементом
        arr[i], arr[0] = arr[0], arr[i]
        # Вызываем heapify на уменьшенной куче
        heapify(arr, i, 0)