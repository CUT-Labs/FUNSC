try:
    from PyInstaller import *
    import pyi_splash
except:
    print("Unable to import PyInstaller... continuing")
finally:
    from pathlib import Path
    from tkinter import *

    import tkinter.messagebox as messagebox
    from tkinter.scrolledtext import ScrolledText

    from math import *
    from mpmath import *

    import sympy
    import sympy as sp
    from sympy import sympify

    import requests
    from io import BytesIO
    from PIL import Image, ImageTk

    from FuncTypes import *
    from Util import *
    from RearrangeType import *
    from Function import *

    from cairosvg import svg2png

    from ctypes import windll

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\jhuse\OneDrive - University of Kentucky\Research\FunctionToCircuit\GitHub\build\assets\frame0")

# default values
variable = "x"
point = 0
power = 5
functionStr = "exp(-x)"
lExpress = ""
lFunc = None


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# entry_4 is the input function
# entry_3 is the variable
# entry_2 is the point
# entry_1 is the power
def updateVariables():
    global functionStr
    global variable
    global point
    global power
    global lExpress
    global lFunc

    functionStr = entry_4.get().replace("^", "**")
    variable = entry_3.get()
    point = int(entry_2.get())
    power = int(entry_1.get()) + 1
    lExpress = "lambda " + variable + ": " + functionStr
    # lambda x: sin(x)
    lFunc = eval(lExpress)

    print("-=( + Updated Variables (Local) + )=-")
    print("Function String: " + functionStr)
    print("Variable Selected: " + variable)
    print("Around Point: " + point.__str__())
    print("Degree Est.: " + power.__str__())
    print("Lambda Expression: " + lExpress)
    print("-----------")


def calculate():
    global image_3
    global lFunc

    # Update Variables
    updateVariables()

    print("-=( + Updated Variables (Global) + )=-")
    print("Function String: " + functionStr)
    print("Variable Selected: " + variable)
    print("Contains Variable: " + functionStr.__contains__(variable).__str__())
    print("Around Point: " + point.__str__())
    print("Degree Est.: " + power.__str__())
    print("Lambda Expression: " + lExpress)
    print("Lambda Function" + lFunc.__str__())
    print("-" * 100)

    # Convert to Function Parameter Types
    funcType = FuncTypes.SINUSOIDAL
    if functionStr.__contains__("log"):
        funcType = FuncTypes.LOGARITHMIC
    if functionStr.__contains__("exp"):
        funcType = FuncTypes.EXPONENTIAL
    if functionStr.__contains__("sin") or \
            functionStr.__contains__("cos") or \
            functionStr.__contains__("tan") or \
            functionStr.__contains__("csc") or \
            functionStr.__contains__("cot") or \
            functionStr.__contains__("sec") or \
            functionStr.__contains__("cosh") or \
            functionStr.__contains__("sinh") or \
            functionStr.__contains__("csch") or \
            functionStr.__contains__("coth") or \
            functionStr.__contains__("sech") or \
            functionStr.__contains__("tanh"):
        funcType = FuncTypes.SINUSOIDAL
    else:
        funcType = FuncTypes.POLYNOMIAL

    function = Function(lFunc, point, power, funcType, functionStr, variable)
    # Function(lambda function, point, order, type, title, variable)

    print("Function Type: " + function.functype.__str__())

    # Generate Function Results
    function.generateCoeffs()
    if function.rearrangeType != RearrangeType.UNKNOWN:
        function.generateCircuit()

        # Set Labels
        # convert taylor polynomial coeff dictionary to expression - set label (entry_5)
        x = "x"
        expr = "$\displaystyle " + sympy.latex(sympify(function.taylorString)) + "$"

        # This creates a PNG file and saves there the output of sympy.preview
        bg_color = "{196, 196, 196}"
        sp.preview(expr, euler=False, preamble=r"\documentclass{standalone}"
                                               r"\usepackage{pagecolor}"
                                               r"\definecolor{background}{RGB}" + bg_color +
                                               r"\pagecolor{background}"
                                               r"\begin{document}",
                   viewer="file", filename="assets/taylor.png", dvioptions=["-D 1200"])
        # Open the image as if it were a file. This works only for .ps!
        img = Image.open("assets/taylor.png")
        # See note at the bottom
        img.load()
        img = img.resize((393, int((393 * img.size[1] / img.size[0]))), Image.BILINEAR)
        photo = ImageTk.PhotoImage(img)
        entry_5.config(image=photo)
        entry_5.image = photo

        # convert rearranged polynomial coeff dictionary to expression - set label (entry_6)
        #exec(variable + " = sympy.symbols('" + variable + "')")
        #expr = "$\displaystyle " + sympy.latex(eval(function.rearrangeString)) + "$"  # sympify(function.rearrangeString, strict=True)

        #print(expr)

        # This creates a PNG file and saves there the output of sympy.preview
        #bg_color = "{196, 196, 196}"
        #sp.preview(expr, euler=False, preamble=r"\documentclass{standalone}"
        #                                       r"\usepackage{pagecolor}"
        #                                       r"\definecolor{background}{RGB}" + bg_color +
        #                                       r"\pagecolor{background}"
        #                                       r"\begin{document}",
        #           viewer="file", filename="assets/rearranged.png", dvioptions=["-D 1200"])
        # Open the image as if it were a file. This works only for .ps!
        #img = Image.open("assets/rearranged.png")
        # See note at the bottom
        #img.load()
        #img = img.resize((393, int((393 * img.size[1] / img.size[0]))), Image.BILINEAR)
        #photo = ImageTk.PhotoImage(img)
        #entry_6.config(image=photo)
        #entry_6.image = photo
        entry_6.delete(0, END)
        entry_6.insert(INSERT, function.rearrangeString)

        # trace equation - set label (entry_8)
        function.generateTrace()
        entry_7.delete(0, END)
        entry_7.insert(INSERT, str(function.traceValue))

        # Update Circuit Diagram
        baseWidth = 908
        baseHeight = 268
        svg2png(url="assets/result.svg", write_to="assets/result.png", output_height=500)
        img = Image.open("assets/result.png")

        # adjust size based on width (for bigger circuits)
        wpercent = (baseWidth / float(img.size[0]))
        hsize = int(float(img.size[1])*float(wpercent))

        # adjust size based on height (for smaller circuits)
        hpercent = (baseHeight / float(img.size[1]))
        wsize = int(float(img.size[0])*float(hpercent))

        # if the adjusted size is taller than the frame, use size based on height instead
        if hsize > baseHeight:
            img = img.resize((baseHeight, wsize), Image.LANCZOS)
        else:
            img = img.resize((baseWidth, hsize), Image.LANCZOS)

        photo = ImageTk.PhotoImage(img)

        image_3_updater.config(image=photo)
        image_3_updater.image = photo

    else:
        messagebox.showinfo("UK Function To Circuit Designer", "Error! The function you entered is not supported for these parameters:\n" +
                                                               "-----------------------------------\n"
                                                               "Function: " + functionStr.replace("**", "^") + "\n" +
                                                               "Variable: " + variable + "\n" +
                                                               "Degree: " + str(power-1) + "\n" +
                                                               "Point Estimation: " + str(point))


