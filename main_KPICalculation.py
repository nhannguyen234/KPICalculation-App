"""
Created by Nguyen Le Nhan PS/EVI-VN
Updated date: 30 March 2023
"""
from tkinter import *
from tkinter import messagebox, ttk
from data_processing import *
from KPI_buttons import *
import json


json_path = 'layout.json'
layout_info = json.load(open(json_path))

div = layout_info['window'][0]['main']['div']
measurement_canvas = div[0]['measurement']
simulation_canvas = div[1]['simulation']
convert_btn_canvas = div[2]['convert_button']


window = Tk()
window.title('VVV-KPI Calculation-v0.5')
window.iconbitmap('kpi.ico')
frame = Frame(window, relief='sunken')
frame.pack()

#Data Conversion
data_conversion = LabelFrame(frame, text='Data conversion v0.5', font=('Arial Bolt',14))
data_conversion.grid(row=1, column=0, sticky='news',padx=20, pady=10)

#Canvas widget
top_canvas = Canvas(data_conversion, borderwidth=0)
top_canvas.pack(side='top', fill='x', padx=5, pady=5)
bottom_canvas = Canvas(data_conversion, borderwidth=0)
bottom_canvas.pack(side='bottom', fill='x', padx=5, pady=5)

canvas_mea = Canvas(globals()[measurement_canvas['canvas']], borderwidth=2)
canvas_mea.pack(side=measurement_canvas['side'], 
                fill=measurement_canvas['fill'], 
                padx=5, pady=5)

canvas_sim = Canvas(globals()[simulation_canvas['canvas']], borderwidth=2)
canvas_sim.pack(side=simulation_canvas['side'], 
                fill=simulation_canvas['fill'], 
                padx=5, pady=5)


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
    window.filename = filedialog.askopenfilenames(initialdir=initial_dir,
                                                  filetypes=(('xlsx file', '*.xlsx'),('all files','*.*')), 
                                                  title='Select measurement files')
    paths_mea.set(window.filename)
    branch_mea = set_dir(paths_mea.get().split(' ')[0])

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
                                               filetypes=(('xlsx file', '*.xlsx'),('all files','*.*')), 
                                               title='Select simulation files')
    paths_sim.set(window.files)
    branch_sim = set_dir(paths_sim.get().split(' ')[0])


def naccheck(entry, 
            browse, 
            type_data,
            name_measurement_file,
            var):
    # print(var.get())
    list_toggle = ['magnitude', 'real', 'imaginary','select_all_option',
                    'XX', 'YX', 'XZ', 'XY', 'YY', 'ZY','ZX', 'YZ', 'ZZ',
                    'select_all_option_dir','merge_checkbox']
    if type_data == 'meas':
        if var.get() == 0:
            name_measurement_file.config(state='disabled')
            for option in list_toggle:
                globals()[option].config(state='disabled')
        else:
            name_measurement_file.config(state='normal')
            for option in list_toggle:
                globals()[option].config(state='normal')
    else:
        pass

    if var.get() == 0:
        entry.config(state='disabled')
        browse.config(state='disabled')
    else:
        entry.config(state='normal')
        browse.config(state='normal')

