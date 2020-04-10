def filter_row(row, condition):
    row *= condition
    
def set_on_index(matrix,index, value):
    matrix[index[0]][index[1]]= value
    
def matrix_on(matrix, index):
    return matrix[index[0]][index[1]]