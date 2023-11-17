from typing import List, Tuple

def get_unique_rows_at_given_col(column: str, data: List[dict]) -> List[dict]:
    seen_values = set()
    unique_rows = []

    for row in data:
        if row[column] and row[column] not in seen_values:
            seen_values.add(row[column])
            unique_rows.append(row)
    return unique_rows

def drop_cols(col_list: List[str], data: List[dict]) -> List[dict]:

    build_list = []

    for row in data: 
        new_row = {}
        for key, value in row.items():
            if key not in col_list:
                new_row[key] = value
        build_list.append(new_row)

    return build_list

def add_request_parameters(requestUrl: str, parameters: List[Tuple[str, str]]): 
    build_url = requestUrl
    for i, parameter in enumerate(parameters):
        if i == 0: build_url += "?"
        else: build_url += "&"

        param_name = parameter[0] 
        param_value = parameter[1]

        build_url += str(param_name) + "=" + str(param_value) 
    return build_url