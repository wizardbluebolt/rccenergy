import csv
import os
import datetime
import GetBase
import baseTemperature
import constantsTemperature


def get_year_month(p_date_string):
    date_parts = p_date_string.split("/")
    tdate = date_parts[0] + "/1/" + date_parts[2]
    return tdate


def execute():
    nl = "\n"
    tempBase = GetBase.getbase() + baseTemperature.TEMPERATURE_BASE
    outfolder = tempBase + constantsTemperature.OUTPUT_FOLDER
    infolder = tempBase + constantsTemperature.INPUT_FOLDER
    now = datetime.datetime.now()
    fnamenow = now.strftime("%Y-%m-%d T %H%M%S")
    logfname = tempBase + constantsTemperature.LOG_FOLDER + "Temperature Log " + fnamenow + ".txt"
    print("Processing temperature data now.  Log file " + logfname)
    with open(logfname, mode="w") as log_file:
        output_lines = 0
        all_input = 0
        for file in os.listdir(infolder):
            infilename = os.fsdecode(file)
            log_file.write("Processing input file " + infilename + nl)
            with open(infolder + infilename, mode="r") as in_file:
                input_lines = 0
                csv_reader = csv.reader(in_file)
                temp_dict = {}
                for row in csv_reader:
                    input_lines += 1
                    if input_lines == 1:
                        # Skip header row
                        continue
                    t_station = constantsTemperature.STATIONS[row[0]]
                    if t_station not in temp_dict:
                        temp_dict[t_station] = {}
                    t_year_month = get_year_month(row[2])
                    if t_year_month not in temp_dict[t_station]:
                        temp_dict[t_station][t_year_month] = {'avg': 0, 'days': 0, 'max': 0, 'min': 999}
                    # Provide estimate for daily average temperature if it is missing from the data set
                    t_max = int(row[4])
                    t_min = int(row[5])
                    if len(row[3]) == 0:
                        t_avg = (t_max + t_min) / 2
                    else:
                        t_avg = int(row[3])
                    t_entry = temp_dict[t_station][t_year_month]
                    t_entry['avg'] += t_avg
                    t_entry['days'] += 1
                    if t_max > t_entry['max']:
                        t_entry['max'] = t_max
                    if t_min < t_entry['min']:
                        t_entry['min'] = t_min
                all_input += input_lines
            for t_station in temp_dict.keys():
                outfilename = infilename[ : -4] + " " + t_station + ".csv"
                with open(outfolder + outfilename, mode="w", newline='') as out_file:
                    csv_writer = csv.writer(out_file, )
                    csv_writer.writerow(["yearmonth", "temphigh", "templow", "tempavg"])
                    for yearmonth, entry in temp_dict[t_station].items():
                        t_avg = int((entry['avg'] / entry['days']) + 0.5)  # Ensure result is rounded
                        csv_writer.writerow([yearmonth, entry['max'], entry['min'], t_avg])
                        output_lines += 1
            log_file.write("Processing of file completed.  " + str(output_lines) + " data lines written." + nl)