#Create a new window to extract selected directions
def dirs_name_option():
    global dir_selected, \
            check_var_all_dir,\
            count_check_dir,\
            select_all_option_dir
    count_check_dir=0
    dir_selected=[]
    dir_name_list = [['XX', 'YX', 'ZX'],['XY','YY','ZY'],['XZ','YZ','ZZ']]

    def select_all(dir_names, 
                    check_var):
        global count_check_dir
        if check_var.get()!=0:
            for i in range(len(dir_names)):
                for j in range(len(dir_names[i])):
                    globals()[dir_names[i][j]].select()
                    dir_selected.append(dir_names[i][j])
            #returnn to full options if select all toogle is on
            count_check_dir = len(dir_name_list[0])*len(dir_name_list)
        else:
            for i in range(len(dir_names)):
                for j in range(len(dir_names[i])):
                    globals()[dir_names[i][j]].deselect()
                    dir_selected.clear()
            #return to 0 if select all toogle is off
            count_check_dir=0
        #show error message
        if dir_selected ==[]:
            messagebox.showerror(title='Error', message='Please choose at least 1 direction')

    def check_btn(dir_name, 
                    check_var):
        global check_var_all_dir, count_check_dir
        if check_var.get()!=0:
            dir_selected.append(dir_name)
            count_check_dir+=1
            if count_check_dir == len(dir_name_list[0])*len(dir_name_list):
                check_var_all_dir.set(1)
        else:
            dir_selected.remove(dir_name)
            if dir_selected != dir_name_list:
                count_check_dir-=1
                check_var_all_dir.set(0) 
        #show error message
        if dir_selected ==[]:
            messagebox.showerror(title='Error', message='Please choose at least 1 direction')

    for i in range(len(dir_name_list)):
        for j in range(len(dir_name_list[i])):
            globals()['op_check_'+dir_name_list[i][j]] = IntVar()
            globals()[dir_name_list[i][j]] = Checkbutton(direction_choose_frame,
                                                        text=dir_name_list[i][j], 
                                                        variable=globals()['op_check_'+dir_name_list[i][j]],
                                                        command= lambda dir_name = dir_name_list[i][j], 
                                                                        check_var=globals()['op_check_'+dir_name_list[i][j]]: check_btn(dir_name, 
                                                                                                                                        check_var))
            globals()[dir_name_list[i][j]].grid(row=j+measurement_canvas['frame_direction_choose']['toggle_retained_initiate']['row'], 
                                                column=i, 
                                                sticky=measurement_canvas['frame_direction_choose']['toggle_retained_initiate']['sticky'], 
                                                pady=5, padx=5)

    check_var_all_dir = IntVar()
    select_all_option_dir = Checkbutton(direction_choose_frame, text='Select all', 
                                    variable=check_var_all_dir,
                                    command= lambda dir_names = dir_name_list, 
                                                    check_var = check_var_all_dir: select_all(dir_names, 
                                                                                                check_var))
    select_all_option_dir.grid(row=measurement_canvas['frame_direction_choose']['toggle_select_all']['row'], 
                                column=i+measurement_canvas['frame_direction_choose']['toggle_select_all']['column'], 
                                sticky=measurement_canvas['frame_direction_choose']['sticky'], 
                                pady=5, padx=5)
   

#Create a frame to extract complex components
def complex_component_option():
    global complex_selected,\
            check_var_all,\
            count_check,\
            magnitude, real, imaginary,\
            merge_checkbox, merge_inp,\
            select_all_option
    count_check=0
    check_var_all = IntVar()
    complex_selected=[]
    complex_component_list = ['real','imaginary','magnitude']
    def select_all(complex_components, 
                check_var):
        global count_check
        if check_var.get()!=0:
            for i in range(len(complex_components)):
                globals()[complex_components[i]].select()
                complex_selected.append(complex_components[i])
            count_check = len(complex_component_list) 
        else:
            for i in range(len(complex_components)):
                globals()[complex_components[i]].deselect()
                complex_selected.clear()
            count_check=0
        #show error message
        if complex_selected ==[]:
            messagebox.showerror(title='Error', message='Please choose at least 1 complex component')

    def check_btn(complex_component,
                check_var):
        """Checkbutton function"""
        global count_check
        if check_var.get()!=0:
            complex_selected.append(complex_component)
            count_check+=1
            if count_check == len(complex_component_list):
                check_var_all.set(1)
        else:
            complex_selected.remove(complex_component)
            if complex_selected != complex_component_list:
                count_check-=1
                check_var_all.set(0)
        #show error message
        if complex_selected ==[]:
            messagebox.showerror(title='Error', message='Please choose at least 1 complex component')

    def merge_function(complex_component,
                    check_var):
        if check_var.get()!=0:
            check_var_all.set(1)
            select_all(complex_component, check_var_all)
            
    for i in range(len(complex_component_list)):
        globals()['op_check_'+complex_component_list[i]] = IntVar()
        globals()[complex_component_list[i]] = Checkbutton(complex_component_frame, 
                                                        text=complex_component_list[i], 
                                                        variable=globals()['op_check_'+complex_component_list[i]],
                                                        command= lambda complex_component = complex_component_list[i],
                                                                        check_var=globals()['op_check_'+complex_component_list[i]]: check_btn(complex_component,
                                                                                                                                                    check_var))
        globals()[complex_component_list[i]].grid(row=measurement_canvas['frame_complex_chosen']['toggle']['row'], 
                                                column=i, 
                                                sticky='w', 
                                                pady=5, padx=5)
    merge_inp = IntVar()
    merge_checkbox = Checkbutton(complex_component_frame, 
                                text='MERGE (merge all to one file)', 
                                variable=merge_inp,
                                command= lambda complex_component = complex_component_list,
                                                check_var = merge_inp : merge_function(complex_component, 
                                                                                        check_var))
    merge_checkbox.grid(row=measurement_canvas['frame_complex_chosen']['toggle_merge']['row'], 
                        columnspan=measurement_canvas['frame_complex_chosen']['toggle_merge']['columnspan']+len(complex_component_list), 
                        sticky=measurement_canvas['frame_complex_chosen']['toggle_merge']['sticky'], 
                        pady=5, padx=5)

    select_all_option = Checkbutton(complex_component_frame, 
                                    text='Select all', variable=check_var_all,
                                    command= lambda complex_components = complex_component_list, 
                                                    check_var = check_var_all: select_all(complex_components, 
                                                                                            check_var))
    select_all_option.grid(row=measurement_canvas['frame_complex_chosen']['toggle']['row'], 
                            column=len(complex_component_list)+1, 
                            sticky='w', 
                            pady=5, padx=5)
    

