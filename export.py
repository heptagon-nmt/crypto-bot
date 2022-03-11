"""
Used to export data to different formats.
"""
import csv

def export_csv(data: dict[str, list[float]], filename: str = "data/data_out.csv") -> None:
    """
    Exports data as a CSV file.
    :arg data: A colection of predictions from the ml unit, with prediction
    types as keys.
    :arg filename: The name of the file to save to within data/
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