def clearEq():
    entry_4.delete(0, END)


def insertVar():
    global variable
    entry_4.insert(INSERT, variable)


def insertButton(button):
    if button == 0:
        entry_4.insert(INSERT, "0")
    elif button == 1:
        entry_4.insert(INSERT, "1")
    elif button == 2:
        entry_4.insert(INSERT, "2")
    elif button == 3:
        entry_4.insert(INSERT, "3")
    elif button == 4:
        entry_4.insert(INSERT, "4")
    elif button == 5:
        entry_4.insert(INSERT, "5")
    elif button == 6:
        entry_4.insert(INSERT, "6")
    elif button == 7:
        entry_4.insert(INSERT, "7")
    elif button == 8:
        entry_4.insert(INSERT, "8")
    elif button == 9:
        entry_4.insert(INSERT, "9")
    elif button == "/":
        entry_4.insert(INSERT, "/")
    elif button == "*":
        entry_4.insert(INSERT, "*")
    elif button == "-":
        entry_4.insert(INSERT, "-")
    elif button == "+":
        entry_4.insert(INSERT, "+")
    else:
        entry_4.insert(INSERT, button)
        entry_4.icursor(entry_4.index(INSERT) - 1)  # move cursor back 1


# windll.shcore.SetProcessDpiAwareness(1)
window = Tk()

# generate favicon
# faviconURL_white = "https://i.gyazo.com/46f8159ba9cf00c29841f309498ef3cf.png"
faviconURL_blue = "https://i.gyazo.com/0a5a8e0b41b060db1eacbceb234e47f2.png"
faviconResponse = requests.get(faviconURL_blue)
faviconIMGData = faviconResponse.content
favicon = ImageTk.PhotoImage(Image.open(BytesIO(faviconIMGData)))

# Setting icon of master window
window.iconphoto(True, favicon)
window.title("UK Function to Circuit Designer")

