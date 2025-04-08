import consolemenu as cm
import Temperature
import SolarMonitor
import NormPacificPower


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
        NormPacificPower.execute()
    elif selection == choice2:
        Temperature.execute()
    elif selection == choice3:
        SolarMonitor.execute()
    else:
        tfname = 'stop'
