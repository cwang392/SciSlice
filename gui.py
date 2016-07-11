# -*- coding: utf-8 -*-
'''
Created on Sat May 28 16:39:58 2016
@author: Alex Diebold
'''

import os
import constants as c
import matplotlib                   #for 3D model

#if using the Spyder console, matplotlib is already imported and the backend cannot be changed with .use() as is needed
#to change the backend to TkAgg, go to Tools > Preferences > Console > External modules > Matplotlib GUI backend
#be sure to mind the caps in TkAgg
'''
backend = matplotlib.get_backend()
if backend != 'TkAgg' and backend != 'module://ipykernel.pylab.backend_inline':
    matplotlib.use('TkAgg')             #backend of matplotlib, used for putting in GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
'''
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tkinter import *               #GUI module
from tkinter import ttk             #for styling purposing
from tkinter import filedialog      #window for saving and uploading files
import json                         #for saving and uploading files
from main import Main        #for converting to Gcode

class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        Tk.iconbitmap(self, 'UW_Madison_icon.ico')
        Tk.title(self, '3D Printer Parameter Setter')
        #format window size -- width=450, height=475, 100px from left of screen, 100px from top of screen
        #Tk.geometry(self, '450x475+100+100')
        
        #set up frame
        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid(row=0,column=0)
        
        #create menubar
#        menubar = Menu(container)
#        filemenu = Menu(menubar, tearoff=0)
#        filemenu.add_command(label='Save', command=lambda: Page_Variables.save(Page_Variables))
#        filemenu.add_command(label='Upload', command=lambda: Page_Variables.upload(Page_Variables))
#        menubar.add_cascade(label='File', menu=filemenu)
#        
#        Tk.config(self, menu=menubar)
        
        #dictionary of Frames
        self.frames = {}
        
        self.shapes = {Page_Variables : '425x525+150+100',       
                       Page_Model : '600x500+150+100'}
        
        #add Frames to dictionary