window.geometry("1400x750")
window.configure(bg="#DCDDDE")

canvas = Canvas(
    window,
    bg="#DCDDDE",
    height=750,
    width=1400,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

canvas.create_rectangle(
    0.0,
    0.0,
    1400.0,
    77.77777862548828,
    fill="#1B365D",
    outline="")

canvas.create_rectangle(
    0.0,
    700.0,
    1400.0,
    751.0,
    fill="#4D567C",
    outline="")

canvas.create_rectangle(
    0.0,
    466.6666564941406,
    1400.0,
    700.0,
    fill="#1B365D",
    outline="")

# +
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("+"),
    relief="flat"
)
button_1.place(
    x=1330.0,
    y=637.7777709960938,
    width=52.5,
    height=46.66668701171875
)

# -
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("-"),
    relief="flat"
)
button_2.place(
    x=1330.0,
    y=583.3333129882812,
    width=52.5,
    height=46.66668701171875
)

# *
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("*"),
    relief="flat"
)
button_3.place(
    x=1330.0,
    y=528.888916015625,
    width=52.5,
    height=46.66668701171875
)

# /
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("/"),
    relief="flat"
)
button_4.place(
    x=1330.0,
    y=474.4444580078125,
    width=52.5,
    height=46.66668701171875
)

# (-)
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("-"),
    relief="flat"
)
button_5.place(
    x=1198.75,
    y=637.7777709960938,
    width=52.5,
    height=46.66668701171875
)

# 0
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(0),
    relief="flat"
)
button_6.place(
    x=1133.125,
    y=637.7777709960938,
    width=52.5,
    height=46.66668701171875
)

# 1
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(1),
    relief="flat"
)
button_7.place(
    x=1133.125,
    y=583.3333129882812,
    width=52.5,
    height=46.66668701171875
)

# 2
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(2),
    relief="flat"
)
button_8.place(
    x=1198.75,
    y=583.3333129882812,
    width=52.5,
    height=46.66668701171875
)

# 3
button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(3),
    relief="flat"
)
button_9.place(
    x=1264.375,
    y=583.3333129882812,
    width=52.5,
    height=46.66668701171875
)

# 4
button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(4),
    relief="flat"
)
button_10.place(
    x=1133.125,
    y=528.888916015625,
    width=52.5,
    height=46.66668701171875
)

# 5
button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(5),
    relief="flat"
)
button_11.place(
    x=1198.75,
    y=528.888916015625,
    width=52.5,
    height=46.66668701171875
)

# 6
button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(6),
    relief="flat"
)
button_12.place(
    x=1264.375,
    y=528.888916015625,
    width=52.5,
    height=46.66668701171875
)

# 7
button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(7),
    relief="flat"
)
button_13.place(
    x=1133.125,
    y=474.4444580078125,
    width=52.5,
    height=46.66668701171875
)

# 8
button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(8),
    relief="flat"
)
button_14.place(
    x=1198.75,
    y=474.4444580078125,
    width=52.5,
    height=46.66668701171875
)

# 9
button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton(9),
    relief="flat"
)
button_15.place(
    x=1264.375,
    y=474.4444580078125,
    width=52.5,
    height=46.66668701171875
)

# exp()
button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("exp()"),
    relief="flat"
)
button_16.place(
    x=903.875,
    y=474.4444580078125,
    width=112.875,
    height=46.66668701171875
)

# log()
button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("log()"),
    relief="flat"
)
button_17.place(
    x=773.5,
    y=474.4444580078125,
    width=112.875,
    height=46.66668701171875
)

# tan()
button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("tan()"),
    relief="flat"
)
button_18.place(
    x=643.125,
    y=474.4444580078125,
    width=112.875,
    height=46.66668701171875
)

# cos()
button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("cos()"),
    relief="flat"
)
button_19.place(
    x=512.75,
    y=474.4444580078125,
    width=112.875,
    height=46.66668701171875
)

# sin()
button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("sin()"),
    relief="flat"
)
button_20.place(
    x=386.75,
    y=474.4444580078125,
    width=112.875,
    height=46.66668701171875
)

# sec()
button_image_21 = PhotoImage(
    file=relative_to_assets("button_21.png"))
button_21 = Button(
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("sec()"),
    relief="flat"
)
button_21.place(
    x=387.0,
    y=529.0,
    width=112.875,
    height=46.66668701171875
)

# sech()
button_image_22 = PhotoImage(
    file=relative_to_assets("button_22.png"))
