def find_division_index(arr):
    left = 0
    right = len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == 1 and arr[mid-1] == 0:
            result = mid
            break
        elif arr[mid] == 0:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

arr = list(map(int, input("Введите числа массива: ").split()))

division_index = find_division_index(arr)

if division_index != -1:
    print(f"Разделение на индексе {division_index}")
else:
    print("Разделения не найдено.")
