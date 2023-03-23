def dynamic_where(conditions):
    temp = []
    for key in conditions:
        temp.append(key + ' = ?')
    
    return " WHERE " + ' AND '.join(temp)


def dynamic_columns(columns):
    return ', '.join(columns)

def dynamic_set(dictionary_keys):
    temp = []
    for key in dictionary_keys:
        temp.append(key + ' = ?')

    return ', '.join(temp)

def dynamic_values(values):
    temp = []
    for value in values:
        temp.append('?')
    
    return '(' + ', '.join(temp) + ')'