button_22 = Button(
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("sech()"),
    relief="flat"
)
button_22.place(
    x=387.0,
    y=583.0,
    width=112.875,
    height=46.66668701171875
)

# csc()
button_image_23 = PhotoImage(
    file=relative_to_assets("button_23.png"))
button_23 = Button(
    image=button_image_23,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("csc()"),
    relief="flat"
)
button_23.place(
    x=513.0,
    y=529.0,
    width=112.875,
    height=46.66668701171875
)

# csch()
button_image_24 = PhotoImage(
    file=relative_to_assets("button_24.png"))
button_24 = Button(
    image=button_image_24,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("csch()"),
    relief="flat"
)
button_24.place(
    x=513.0,
    y=583.0,
    width=112.875,
    height=46.66668701171875
)

# coth()
button_image_25 = PhotoImage(
    file=relative_to_assets("button_25.png"))
button_25 = Button(
    image=button_image_25,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("coth()"),
    relief="flat"
)
button_25.place(
    x=643.0,
    y=583.0,
    width=112.875,
    height=46.66668701171875
)
# tanh()
button_image_26 = PhotoImage(
    file=relative_to_assets("button_26.png"))
button_26 = Button(
    image=button_image_26,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("tanh()"),
    relief="flat"
)
button_26.place(
    x=774.0,
    y=583.0,
    width=112.875,
    height=46.66668701171875
)

# cot()
button_image_27 = PhotoImage(
    file=relative_to_assets("button_27.png"))
button_27 = Button(
    image=button_image_27,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("cot()"),
    relief="flat"
)
button_27.place(
    x=643.0,
    y=529.0,
    width=112.875,
    height=46.66668701171875
)

# sinh()
button_image_28 = PhotoImage(
    file=relative_to_assets("button_28.png"))
button_28 = Button(
    image=button_image_28,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("sinh()"),
    relief="flat"
)
button_28.place(
    x=774.0,
    y=529.0,
    width=112.875,
    height=46.66668701171875
)

# cosh()
button_image_29 = PhotoImage(
    file=relative_to_assets("button_29.png"))
button_29 = Button(
    image=button_image_29,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertButton("cosh()"),
    relief="flat"
)
button_29.place(
    x=904.0,
    y=529.0,
    width=112.875,
    height=46.66668701171875
)

#
# IMAGE 1: UNIVERSITY OF KENTUCKY LOGO
#
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    114.0,
    47.0,
    image=image_image_1
)

#
# IMAGE 2: DIVIDER LINE
#
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    241.5,
    38.22222137451172,
    image=image_image_2
)

# Variable Label
canvas.create_text(
    30.625,
    535.888916015625,
    anchor="nw",
    text="Variable:",
    fill="#FFFFFF",
    font=("BitterRoman ExtraBold", 20 * -1)
)

# Point Estimation Label
canvas.create_text(
    27.125,
    571.6666870117188,
    anchor="nw",
    text="Point Est:",
    fill="#FFFFFF",
    font=("BitterRoman ExtraBold", 20 * -1)
)

# Degree Label
canvas.create_text(
    44.625,
    607.4444580078125,
    anchor="nw",
    text="Degree:",
    fill="#FFFFFF",
    font=("BitterRoman ExtraBold", 20 * -1)
)

#
# ENTRY 1: TRACED VALUE ENTRY
#
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    165.8125,
    618.7222290039062,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#DCDDDE",
    fg="#000716",
    highlightthickness=0,
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
entry_1.place(
    x=137.375,
    y=607.4444580078125,
    width=56.875,
    height=20.5555419921875
)
entry_1.insert(0, power)

#
# ENTRY 2: POINT ESTIMATION ENTRY
#
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    165.8125,
    582.9444580078125,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#DCDDDE",
    fg="#000716",
    highlightthickness=0,
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
entry_2.place(
    x=137.375,
    y=571.6666870117188,
    width=56.875,
    height=20.5555419921875
)
entry_2.insert(0, point)

#
# ENTRY 3: VARIABLE ENTRY
#
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    165.8125,
    547.1666870117188,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#DCDDDE",
    fg="#000716",
    highlightthickness=0,
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
entry_3.place(
    x=137.375,
    y=535.888916015625,
    width=56.875,
    height=20.5555419921875
)
entry_3.insert(0, variable)

#
# ENTRY 4: User Input Function Entry
#
entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    566.5,
    449.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#B1C9E8",
    fg="#000716",
    highlightthickness=0,
    font=("BitterRoman ExtraBold", 15)
)
entry_4.place(
    x=0.0,
    y=432.0,
    width=1133.0,
    height=33.0
)
entry_4.insert(0, functionStr)

