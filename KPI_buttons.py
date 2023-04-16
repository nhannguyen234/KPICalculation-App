from tkinter import *
from tkinter import filedialog
from KPI_function import *


def calculate_button_fn():
    sim_paths_str = sim_paths.get()
    meas_path_str = mea_path.get()
    KPI2_fn(meas_path_str, sim_paths_str, saved_path.get(), int(initial_val.get()), int(end_val.get()))

def set_dir(sourcePath):
    try:
        return os.path.dirname(os.path.abspath(sourcePath))
    except:
        return sourcePath

def browse(window, option):
    global branch_result
    try:
        initial_dir = branch_mea
    except:
        try:
            initial_dir = branch_result
        except:
            try:
                initial_dir = branch_sim
            except:
                initial_dir = '/'
    window.filename = filedialog.askdirectory(initialdir=initial_dir,
                                               title='Select a folder')
    globals()['path_' + option].set(window.filename)
    branch_result = set_dir(globals()['path_' + option])

def browse_mea_files(window):
    global branch_mea
    try:
        initial_dir = branch_mea
    except:
        try:
            initial_dir = branch_result
        except:
            try:
                initial_dir = branch_sim
            except:
                initial_dir = '/'
    window.filename = filedialog.askopenfilename(initialdir=initial_dir, 
                                                 filetypes=(('csv file', '*.csv'),('all files','*.*')), 
                                                 title='Select a measurement file')
    path_mea.set(window.filename)
    branch_mea = set_dir(path_mea.get())

def browse_sim_files(window):
    global branch_sim
    try:
        initial_dir = branch_mea
    except:
        try:
            initial_dir = branch_result
        except:
            try:
                initial_dir = branch_sim
            except:
                initial_dir = '/'
    window.files = filedialog.askopenfilenames(initialdir=initial_dir, 
                                               filetypes=(('csv file', '*.csv'),('all files','*.*')), 
                                               title='Select simulation files')
    paths_sim.set(window.files)
    branch_sim = set_dir(paths_sim.get().split(' ')[0])


def KPI1():
    top=Toplevel()
    top.title('KPI1 Calculation')

    strsimpath = StringVar()
    strmeapath = StringVar()

    Label(top, text='Measurement file path').pack()
    meapath = Entry(top, justify='left', textvariable=strmeapath).pack()

    Label(top, text='Simulation file path').pack()
    simpath = Entry(top, justify='left', textvariable=strsimpath).pack()

def KPI2():
    top = Toplevel()
    top.title('KPI2 Calculation v1.0-beta')
    top.iconbitmap('kpi.ico')
    frame = Frame(top, relief='sunken')
    frame.pack()
    #specific frequency
    specific_f = LabelFrame(frame, text='Place your frequency range', font=('Arial Bolt',12))
    specific_f.grid(row=0, column=0, sticky='news', padx=5, pady=10)

    global initial_val, end_val, initial_default, end_default
    initial_default = IntVar(value=100)
    end_default = IntVar(value=2000)
    initial_val = Entry(specific_f, textvariable=initial_default)
    end_val = Entry(specific_f, textvariable=end_default)
    initial_val.grid(row=0, column=1, padx=5, pady=2)
    end_val.grid(row=1, column=1, padx=5, pady=2)

    initial_f = Label(specific_f, text='Initial frequency (default 100Hz)')
    end_f = Label(specific_f, text='End frequency (default 2000Hz)')
    initial_f.grid(row=0, column=0, padx=5, pady=5)
    end_f.grid(row=1, column=0, padx=5, pady=5)
    #insert path
    path_label = LabelFrame(frame, text='Insert your path', font=('Arial Bolt',12))
    path_label.grid(row=1, column=0, sticky='news', padx=5, pady=10)
    #label
    mea_label = Label(path_label, text='MEASUREMENT (*.csv file) (only 1 file)')
    sim_label = Label(path_label, text='SIMULATION (*.csv files) (1 and more files)')
    mea_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
    sim_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
    #path
    global mea_path, sim_paths, path_mea, paths_sim
    path_mea = StringVar()
    paths_sim = StringVar()
    mea_path = Entry(path_label, width=40, textvariable=path_mea)
    sim_paths = Entry(path_label, width=40, textvariable=paths_sim)
    mea_path.grid(row=1, column=0, padx=5, pady=2)
    sim_paths.grid(row=3, column=0, padx=5, pady=2)
    #browse for adding processing path
    mea_browse = Button(path_label, 
                        text='Browse',
                        width=8, 
                        command=lambda window=top: browse_mea_files(window))
    sim_browse = Button(path_label, 
                        text='Browse',
                        width=8, 
                        command=lambda window=top: browse_sim_files(window))
    mea_browse.grid(row=1, column=1, sticky='W', padx=5, pady=2)
    sim_browse.grid(row=3, column=1, sticky='W', padx=5, pady=2)
    
    #Saved folder and file name
    global saved_path, path_saved_folder
    savepath_label = LabelFrame(frame, text='Saved folder path', font=('Arial Bolt',12))
    savepath_label.grid(row=2, column=0, sticky='news', padx=5, pady=10)

    path_saved_folder = StringVar()
    saved_path = Entry(savepath_label, textvariable=path_saved_folder, width=40)
    saved_path.grid(row=1, column=1, padx=5, pady=2)
    
    saved_browse = Button(savepath_label, 
                          text='Browse', 
                          width=8,
                          command=lambda window=top, option = 'saved_folder': browse(window, option))
    saved_browse.grid(row=1, column=2, sticky='W', padx=5, pady=2)

    #Convert button
    convert_button = Button(frame, text='Calculate', command=calculate_button_fn, font=('Arial Bolt',14))
    convert_button.grid(row=3, sticky='news', padx=5, pady=10)

def KPI3():
    top = Toplevel()
    top.title('KPI3 Calculation')
    my_label = Label(top, text='Hello guys')
    my_label.pack()