#        for F in (Page_Variables):
#        
#            frame = F(self.container, self)
#            
#            self.frames[F] = frame
#            
#            frame.grid(row=0, column=0, sticky='nsew')
        frame = Page_Variables(self.container, self)
        self.frames[Page_Variables] = frame
        frame.grid(row=0, column=0, sticky='nsew')
            
        
        #show initial Frame
        Tk.geometry(self, self.shapes[Page_Variables])
        self.show_frame(Page_Variables)
       
    #show frame
    def show_frame(self, cont, delete=False, cont_to_del = None):
        
        if cont not in self.frames:
            frame = cont(self.container, self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            
        Tk.geometry(self, self.shapes[cont])        
        frame = self.frames[cont]
        frame.tkraise() 
        
        if delete:
            del self.frames[cont_to_del]
        
class Page_Variables(Frame):
    
    STL_FILE = 'stl_file'
    SOLIDITYRATIO = 'solidityRatio'
    PRINTSPEED = 'printSpeed'
    SHIFTX = 'shiftX'
    SHIFTY = 'shiftY'
    FIRSTLAYERSHIFTZ = 'firstLayerShiftZ'
    NUMLAYERS = 'numLayers'
    PATTERN = 'pattern'
    DESIGNTYPE = 'designType'
    INFILLANGLEDEGREES = 'infillAngleDegrees'
    PATHWIDTH = 'pathWidth'
    LAYERHEIGHT = 'layerHeight'
    INFILLSHIFTX = 'infillShiftX'
    INFILLSHIFTY = 'infillShiftY'
    NUMSHELLS = 'numShells'
    TRIMADJUST = 'trimAdjust'
    START_GCODE_FILENAME = 'start_Gcode_FileName'
    END_GCODE_FILENAME = 'end_Gcode_FileName'
    OUTPUTFILENAME = 'outputFileName'
    BEDTEMP = 'bed_temp'
    EXTRUDERTEMP = 'extruder_temp'
    CURRPATH = os.path.dirname(os.path.realpath(__file__))
    GCODEPATH = CURRPATH + '\\Gcode\\'
    JSONPATH = CURRPATH + '\\JSON\\'
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        ########################
        #   class variables    #
        ########################
        
        #string that is the filename of the current file
        self.filename = ''
        
        #dictionary with variable name as key and StringVar as value
        self.text_variable = {} 
        
        #dictionary with variable name as key and Label as value        
        self.labels = {}
                   
        #dictionary with variable name as key and Entry as value
        self.entries = {}
        
        #array of Strings of the variables
        self.texts = [self.STL_FILE, self.SOLIDITYRATIO, self.PRINTSPEED, self.SHIFTX,            #part parameters
                 self.SHIFTY, self.FIRSTLAYERSHIFTZ, self.NUMLAYERS,                         #part parameters
                 self.PATTERN, self.DESIGNTYPE,                                           #part parameters
                 self.INFILLANGLEDEGREES, self.PATHWIDTH, self.LAYERHEIGHT,                  #layer parameters
                 self.INFILLSHIFTX, self.INFILLSHIFTY, self.NUMSHELLS, self.TRIMADJUST,         #layer parameters
                 self.START_GCODE_FILENAME, self.END_GCODE_FILENAME,                      #file parameters
                 self.BEDTEMP, self.EXTRUDERTEMP]                                           #print parameters
                 
        #array of part parameters
        self.part_param = [self.STL_FILE, self.SOLIDITYRATIO, self.PRINTSPEED, self.SHIFTX,           
                         self.SHIFTY, self.FIRSTLAYERSHIFTZ, self.NUMLAYERS,                      
                         self.PATTERN, self.DESIGNTYPE]
                         
        #array of layer parameters
        self.layer_param = [self.INFILLANGLEDEGREES, self.PATHWIDTH, self.LAYERHEIGHT,            
                            self.INFILLSHIFTX, self.INFILLSHIFTY, self.NUMSHELLS, self.TRIMADJUST]
                            
        #array of file parameters
        self.file_param = [self.START_GCODE_FILENAME, self.END_GCODE_FILENAME]
        
        #array of print parameters
        self.print_param = [self.BEDTEMP, self.EXTRUDERTEMP]
                 
        #array of Strings of the commonly used variables
        self.common_texts = [self.STL_FILE, self.SOLIDITYRATIO, self.PRINTSPEED, 
                        self.SHIFTX, self.SHIFTY, self.PATTERN, self.NUMSHELLS]
                      
        #array of Strings of the default values
        self.defaults = ['Arch3.stl', '1.09', '2000', '10, 50',                #part parameters
                    '10, 35, 60', '0', '8',                                         #part parameters
                    'None', '0',                                                    #part parameters
                    '0, -45, 90, 45, 45, 90, -45', '0.5', '0.4',                    #layer parameters
                    '0', '0', '13,1,1,0,0,1,1', '2*c.EPSILON',                      #layer parameters
                    'Start_Gcode_Taz5.txt', 'End_Gcode_Taz5.txt',                   #file parameters   
                    '999', '999']                                               #print parameters
                    
        self.create_var_page()
              
    ##########################################################
    #   methods that create labels, entries, and/or buttons  #
    ##########################################################
              
    #initial creation of labels
    def set_labels(self):
        
#        self.labelVariable = Label(self, text='Variable Name', font='-weight bold')
#        self.labelVariable.grid(row=0,column=0)
        
        #create all labels
        for x in range(len(self.texts)):
            #create label
            self.labels[self.texts[x]] = Label(self, text=self.texts[x])
            
        #show commonly used variables
        for x in range(len(self.common_texts)):
            #use grid() after creating label or dictionary value will be 'NoneType'
            self.labels[self.common_texts[x]].grid(row=x+1,column=0)   
            
    #initial creation of entries
    def set_entries(self):
        
#        self.labelValue = Label(self, text='Value', font='-weight bold')
#        self.labelValue.grid(row=0,column=1)
        #create all StringVars
        for x in range(len(self.texts)):
            #set textvariable to StringVar with default text as value
            self.text_variable[self.texts[x]] = StringVar(self, value=self.defaults[x])
            
        #create all entries
        for x in range(len(self.texts)):
            #create entry 
            self.entries[self.texts[x]] = ttk.Entry(self, textvariable=self.text_variable[self.texts[x]])
            
        #show commonly used variables
        for x in range(len(self.common_texts)):
            #use grid() after creating entry or dictionary value will be 'NoneType'
            self.entries[self.common_texts[x]].grid(row=x+1,column=1)
        
    #creates button for saving all values
    def save_option(self): 
        
        #create button
        buttonSave = ttk.Button(self,text='Save (exclude .json)',command=lambda: self.save()).grid(row=0,column=1)
    
    #creates label, entry, and button for uploading all values    
    def upload_option(self):   
        
        #create button
        buttonUpload = ttk.Button(self,text='Upload',command=lambda: self.upload()).grid(row=0,column=0)
        
    #create menu of label and buttons to switch between tabs
    def tab_buttons(self):
        
        #label for parameters
        labelParameters = Label(self,text='Parameters',font='-weight bold')
        labelParameters.grid(row=0,column=2)
        
        #button to display all variables
        buttonAll = ttk.Button(self,text='All',command=lambda: self.use_all())
        buttonAll.grid(row=1,column=2)
        #button to display commonly used variables
        buttonCommon = ttk.Button(self,text='Common',command=lambda: self.use_common())
        buttonCommon.grid(row=2,column=2)
        #button to display part parameters
        buttonParts = ttk.Button(self,text='Parts',command=lambda: self.use_parts())
        buttonParts.grid(row=3,column=2)
        #button to display layer parameters
        buttonLayers = ttk.Button(self,text='Layers',command=lambda: self.use_layers())
        buttonLayers.grid(row=4,column=2)
        #button to display file parameters
        buttonFiles = ttk.Button(self,text='Files',command=lambda: self.use_files())
        buttonFiles.grid(row=5,column=2)
        #button to display print parameters
        buttonPrints = ttk.Button(self,text='Prints',command=lambda: self.use_prints())
        buttonPrints.grid(row=6,column=2)
        
    #create label and buttons for different preset values of parameters
    def presets(self):
        
        #label for presets
        labelPresets = Label(self,text='Presets',font='-weight bold')
        labelPresets.grid(row=0,column=3)
        #button for dogbone
        buttonDogbone = ttk.Button(self,text='Dogbone',command=lambda: self.dogbone())
        buttonDogbone.grid(row=1,column=3)
    
    #create button to convert to Gcode
    def gcode(self):
        
        buttonGcode = ttk.Button(self,text='Convert to Gcode',command=lambda: self.convert())
        buttonGcode.grid(row=len(self.texts)+1,column=1)
        
    #all set up functions together
    def create_var_page(self):
        
        self.set_labels()
        self.set_entries()
        self.save_option()
        self.upload_option()
        self.tab_buttons()
        self.presets()
        self.gcode()
        self.model_page()
        self.g_robot()
    
    #create button to switch to 3D model page
    def model_page(self):  
        
        #button to switch to 3D model page
        buttonModel = ttk.Button(self, text='3D Model', 
                             command=lambda: self.to_model())
        buttonModel.grid(row=len(self.texts)+1,column=0)
        
    #create radiobutton to switch between gcode and robotcode
    def g_robot(self):
        
        self.g_robot_var = IntVar()
        self.g_robot_var.set(0)
        
        ttk.Radiobutton(self, text='Gcode', variable=self.g_robot_var, value=c.GCODE).grid(row=len(self.texts)+2,column=0)
        ttk.Radiobutton(self, text='RobotCode', variable=self.g_robot_var, value=c.ROBOTCODE).grid(row=len(self.texts)+2,column=1)
        
    #############################################
    #   methods that are called from buttons    #
    #############################################
                
    def save(self, name = None):
        
        if name == None:
            data = {}               #dictionary to put String value of StringVar values in
            self.filename = filedialog.asksaveasfilename()   #creates window to get filename
            gcodeName = self.filename.split('/')[len(self.filename.split('/'))-1] + '.gcode'
            self.filename = self.filename + '.json'  
        else:
            data = {}               #dictionary to put String value of StringVar values in
            gcodeName = name + '.gcode'
            self.filename = self.JSONPATH + name + '.json'               
        
        #check if the user cancelled saving the file
        if self.filename != '':
            to_string = [self.STL_FILE, self.START_GCODE_FILENAME, self.END_GCODE_FILENAME]      #variables with type String                
            to_int = [self.DESIGNTYPE, self.FIRSTLAYERSHIFTZ, self.BEDTEMP, self.EXTRUDERTEMP]  #variables with type int
            to_string_array = [self.TRIMADJUST]                                                 #variables with type String that go in an array
            to_int_array = [self.PRINTSPEED, self.SHIFTX, self.SHIFTY,                          #variables with type int that go in an array
                            self.NUMLAYERS, self.INFILLANGLEDEGREES,
                            self.INFILLSHIFTX, self.INFILLSHIFTY, self.NUMSHELLS]
            to_float_array = [self.SOLIDITYRATIO, self.PATHWIDTH,                               #variables with type double that go in an array
                               self.LAYERHEIGHT]
            to_none = [self.PATTERN]                                                            #variables with type None
            data[self.OUTPUTFILENAME] = gcodeName
            for key in self.text_variable:
                if key in to_string:
                    data[key] = self.text_variable[key].get()
                elif key in to_int:
                    data[key] = int(self.text_variable[key].get())   
                elif key in to_none:
                    data[key] = None                           
                else:
                    value = self.text_variable[key].get()            
                    if ' ' in value:
                        value = value.replace(' ', ',')                
                    if ',,' in value:
                        value = value.replace(',,', ',')               
                    if key in to_string_array:                        
                        data[key] = value.split(',')            
                    elif key in to_int_array:
                        data[key] = [int(i) for i in value.split(',')]     
                    elif key in to_float_array:
                        data[key] = [float(i) for i in value.split(',')]      
                    
            with open(self.filename, 'w') as fp:
                json.dump(data, fp)    #save JSON file
        
    #uploads dictionary from JSON file to replace current StringVar values, opens window to find file       
    def upload(self):

        data = {}               #new dictionary that will be replaced with dictionary from JSON file
        uploadname = filedialog.askopenfilename()     #creates window to find file
        
        if uploadname != '':
            with open(uploadname, 'r') as fp:
                data = json.load(fp)    #upload JSON file
                
            for key in data:
                if data[key] == None:
                    self.text_variable[key].set('None') #replace current StringVar with String 'None'
                elif key in self.text_variable.keys():
                    value = str(data[key])
                    value = value.replace('[','')
                    value = value.replace(']','')
                    self.text_variable[key].set(value)   #replace current StringVar values with data from JSON file
        
    #switch to tab with all parameters    
    def use_all(self):
        
        for x in range(len(self.labels)):
            self.labels[self.texts[x]].grid(row=x+1,column=0)    
            self.entries[self.texts[x]].grid(row=x+1,column=1)   
        
    def use_common(self):
        
        for text in self.texts:
            self.labels[text].grid_forget()      
            self.entries[text].grid_forget()     
            
        for x in range(len(self.common_texts)):
            self.labels[self.common_texts[x]].grid(row=x+1,column=0)     
            self.entries[self.common_texts[x]].grid(row=x+1,column=1)  
        
    #switch to tab with only part parameters
    def use_parts(self):
        
        for x in range(len(self.part_param)):
            self.labels[self.part_param[x]].grid(row=x+1,column=0)  
            self.entries[self.part_param[x]].grid(row=x+1,column=1)
            
        for layer_p in self.layer_param:
            self.labels[layer_p].grid_forget()    
            self.entries[layer_p].grid_forget()
            
        for file_p in self.file_param:
            self.labels[file_p].grid_forget()    
            self.entries[file_p].grid_forget()    
            
        for print_p in self.print_param:
            self.labels[print_p].grid_forget()
            self.entries[print_p].grid_forget()
      
    #switch to tab with only layer parameters  
    def use_layers(self):
        
        for x in range(len(self.layer_param)):
            self.labels[self.layer_param[x]].grid(row=x+1,column=0)     #show labels
            self.entries[self.layer_param[x]].grid(row=x+1,column=1)    #show entries
            
        for file_p in self.file_param:
            self.labels[file_p].grid_forget()    
            self.entries[file_p].grid_forget()    
            
        for part_p in self.part_param:
            self.labels[part_p].grid_forget()    
            self.entries[part_p].grid_forget()    
            
        for print_p in self.print_param:
            self.labels[print_p].grid_forget()
            self.entries[print_p].grid_forget()
      
    #switch to tabe with only file parameters  
    def use_files(self):
            
        for x in range(len(self.file_param)):
            self.labels[self.file_param[x]].grid(row=x+1,column=0)     #show labels
            self.entries[self.file_param[x]].grid(row=x+1,column=1)    #show entries
            
        for part_p in self.part_param:
            self.labels[part_p].grid_forget()    
            self.entries[part_p].grid_forget()    
            
        for layer_p in self.layer_param:
            self.labels[layer_p].grid_forget()    
            self.entries[layer_p].grid_forget()
            
        for print_p in self.print_param:
            self.labels[print_p].grid_forget()
            self.entries[print_p].grid_forget()
            
    def use_prints(self):
        
        for x in range(len(self.print_param)):
            self.labels[self.print_param[x]].grid(row=x+1,column=0)
            self.entries[self.print_param[x]].grid(row=x+1,column=1)
            
        for part_p in self.part_param:
            self.labels[part_p].grid_forget()    
            self.entries[part_p].grid_forget()    
            
        for layer_p in self.layer_param:
            self.labels[layer_p].grid_forget()    
            self.entries[layer_p].grid_forget()
            
        for file_p in self.file_param:
            self.labels[file_p].grid_forget()    
            self.entries[file_p].grid_forget()
        
    #change values to dogbone preset    
    def dogbone(self):
        
        dogbone_data = ['Arch3.stl', '1.09', '2000', '10, 50',                     #part parameters
                '10, 35, 60', '0', '8',                                                 #part parameters
                'None', '0',                                                            #part parameters
                '0, -45, 90, 45, 45, 90, -45', '0.5', '0.4',                            #layer parameters
                '0', '0', '13,1,1,0,0,1,1',  '2*c.EPSILON',                             #layer parameters
                'Start_Gcode_Taz5.txt', 'End_Gcode_Taz5.txt',                      #file parameters
                '999', '999']                                                       #print parameters
                
        for x in range(len(self.texts)):
            self.text_variable[self.texts[x]].set(dogbone_data[x])        #change values to dogbone values
    
    #create Gcode file                    
    def convert(self, name = None):
        
        if name == None:
            self.save()
        else:
            self.save(name)
        
        #check if the user cancelled converting to Gcode
        if self.filename != '':
            #convert to Gcode
            conversion = Main(self.filename, self.g_robot_var.get())
            conversion.run()
            
    
    #convert to gcode, switch to Page_Model        
    def to_model(self):
# TODO: uncomment these        
        self.convert('temp')
        
        self.controller.show_frame(Page_Model)
        
        os.remove(self.JSONPATH + 'temp.json')
        os.remove(self.GCODEPATH + 'temp.gcode')
        


class Page_Model(Frame):    
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.get_data()
        
    def get_data(self):
        
        data = []
        counter = 0
        self.xar = []
        self.yar = []
        self.zar = []
        self.layer_part = []
        
        with open('data_points.txt', 'r') as f:
            for line in f:
                if 'start' in line:
                    print('start ', counter)
                    start = counter
                elif 'layer_number' in line:
                    print(line)
                    print(counter)
                    self.layer_part.append([line.split(':')[1], line.split(':')[3], start, counter])
                else:
                    data.append(line)      
                    data[counter] = data[counter].split(',')
                    for y in range(0,len(data[counter])):
                        data[counter][y] = float(data[counter][y])
                    self.xar.append([data[counter][0], data[counter][3]])
                    self.yar.append([data[counter][1], data[counter][4]])
                    self.zar.append([data[counter][2], data[counter][5]])     
                    counter += 1
                    
        self.setup()
    
    def show_labels(self):
        
        labelIntro = Label(self, text='Choose the start and end layers of the model:')
        labelIntro.grid(row=0,column=1)
        
        labelStart = Label(self, text='Start')
        labelStart.grid(row=1,column=0)
        
        labelEnd = Label(self, text='End')
        labelEnd.grid(row=2,column=0)
        
    def show_scales(self):
        
        self.scaleStart = Scale(self, from_=0, to=len(self.x), length=500, orient=HORIZONTAL)
        self.scaleStart.grid(row=1,column=1)
        
        self.scaleEnd = Scale(self, from_=0, to=len(self.x), length=500, tickinterval=5000, orient=HORIZONTAL)
        self.scaleEnd.grid(row=2,column=1)
        
    def show_buttons(self):
        
        buttonSubmit = ttk.Button(self, text='Create Model', command=lambda: 
            self.make_graph(self.scaleStart.get(), self.scaleEnd.get()))
        buttonSubmit.grid(row=3,column=1)
        
        buttonVariables = ttk.Button(self, text='Variables', 
                     command=lambda: self.to_variables())
        buttonVariables.grid(row=0,column=0)
    
#        self.buttonUpdate = ttk.Button(self, text='Update from Variables', command=lambda: self.get_data())
#        self.buttonUpdate.grid(row=4,column=1)

#        self.radiobuttons = {}
#        x = 0
#        y = 0
#        z = 0
#        selection = IntVar()
#        
#        for id_array in self.layer_part:
#            rb_text = 'Part:' + str(id_array[1] + ' Layer:' + str(id_array[0]))
#            self.radiobuttons[str(id_array)] = ttk.Radiobutton(self, text=rb_text, variable=selection, value=x)
#            self.radiobuttons[str(id_array)].grid(row=z+4,column=y)
#            x+=1
#            y = x//5
#            z = x%5 

        self.intvar_layerparts = {}
        
        self.mb = ttk.Menubutton(self, text='testing')
        self.mb.grid()
        self.mb.menu = Menu (self.mb, tearoff=1)
        self.mb['menu'] = self.mb.menu
        
        for id_array in self.layer_part:
            self.intvar_layerparts[str(id_array)] = IntVar()
            self.rb_text = 'Part:' + str(id_array[1] + ' Layer:' + str(id_array[0]))
            self.mb.menu.add_checkbutton(label=self.rb_text, onvalue=1, offvalue=0, variable=self.intvar_layerparts[str(id_array)])
        
        self.mb.grid(row=5,column=1)
        
        buttonModel = ttk.Button(self, text='Create Model', command=lambda:
            self.make_model())
        buttonModel.grid(row=6,column=1)
        

    def setup(self):

        self.show_labels()
        self.show_scales()
        self.show_buttons()                
        
    def make_graph(self, start, end):
                
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.colors = []
        
        color_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        color_num2 = ['0','8']
        for one in color_num:
            for two in color_num2:
                for three in color_num2:
                    for four in color_num2:
                        for five in color_num2:
                            for six in color_num:
                                curr_color = '#' + one + two + three + four + five + six
                                self.colors.append(curr_color)
            
        for num in range(start, end):
            num_color = num%len(self.colors)
            self.ax.plot_wireframe(self.xar[num], self.yar[num], self.zar[num], color=self.colors[num_color])
            
        plt.show()
        
    def make_model(self):
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.colors = []
        
        color_num = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        color_num2 = ['0','8']
        for one in color_num:
            for two in color_num2:
                for three in color_num2:
                    for four in color_num2:
                        for five in color_num2:
                            for six in color_num:
                                curr_color = '#' + one + two + three + four + five + six
                                self.colors.append(curr_color)
         
#        for id_array in self.layer_part:
#            print(self.intvar_layerparts[id_array].get())
         
         
        counting = 0                       
        for id_array in self.layer_part:
            if self.intvar_layerparts[str(id_array)].get() == 1:
                for c in range(int(id_array[2]), int(id_array[3])):
                    num_color=c%len(self.colors)
                    self.ax.plot_wireframe(self.xar[c], self.yar[c], self.zar[c], color=self.colors[num_color])
                    
        plt.show()
        
    def to_variables(self):
        
        self.controller.show_frame(Page_Variables, True, Page_Model)
        
    
#class Page_Model(Frame):
#    
#    def __init__(self, parent, controller):
#        Frame.__init__(self, parent)
#        self.controller = controller
#        
#        labelExample = Label(self, text='HELLO')
#        labelExample.pack()
#        
#        self.to_variables()
#        
#        canvasExample = Canvas(self, width=200, height=100)
#        canvasExample.pack()      \
#        
#        canvasExample.create_rectangle(50, 20, 150, 80, fill='#476042')
#        canvasExample.create_line(0, 0, 50, 20, width=3)
#        
#        '''
#        f = Figure(figsize=(5,5), dpi=100)
#        a = f.add_subplot(111)
#        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
#        
#        canvas = FigureCanvasTkAgg(f, self)
#        canvas.show()
#        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
#        
#        toolbar = NavigationToolbar2TkAgg(canvas, self)
#        toolbar.update()
#        canvas._tkcanvas.pack()
#        '''
#        
#        
#    def to_variables(self):
#        
#        buttonVariable = ttk.Button(self, text='Variables', 
#                                command=lambda: self.controller.show_frame(Page_Variables))
#        buttonVariable.pack()
    
#only works if program is used as the main program, not as a module    
#if __name__ == '__main__':
    

#####################
#   GUI creation    #
#####################

#create GUI
gui = GUI()

#keeps GUI open, always necessary
gui.mainloop() 