#
# IMAGE 3: CIRCUIT DIAGRAM BACKGROUND
#
image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    908.0,
    268.0,
    image=image_image_3
)

# diagram picture
image_3_updater = Label(
    bd=0,
    bg="#fff",
    highlightthickness=0,
    #    state="disabled",
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
image_3_updater.place(
    x=444,
    y=124,
    width=908.0,
    height=268.0
)

# Maclaurin Series Estimate
canvas.create_text(
    27.0,
    90.0,
    anchor="nw",
    text="Maclaurin Series:",
    fill="#1F2C5E",
    font=("BitterRoman ExtraBold", 24 * -1)
)

# Rearranged Estimate Label
canvas.create_text(
    27.0,
    229.0,
    anchor="nw",
    text="Rearranged Estimate:",
    fill="#1F2C5E",
    font=("BitterRoman ExtraBold", 24 * -1)
)

# Traced Value at Point Label
canvas.create_text(
    27.0,
    382.0,
    anchor="nw",
    text="Traced Value at Point:",
    fill="#1F2C5E",
    font=("BitterRoman ExtraBold", 24 * -1)
)

# Circuit Diagram Label
canvas.create_text(
    444.0,
    90.0,
    anchor="nw",
    text="Circuit Diagram",
    fill="#1F2C5E",
    font=("BitterRoman ExtraBold", 24 * -1)
)

#
# ENTRY 5: MACLAURIN SERIES
#
entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))

entry_bg_5 = canvas.create_image(
    223.5,
    160.0,
    image=entry_image_5
)

entry_5 = Label(
    bd=0,
    bg="#C4C4C4",
    highlightthickness=0,
    #    state="disabled",
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
entry_5.place(
    x=27.0,
    y=124.0,
    width=393.0,
    height=70.0
)
# entry_5.insert(0, "5")

#
# ENTRY 6: REARRANGED ESTIMATE
#
entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    223.5,
    301.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#C4C4C4",
    fg="#000716",
    highlightthickness=0,
    justify="center",
    font=("BitterRoman ExtraBold", 12)
)
entry_6.place(
    x=27.0,
    y=265.0,
    width=393.0,
    height=70.0
)
# entry_6.insert(0, "6")

#
# ENTRY 7: TRACED VALUE
#
entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    350.0,
    395.5,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#C4C4C4",
    fg="#000716",
    highlightthickness=0,
    justify="center",
    font=("BitterRoman ExtraBold", 15)
)
entry_7.place(
    x=280.0,
    y=379.0,
    width=140.0,
    height=31.0
)
# entry_7.insert(0, "7")

# Calculate Button
button_image_32 = PhotoImage(
    file=relative_to_assets("button_32.png"))
button_32 = Button(
    image=button_image_32,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: calculate(),
    relief="flat"
)
button_32.place(
    x=1133.0,
    y=431.0,
    width=267.0,
    height=38.0
)

# Update user variables (variable, point, power) Input Area
button_image_33 = PhotoImage(
    file=relative_to_assets("button_33.png"))
button_33 = Button(
    image=button_image_33,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: updateVariables(),
    relief="flat"
)
button_33.place(
    x=27.0,
    y=643.0,
    width=167.0,
    height=38.0
)
# Variable Button
button_image_30 = PhotoImage(
    file=relative_to_assets("button_30.png"))
button_30 = Button(
    image=button_image_30,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insertVar(),
    relief="flat"
)
button_30.place(
    x=388.0,
    y=638.0,
    width=112.875,
    height=46.66668701171875
)

# Clear Button
button_image_31 = PhotoImage(
    file=relative_to_assets("button_31.png"))
button_31 = Button(
    image=button_image_31,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: clearEq(),
    relief="flat"
)
button_31.place(
    x=66.0,
    y=474.0,
    width=112.875,
    height=46.66668701171875
)

# nsf logo
image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    266.0,
    726.0,
    image=image_image_4
)

# Supporting Statement
canvas.create_text(
    296.0,
    715.0,
    anchor="nw",
    text="This project is supported by the National Science Foundation (NSF) and the University of Kentucky.",
    fill="#FFFFFF",
    font=("Caladea Regular", 20 * -1)
)

canvas.create_text(
    263.0,
    23.5,
    anchor="nw",
    text="FUNSC",
    fill="#FFFFFF",
    font=("BitterRoman ExtraBold", 24 * -1)
)
try:
    pyi_splash.close()
finally:
    window.resizable(True, True)
    window.mainloop()
