import threading
from tkinter import Tk, ttk, StringVar, IntVar # import StringVar for 'textvariable' in Combobox, IntVar for Checkbox
from pycaw.pycaw import AudioUtilities as AU, ISimpleAudioVolume
# if error pip install pycaw

# some helpful Windows Developer documentation:
# https://docs.microsoft.com/en-us/windows/win32/coreaudio/session-volume-controls

window = Tk() # construct GUI
window.title("Volumax")
window.geometry("640x40")
window.resizable(False, False)
 
def main() -> tuple:
    """Retrieve or adjust volume of running processes that are accessing audio out

    Returns:
        tuple: names of running processes capable of producing audio
    """
    t = threading.Timer(10.0, main) # create thread
    t.daemon = True
    t.start()
    # retrieve running processes
    active_processes = AU.GetAllSessions()
    names = [] # function returns this list converted to a tuple, holds names of running processes
    for process in active_processes:
        volume = process._ctl.QueryInterface(ISimpleAudioVolume)
        if checkbox.get() == 1:
            volume.SetMasterVolume(1, None)
        elif process.Process and process.Process.name() == process_list.get():
            volume.SetMasterVolume(1, None)
        try:
            names.append(process.Process.name())
        except AttributeError: # prevent "NoneType"
            continue
    return tuple(names)
    
# creating combobox to show all running processes to user
combobox = StringVar(window)
checkbox = IntVar(window)
select_process = ttk.Label(window, text="Select process: ") # create label
process_list = ttk.Combobox(window, width=60, textvariable=combobox) # initialize combobox
process_list["values"] = main() # add combobox values (pull running processes from 'main()')
button_processes = ttk.Button(window, text="Action", command=main)
auto_max_checkbox = ttk.Checkbutton(window, variable=checkbox, onvalue=1, offvalue=0, text="Auto-Max", command=main)

select_process.grid(column=0, row=0, pady=(10, 10), sticky='E')
process_list.grid(column=1, row=0, pady=(10, 10))
button_processes.grid(column=2, row=0, padx=(10, 0), pady=(10, 10))
auto_max_checkbox.grid(column=3, row=0, padx=(5, 0), pady=(10, 10))

if __name__ == "__main__":
    window.mainloop() # initialize GUI
    main()