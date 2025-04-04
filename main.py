import consolemenu as cm


choice1 = "Convert Electrical Utility Data (Pacific Power)"
choice2 = "Convert Temperature Data (NOAA)"
choice3 = "Retrieve Solar Energy Data"
choices = [choice2, choice1, choice3]
menu = cm.SelectionMenu(choices)

tfname = "go"
while tfname != "stop":
    menu.show()
    selection = menu.selected_item.text
    if selection == choice1:
        tfname = 'NormPacificPower.py'
    elif selection == choice2:
        tfname = 'Temperature.py'
    elif selection == choice3:
        tfname = 'SolarMonitor.py'
    else:
        tfname = 'stop'
    if tfname != 'stop':
        with open(tfname, mode="r") as subfile:
            exec(subfile.read())
