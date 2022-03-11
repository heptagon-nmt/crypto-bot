"""
Used to export data to diffrent formats.
"""
import csv

def export_csv(data: dict[str, list[float]],
        filename: str = "data_out.csv") -> None:
    """
    Exports data as a coma seperated file.
    :arg data: A colection of predicitons from the ml unit, with prediction
    types as keys.
    :arg filename: The name of the file to save to.
    """
    try:
        with open(filename, "w", newline='') as csv_file:
            tmp = csv.writer(csv_file, delimiter=" ",
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tmp.writerow(data.keys())
            tmp.writerows(data.values())
            print(f'Saved output as {filename}')
    except Exception as e:
        print(f'Could not write output file: {e}')

