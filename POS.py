# Imports
import tkinter as tk
import sys
import os
from tkinter import *

# Fonts ----------------------------------------------------------------------------------------------------------------
FONT = ("Times New Roman", 55)
FONT2 = ("Times New Roman", 55, "bold")


# GUI app class --------------------------------------------------------------------------------------------------------
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

class GUIApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # root window attributes
        self.title("Order Terminal")
        self.attributes("-fullscreen", True)

        # set up the container for all of the frames
        container = tk.Frame(self)
        container.pack(expand=True, fill="both")

        #
        self.frames = {}
        for F in (WelcomePage, OrderPage, ReviewPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[page_name]
        frame.pack_forget()
        frame.pack(expand=True, fill="both")

    # Start-Mara
    # get page so u can use its variable from anyother page

    def get_page(self, page_name):
        for page in self.frames.values():
            if str(page.__class__.__name__) == page_name:
                return page

    # end-Mara


# Welcome page class ---------------------------------------------------------------------------------------------------
class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        # Button 1
        start_ord_btn = tk.Button(self, text="Start Order",
                                  padx=90, pady=40,
                                  command=lambda: controller.show_frame("OrderPage"))
        start_ord_btn.place(rely=.4, relx=.35, x=0, y=0)
        start_ord_btn["font"] = FONT2

        # Name text field and method for clearing
        init_entry_txt = tk.StringVar()
        init_entry_txt.set("Order Name")

        def clear_name_text(event):
            name_txt.config(fg="black")
            if name_txt.get() == "Order Name":
                event.widget.delete(0, tk.END)
            else:
                name_txt.config(fg="black")

        name_txt = tk.Entry(self, textvariable=init_entry_txt, width=51)
        name_txt.config(fg="gray")
        name_txt.bind("<Button-1>", clear_name_text)
        name_txt.bind("<FocusIn>", clear_name_text)
        name_txt.place(rely=.6, relx=.35, x=0, y=0)


# Order page class -----------------------------------------------------------------------------------------------------


class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller
        label = tk.Label(self, text=" Place your order:", fg="white", bg="black", font=FONT2)

        label.grid(row=0, column=2, pady=10, sticky="E")

        # start-Mara
        # make order screen dynamically based on Menu.txt
        f = open('Menu.txt', 'r')
        self.menuL = f.read()
        self.menuL = self.menuL.splitlines()
        i = 0
        self.priceL = []
        while i < len(self.menuL):
            thing = self.menuL[i].split()
            self.menuL[i] = thing[0]
            self.priceL.insert(i, float(thing[1]))
            i += 1

        itemId = 0
        y = 1
        x = 0
        self.toggle = []
        for item in self.menuL:
            menu = tk.Label(self, text=self.menuL[itemId], font=FONT, borderwidth=9, relief="raised",
                            background='#33AAFF', width=7, height=2)
            menu.grid(row=y, column=x, padx=20, pady=20, columnspan=2)
            price = tk.Label(self, text="$" + str(self.priceL[itemId]), font=("Times New Roman", 13, "bold"),
                             background='#33AAFF')

            price.grid(row=y, column=x, padx=20, pady=20, columnspan=2, sticky="N")

            self.toggle.insert(itemId, tk.DoubleVar(self, value=0))

            w = tk.Spinbox(self, from_=0, to=10, width=2, textvariable=self.toggle[itemId])

            w.grid(row=y, column=x, padx=20, pady=20, sticky="s")
            itemId += 1
            x += 2
            if x == 8:
                x = 0
                y += 1

            # End-Mara

        # Button 2

        cancel_btn = tk.Button(self, text="Cancel",
                               padx=10, pady=5,
                               command=lambda: controller.show_frame("WelcomePage"))
        cancel_btn.place(rely=.9, relx=.05, x=0, y=0)

        # Button 3
        next_btn = tk.Button(self, text="Submit",
                             padx=22, pady=5,
                             command=self.onclick)
        next_btn.place(rely=.9, relx=.9, x=0, y=0)

    def onclick(self):
        reviewpage = self.controller.get_page("ReviewPage")

        sz = len(self.toggle)
        i = 0

        while i < sz:
            reviewpage.cart[i].set(self.toggle[i].get())

            i += 1
        # print(reviewpage.cart[0].get())
        self.controller.show_frame("ReviewPage")


# Review page class ----------------------------------------------------------------------------------------------------
# revPage = Frame(root)
class ReviewPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        # start-Mara
        # trying to create the order review using variables from orderpage

        label = tk.Label(self, text="Please review your order:", fg="white", bg="black", font=FONT)
        label.pack()
        orderpage = self.controller.get_page("OrderPage")

        self.count = 0
        self.total = 0
        self.cart = []
        self.string = tk.StringVar(value="")
        self.orders = []

        def callback(name, index, op):

            if self.count == len(orderpage.toggle):
                self.count = 0
                self.total = 0
                sz = 0
                while sz < len(self.orders):
                    self.orders[sz].destroy()
                    sz += 1

            if self.getvar(name) > 0:
                amount = orderpage.priceL[self.count] * self.getvar(name)
                self.orders.append(
                    tk.Label(self, text=orderpage.menuL[self.count] + " $" + str(amount), font=FONT, width=20))
                order_sz = len(self.orders) - 1

                self.orders[order_sz].pack()
                self.total += amount
            if self.count == len(orderpage.toggle) - 1:
                self.string.set("Total $" + str(self.total))

            self.count += 1

        i = 0
        for item in orderpage.toggle:
            self.cart.append(tk.DoubleVar(value=0))
            self.cart[i].trace_add("write", callback)
            i += 1

        total = tk.Label(self, textvariable=self.string, font=FONT2, width=15)
        total.place(rely=.85, relx=.3, x=0, y=0)

        # end-Mara


        # Button 4
        prev_btn = tk.Button(self, text="Previous",
                             padx=10, pady=5,
                             command=lambda: controller.show_frame("OrderPage"))
        prev_btn.place(rely=.9, relx=.05, x=0, y=0)

        # Button 5
        place_ord_btn = tk.Button(self, text="Confirm",
                                  padx=22, pady=5,
                                  command=restart_program)
        place_ord_btn.place(rely=.9, relx=.9, x=0, y=0)


# Driver code ----------------------------------------------------------------------------------------------------------
app = GUIApp()
app.mainloop()