#Create a button to convert
def convert_button_fn():
    sim_path_str = sim_paths.get()
    meas_path_str = mea_paths.get()
    merge_inp_str = merge_inp.get()
    if sim_path_str != '':
        expand_data_SIM(sim_path_str)
    
    if meas_path_str != '':
        extract_TF_frommeas(merge_inp_str,
                            meas_path_str, 
                            name_measurement_file.get(), 
                            dir_selected,
                            complex_selected)

    
    messagebox.showinfo(title='Data conversion', message='Finish converting!!')

def KPI_checkbox(var, KPI_btn):
    if var.get()==0:
        KPI_btn.config(state='disabled')
    else:
        KPI_btn.config(state='normal')

#KPI calculation
KPI_buttons = LabelFrame(frame, text='KPI Calculation Function v1.0-beta', font=('Arial Bolt',14))
KPI_buttons.grid(row=0, column=0,padx=20, pady=20)
#KPI1 button is disabled
KPI1_button = Button(KPI_buttons, 
                     text='KPI1 Calculation',
                     width=13, 
                     command=KPI1, 
                     bg='cyan')
KPI1_button.grid(row=1, column=0, padx=10, pady=5)
KPI1_button.config(state='disabled')
#KPI2 button is enabled
KPI2_button = Button(KPI_buttons, 
                     text='KPI2 Calculation',
                     width=13, 
                     command=KPI2, 
                     bg='cyan')
KPI2_button.grid(row=1, column=1, padx=10, pady=5)
#KPI3 button is disabled
KPI3_button = Button(KPI_buttons, 
                     text='KPI3 Calculation',
                     width=13, 
                     command=KPI3, 
                     bg='cyan')
KPI3_button.grid(row=1, column=2, padx=10, pady=5)
KPI3_button.config(state='disabled')

#file browse
paths_mea = StringVar()
paths_sim = StringVar()
mea_paths = Entry(canvas_mea, 
                  width=measurement_canvas['entry_path']['width'], 
                  textvariable=paths_mea)
sim_paths = Entry(canvas_sim, 
                  width=simulation_canvas['entry_path']['width'], 
                  textvariable=paths_sim)
mea_paths.grid(row=measurement_canvas['entry_path']['row'],
                column=measurement_canvas['entry_path']['column'], 
                padx=5, pady=2)
sim_paths.grid(row=simulation_canvas['entry_path']['row'], 
                column=simulation_canvas['entry_path']['column'], 
                padx=5, pady=2)


#browse button for file path
mea_browse = Button(canvas_mea, 
                    text='Browse', 
                    width=measurement_canvas['button_browse']['width'], 
                    command=lambda window=window: browse_mea_files(window))
