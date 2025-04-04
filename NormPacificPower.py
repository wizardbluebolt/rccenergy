import csv
import os
import base
import constantsPacificPower


ppxref = {}
tXRef = base.BASE_DIR + constantsPacificPower.INPUT_FOLDER + constantsPacificPower.XREF_FILENAME
with open(tXRef, mode="r") as xref_file:
    xref_lines = 0
    csv_reader = csv.reader(xref_file)
    for row in csv_reader:
        if xref_lines > 0:
            xref_entry = {"account": row[0], "meter": row[1], "campus": row[2], "location": row[3]}
            ppxref[xref_entry["account"]] = xref_entry
        xref_lines += 1
    print("Read " + str(xref_lines) + " cross-reference entries")
tOutFilename = base.BASE_DIR + constantsPacificPower.OUTPUT_FOLDER + constantsPacificPower.OUTPUT_FILENAME
with open(tOutFilename, mode="w", newline="") as out_file:
    output_lines = 0
    all_input = 0
    csv_writer = csv.writer(out_file)
    tInputFolder = base.BASE_DIR + constantsPacificPower.INPUT_FOLDER
    for file in os.listdir(tInputFolder):
        filename = os.fsdecode(file)
        print("Processing file " + filename)
        nameparts = filename.split(".")
        account = nameparts[0]
        xref_entry = ppxref[account]
        with open(tInputFolder + filename, mode="r") as in_file:
            csv_reader = csv.reader(in_file)
            input_lines = 0
            for row in csv_reader:
                if input_lines > 0:
                    month_year = row[0]
                    units = row[1]
                    cost = row[len(row) - 1].replace("$", "").replace(",", "").replace("\n", "")
                    month_year_parts = month_year.replace("-", " ").split(" ")
                    month_name = month_year_parts[0]
                    year = month_year_parts[1]
                    month = constantsPacificPower.MONTHS.index(month_name) + 1
                    date = str(month) + "/1/" + year
                    csv_writer.writerow([xref_entry["campus"], xref_entry["location"],
                                         "Elec", date, "", units, cost])
                    output_lines += 1
                input_lines += 1
        all_input += input_lines
print("Read " + str(all_input) + " data lines")
print("Wrote " + str(output_lines) + " data lines")
