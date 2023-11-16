from typing import List

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

