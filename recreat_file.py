import csv

import cassandra_config

from models import Row, Cell



def sort_by_position(row):
    return int(row.position)

cassandra_config.init()


file_md5 = '4cbfb1a3141c66c60bef9e495183bf44'
def write_file(delimiter=','):
    rows = Row.objects.filter(document_md5=file_md5).allow_filtering()
    rows = sorted(rows, key=sort_by_position)
    print(len(rows))
    header_fields = set()

    def gen_rows():
        counter = 0
        for row in rows:
            print(f'#{counter+1}')
            cells = Cell.objects.filter(row_id=row.id).allow_filtering()
            row_dict = {}
            for cell in cells:
                if counter == 0:
                    header_fields.add(cell.cell_name)
                row_dict[cell.cell_name] = cell.cell_content

            yield row_dict
            counter += 1

    with open(f'{file_md5}.csv', 'w') as _f:
        csv_writer = csv.DictWriter(
            _f,
            fieldnames=header_fields,
            delimiter=delimiter
        )

        data = gen_rows()
        first_row = None
        try:
            first_row = next(data)
        except StopIteration:
            return

        csv_writer.writeheader()
        csv_writer.writerow(first_row)
        csv_writer.writerows(data)



write_file()
