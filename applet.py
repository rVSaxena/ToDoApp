from tkinter import *
from tkcalendar import Calendar
from datetime import date
import json

today_year, today_month, today_date=list(map(int, str(date.today()).split('-')))
widget_stack=[]


root=Tk()
root.geometry("400x400")

cal=Calendar(root, selectmode = 'day', year=today_year, month=today_month, day=today_date)
cal.pack(pady=20)
widget_stack.append((cal, 0))

def print_whole_json():
    while(len(widget_stack)>0 and widget_stack[-1][1]>=2):
        widget_stack.pop(-1)[0].pack_forget()

    outarea=Text(root, height=20, width=70)
    widget_stack.append((outarea, 2))
    outarea.pack()

    with open('./list.json', 'r') as fileobject:
        output=json.load(fileobject)

    for key in output:
        if len(output[key])>0:
            outarea.insert(END, str(key)+" -- "+", ".join(output[key])+'\n')
    return

def readTasks(curyear, curmonth, curdate):
    date=str(curyear)+'-'+str(curmonth)+'-'+str(curdate)
    with open('./list.json', 'r') as fileobject:
        output=json.load(fileobject)
    res=[]
    try:
        for i in output[date]:
            res.append(i)
    except KeyError as e:
        pass
    return res

def addTask(curyear, curmonth, curdate, task):
    date=str(curyear)+'-'+str(curmonth)+'-'+str(curdate)
    
    with open('./list.json') as f:
        feed=json.load(f)
    
    if date in feed:
        feed[date].append(task)
    else:
        feed[date]=[task]
    
    with open('./list.json', 'w') as file:
        file.write(json.dumps(feed))
    return

def remove_task(curyear, curmonth, curdate, idx):
    while(len(widget_stack)>0 and widget_stack[-1][1]>=3):
        widget_stack.pop(-1)[0].pack_forget()

    idx=idx-1
    date=str(curyear)+'-'+str(curmonth)+'-'+str(curdate)
    
    with open('./list.json') as f:
        data=json.load(f)

    if date not in data:
        return

    try:
        assert(idx<len(data[date]))
    except AssertionError as e:
        return

    data[date]=data[date][:idx]+data[date][idx+1:]

    with open('./list.json', 'w') as file:
        data=json.dump(data, file)
    
    success_label=Label(root)
    success_label.pack()
    widget_stack.append((success_label, 3))
    success_label.config(text="Success!")
    
    return

def read_inpt_area(curyear, curmonth, curdate, inpt_area):
    to_add=inpt_area.get("1.0", "end-1c")
    addTask(curyear, curmonth, curdate, to_add)
    return

def del_inpt_area(curyear, curmonth, curdate, inputArea):
    
    to_remove=int(inputArea.get("1.0", "end-1c"))

    remove_task(curyear, curmonth, curdate, to_remove)
    return


def radioSelection():
    selected_date=cal.get_date()
    curmonth, curdate, curyear=list(map(int, selected_date.split('/')))

    if var.get()==1:
        while(len(widget_stack)>0 and widget_stack[-1][1]>=2):
            widget_stack.pop(-1)[0].pack_forget()

        # read data and display
        OutputArea=Text(root, height=20, width=70)
        OutputArea.delete("1.0", "end")
        OutputArea.pack()
        widget_stack.append((OutputArea, 2))

        data=readTasks(curyear, curmonth, curdate)
        for line in data:
            OutputArea.insert(END, line+'\n')

    elif var.get()==2:
        while(len(widget_stack)>0 and widget_stack[-1][1]>=2):
            widget_stack.pop(-1)[0].pack_forget()

        # Append the thing in the textbox
        inputArea=Text(root, height=1, width=70)
        inputArea.delete("1.0", "end")
        inputArea.pack()
        widget_stack.append((inputArea, 2))

        confirm_add_button=Button(root, text='Append this', width=25, command=lambda : read_inpt_area(curyear, curmonth, curdate, inputArea))
        confirm_add_button.pack()
        widget_stack.append((confirm_add_button, 2))
        
    elif var.get()==3:
        while(len(widget_stack)>0 and widget_stack[-1][1]>=2):
            widget_stack.pop(-1)[0].pack_forget()

        # delete the to_do at the index
        help_display=Label(root)
        help_display.pack()
        widget_stack.append((help_display, 2))
        help_display.config(text="Enter the index in the area below. Indices will be one indexed.")
        inputArea2=Text(root, height=1, width=70)
        inputArea2.delete("1.0", "end")
        inputArea2.pack()
        widget_stack.append((inputArea2, 2))

        confirm_del_button=Button(root, text='Delete at this index', width=25, command=lambda : del_inpt_area(curyear, curmonth, curdate, inputArea2))
        confirm_del_button.pack()
        widget_stack.append((confirm_del_button, 2))

        

display_all_button=Button(root, text='Display all tasks', width=25, command=lambda : print_whole_json())
widget_stack.append((display_all_button, 1))
display_all_button.pack()

var=IntVar()
R1=Radiobutton(root, text="Read", variable=var, value=1, command=radioSelection)
R1.pack()
widget_stack.append((R1, 1))

R2=Radiobutton(root, text="Append", variable=var, value=2, command=radioSelection)
R2.pack()
widget_stack.append((R2, 1))

R3=Radiobutton(root, text="Delete", variable=var, value=3, command=radioSelection)
R3.pack()
widget_stack.append((R3, 1))



# Excecute Tkinter
root.mainloop()
