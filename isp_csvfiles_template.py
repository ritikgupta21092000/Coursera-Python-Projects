"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv


def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Ouput:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    with open(filename, "r", newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,
                                    delimiter=separator,
                                    quotechar=quote)
        return csv_reader.fieldnames


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    answer = []
    with open(filename, "r", newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,
                                    delimiter=separator,
                                    quotechar=quote)
        for row in csv_reader:
            answer.append(row)
    return answer


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    my_dict = {}
    with open(filename, "r", newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,
                                    delimiter=separator,
                                    quotechar=quote)
        for row in csv_reader:
            my_dict[row[keyfield]] = row
        return my_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    """
    with open(filename, "w", newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames,
                                    delimiter=separator,
                                    quotechar=quote,
                                    quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writeheader()
        for row in table:
            csv_writer.writerow(row)
            print(type(row.values()))


# table1 = read_csv_as_list_dict("table1.csv", ',', '"')
# print(table1)
# fieldnames1 = read_csv_fieldnames("table1.csv", ',', '"')
# write_csv_from_list_dict("output.csv", table1, fieldnames1, ',', '"')
# print(read_csv_as_nested_dict("table1.csv", "Field1", ',', '"'))
print(read_csv_fieldnames("table1.csv", ',', '"'))