sim_browse = Button(canvas_sim, 
                    text='Browse', 
                    width=simulation_canvas['button_browse']['width'],
                    command=lambda window=window: browse_sim_files(window))
mea_browse.grid(row=measurement_canvas['button_browse']['row'],
                column=measurement_canvas['button_browse']['column'],
                sticky=measurement_canvas['button_browse']['sticky'],
                pady=2, padx=5)
sim_browse.grid(row=simulation_canvas['button_browse']['row'], 
                column=simulation_canvas['button_browse']['column'], 
                sticky=simulation_canvas['button_browse']['sticky'], 
                pady=2, padx=5)

#exporting complex component 
complex_component_frame = LabelFrame(canvas_mea, text='Choose complex component', borderwidth=1)
complex_component_frame.grid(row=measurement_canvas['frame_complex_chosen']['row'], 
                            columnspan=measurement_canvas['frame_complex_chosen']['columnspan'], 
                            sticky=measurement_canvas['frame_complex_chosen']['sticky'], 
                            padx=5, pady=5)
complex_component_option()


#project name
name_meas_frame = LabelFrame(canvas_mea, text='Project name (Choose the project name)', borderwidth=0)
name_meas_frame.grid(row=measurement_canvas['frame_project_naming']['row'], 
                    columnspan=measurement_canvas['frame_project_naming']['columnspan'],
                    sticky=measurement_canvas['frame_project_naming']['sticky'], 
                    padx=5, pady=5)
name_measurement_file = ttk.Combobox(name_meas_frame, 
                                    values=['PAG_LK3_Gosa'
                                            'PAG_LK3_C1', 
                                            'PAG_Taycan', 
                                            'Daimler_CV',
                                            'Daimler1_6_V2_B',
                                            'Daimler1_6_V4_B',
                                            'Daimler1_6_V4.1_B',
                                            'Daimler1_6_V2_C',
                                            'Daimler1_6_V4_C',
                                            'Daimler1_6_V4.1_C'],
                                    width=measurement_canvas['frame_project_naming']['combo_box']['width'])
name_measurement_file.grid(row=measurement_canvas['frame_project_naming']['combo_box']['row'], 
                            column=measurement_canvas['frame_project_naming']['combo_box']['column'], 
                            sticky=measurement_canvas['frame_project_naming']['combo_box']['sticky'], 
                            padx=5, pady=5)


##Create button to choose the direction
direction_choose_frame = LabelFrame(canvas_mea, text='Directions (Choose transferfunction directions)', borderwidth=0)
direction_choose_frame.grid(row=measurement_canvas['frame_direction_choose']['row'], 
                            columnspan=measurement_canvas['frame_direction_choose']['columnspan'], 
                            sticky=measurement_canvas['frame_direction_choose']['sticky'],
                            padx=5)
dirs_name_option()


##Check box
varmea = IntVar(value=1)
varsim = IntVar(value=1)
mea_canvas_status = Checkbutton(canvas_mea, text='MEASUREMENT FILES PATH', variable=varmea,
                            command=lambda e=mea_paths,
                                            b=mea_browse, 
                                            p=name_measurement_file,
                                            v=varmea: naccheck(e,b,'meas',p,v))
sim_canvas_status = Checkbutton(canvas_sim, text='SIMULATION FILES PATH', variable=varsim,
                            command=lambda e=sim_paths,
                                            b=sim_browse, 
                                            p=None, 
                                            v=varsim: naccheck(e,b,'sim',p,v))

mea_canvas_status.grid(row=measurement_canvas['toggle']['row'], 
                        column=measurement_canvas['toggle']['column'], 
                        sticky=measurement_canvas['toggle']['sticky'], pady=2)
sim_canvas_status.grid(row=simulation_canvas['toggle']['row'], 
                        column=simulation_canvas['toggle']['column'], 
                        sticky=simulation_canvas['toggle']['sticky'], pady=2)

#Convert button
convert_button = Button(globals() [convert_btn_canvas['canvas']], 
                        text='CONVERT', 
                        borderwidth=1, 
                        command=convert_button_fn, 
                        font=('Arial Bolt',14))
convert_button.pack(side=convert_btn_canvas['side'], 
                    fill=convert_btn_canvas['fill'], 
                    padx=5, pady=5)

window.mainloop()
