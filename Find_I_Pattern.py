arr = [
[1, 0, 1, 2, 2, 2, 1, 0, 3],
[0, 0, 3, 1, 4, 6, 1, 2, 4],
[5, 6, 1, 10, 3, 1, 2, 7, 3],
[1, 0, 5, 6, 11, 0, 0, 0, 3],
[1, 0, 1, 2, 2, 2, 1, 0, 3],
[6, 2, 1, 5, 1, 1, 7, 1, 3],
[3, 2, 2, 2, 1, 6, 8, 2, 3],
[1, 5, 2, 2, 2, 2, 1, 0, 3],
[1, 0, 5, 2, 1, 7, 8, 2, 2]
]
# Output:
# Sum = 40

# arr = [
# [1, 0, 1, 2, 2, 2, 1, 0, 3],
# [0, 0, X, X, X, 6, 1, 2, 4],
# [5, 6, 1, X, 3, 1, 2, 7, 3],
# [1, 0, X, X, X, 0, 0, 0, 3],
# [1, 0, 1, 2, 2, 2, 1, 0, 3],
# [6, 2, 1, 5, 1, 1, 7, 1, 3],
# [3, 2, 2, 2, 1, 6, 8, 2, 3],
# [1, 5, 2, 2, 2, 2, 1, 0, 3],
# [1, 0, 5, 2, 1, 7, 8, 2, 2]



def find_patterns(arr):
    final_result_list = []
    max_sum = 0
    for i in range(1,len(arr) -1):
                for j in range(1, len(arr[0])-1):
                            try:
                                first_row = [arr[i-1][j-1],arr[i-1][j],arr[i-1][j + 1]]
                                mid = arr[i][j]
                                last_row = [arr[i+1][j-1], arr[i+1][j], arr[i+1][j+1]]

                                sum_of_rows = sum(first_row) +mid + sum(last_row)
                                if sum_of_rows > max_sum:
                                    max_sum = sum_of_rows
                                    temp_result = [row.copy() for row in arr]
                                    temp_result[i-1][j-1]=temp_result[i-1][j]=temp_result[i-1][j + 1]=temp_result[i][j]=temp_result[i+1][j-1]=temp_result[i+1][j]=temp_result[i+1][j+1]='X'
                                    final_result_list = temp_result
                            except Exception as exe:
                                        continue
                
    print("sum",max_sum)
    for row in final_result_list:
           print(row)
           
find_patterns(arr)
