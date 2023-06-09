from customtkinter import *
from tkinter import *
import sys
from DatabaseActions import *
from PIL import Image, ImageTk

set_appearance_mode("light")
set_default_color_theme("green")

# Stworzenie głównego okna
global ordersWindow
ordersWindow: CTk = CTk()
ordersWindow.title("Restaurant Manager")
ordersWindow.iconbitmap("Resources/restaurant_4373.ico")
ordersWindow.geometry("1200x600")
ordersWindow.configure(background="#F4F5F7")

ordersWindow.columnconfigure(0, weight=1)
ordersWindow.columnconfigure(1, weight=1)
ordersWindow.columnconfigure(2, weight=1)
ordersWindow.columnconfigure(3, weight=1)
ordersWindow.columnconfigure(4, weight=1)
ordersWindow.columnconfigure(5, weight=13)
ordersWindow.columnconfigure(6, weight=18)
ordersWindow.rowconfigure(0, weight=1)
ordersWindow.rowconfigure(1, weight=15)
ordersWindow.rowconfigure(2, weight=1)

global currentUserId
currentUserId = int(sys.argv[0])


def navigateToDashboard() -> None:
    user = returnCertainUser(currentUserId)
    userId: int = user[0]
    sys.argv = [str(userId)]
    ordersWindow.destroy()
    exec(open('Dashboard.py').read())


def navigateToMenu() -> None:
    user = returnCertainUser(currentUserId)
    userId: int = user[0]
    sys.argv = [str(userId)]
    ordersWindow.destroy()
    exec(open('Menu.py').read())


def logout() -> None:
    ordersWindow.destroy()
    exec(open('Login.py').read())


# navbar

menuButton = CTkButton(ordersWindow, command=navigateToMenu, text="", fg_color="white")
menuButton.grid(pady=20, row=0, column=0)
image = CTkImage(light_image=Image.open("Resources/menu.png"), size=(30, 30))
menuImagelabel = CTkLabel(menuButton, text="", image=image)
menuImagelabel.bind(navigateToMenu)
menuImagelabel.grid(row=0, column=0, sticky=W + E + N + S)

dashboardButton = CTkButton(ordersWindow, command=navigateToDashboard, text="", fg_color="white")
dashboardButton.grid(pady=20, row=0, column=1, columnspan=2)
image = CTkImage(light_image=Image.open("Resources/pie-chart.png"), size=(30, 30))
DashboardImagelabel = CTkLabel(dashboardButton, text="", image=image)
DashboardImagelabel.grid(pady=5, row=0, column=0)
dashboardLabel = CTkLabel(dashboardButton, text="Dashboard", font=("Kanit", 16), bg_color='transparent')
dashboardLabel.grid(pady=5, row=0, column=1, sticky=W)

ordersButton = CTkButton(ordersWindow, text="")
ordersButton.grid(pady=20, row=0, column=3, columnspan=2)
image = CTkImage(light_image=Image.open("Resources/clipboard.png"), size=(30, 30))
OrdersMenuImage = CTkLabel(ordersButton, text="", image=image)
OrdersMenuImage.grid(pady=5, row=0, column=0)
ordersLabel = CTkLabel(ordersButton, text="Orders", font=("Kanit", 16))
ordersLabel.grid(pady=5, row=0, column=1, sticky=W)

logoutButton = CTkButton(ordersWindow, command=logout, text="Logout", fg_color="red")
logoutButton.grid(pady=10, padx=25, row=0, column=6, sticky=E)

# incoming


incomingFrame = CTkFrame(ordersWindow, bg_color="#E8EAED", corner_radius=10)
incomingFrame.grid(pady=10, padx=10, row=1, rowspan=2, column=0, columnspan=6, sticky=W + E + S + N)

incomingFrame.columnconfigure(0, weight=1)
incomingFrame.columnconfigure(1, weight=1)
incomingFrame.columnconfigure(2, weight=15)
incomingFrame.rowconfigure(0, weight=1)

incomingLabel = CTkLabel(incomingFrame, text="Incoming", font=("Kanit", 20, "bold"))
incomingLabel.grid(pady=10, padx=25, row=0, column=0, sticky=E)
incomingAmountLabel = CTkLabel(incomingFrame, text=str(returnAmountOfIncoming(currentUserId)), font=("Kanit", 16),
                               corner_radius=10, fg_color='#F4F5F7')
incomingAmountLabel.grid(pady=10, row=0, column=1, sticky=W)

# incoming list

for x, order in enumerate(returnIncomingOrdersList(currentUserId)):
    incomingFrame.rowconfigure(x + 1, weight=5)
    certainOrderFrame = CTkFrame(incomingFrame, bg_color="#FFFFFF", corner_radius=10)
    certainOrderFrame.grid(pady=10, padx=10, row=x + 1, column=0, columnspan=3, sticky=W + E + S + N)
    certainOrderFrame.columnconfigure(0, weight=3)
    certainOrderFrame.columnconfigure(1, weight=1)
    certainOrderFrame.columnconfigure(2, weight=2)
    certainOrderFrame.rowconfigure(0, weight=1)
    certainOrderFrame.rowconfigure(1, weight=3)
    certainOrderFrame.rowconfigure(2, weight=2)

    idLabel = CTkLabel(certainOrderFrame, text="#"+str(order[0]), font=("Kanit", 23),
                       bg_color='transparent')
    idLabel.grid(pady=5, padx=25, row=0, column=0, sticky=W)
    customerNameLabel = CTkLabel(certainOrderFrame, text=str(order[5]), font=("Kanit", 18),
                                 bg_color='transparent')
    customerNameLabel.grid(pady=4, padx=25, row=1, column=0, sticky=W)

    takeAwayButton = CTkButton(certainOrderFrame, text="Takeaway", width=25, height=20, fg_color="green",
                               corner_radius=30)
    takeAwayButton.grid(pady=4, padx=20, row=2, column=0, sticky=W)

    # additional frame for items list
    orderItemListFrame = CTkFrame(certainOrderFrame, bg_color="#F4F5F7", corner_radius=10)
    orderItemListFrame.grid(pady=10, padx=10, row=0, rowspan=2, column=1, columnspan=2, sticky=W + E + S + N)
    itemList = returnItemsForOrderList(order[0])
    for count, item in enumerate(itemList):
        if count > 2:
            xMoreLabel = CTkLabel(orderItemListFrame, text="+"+str(int(len(itemList)) - count)+" more", font=("Kanit", 19),
                                  bg_color='transparent')
            xMoreLabel.grid(pady=4, padx=25, row=count + 1, column=2, sticky=W)
            break
        itemWithCountLabel = CTkLabel(orderItemListFrame, text=str(item[6]) + "x "+str(item[2]), font=("Kanit", 19),
                                      bg_color='transparent')
        itemWithCountLabel.grid(pady=4, padx=25, row=count + 1, column=2, sticky=W)

    timeButton = CTkButton(certainOrderFrame, text="", width=25, height=25, fg_color="#F2F7ED", text_color="#589A1D", corner_radius=30)
    timeButton.grid(pady=4, padx=20, row=2, column=1, sticky=E)
    minutesValueLabel = CTkLabel(timeButton, text="15", font=("Kanit", 19),
                          bg_color='transparent', text_color="#589A1D")
    minutesValueLabel.grid(pady=1, padx=20, row=0, column=0, sticky=W+E+S+N)
    minutesLabel = CTkLabel(timeButton, text="min.", font=("Kanit", 13),
                            bg_color='transparent', text_color="#589A1D")
    minutesLabel.grid(pady=1, padx=20, row=1, column=0, sticky=W+E+S+N)

    acceptButton = CTkButton(certainOrderFrame, text="Accept", width=25, height=40, fg_color="blue", corner_radius=30)
    acceptButton.grid(pady=25, padx=20, row=2, column=2, sticky=E)

# accepted

acceptedFrame = CTkFrame(ordersWindow, bg_color="#E8EAED")
acceptedFrame.grid(pady=10, padx=10, row=1, column=6, sticky=W + E + S + N)

acceptedFrame.columnconfigure(0, weight=1)
acceptedFrame.columnconfigure(1, weight=1)
acceptedFrame.columnconfigure(2, weight=15)

acceptedLabel = CTkLabel(acceptedFrame, text="Accepted", font=("Kanit", 20, "bold"))
acceptedLabel.grid(pady=10, padx=25, row=0, column=0, sticky=E)
acceptedAmountLabel = CTkLabel(acceptedFrame, text=str(returnAmountOfAccepted(currentUserId)), font=("Kanit", 16),
                               corner_radius=10, fg_color='#F4F5F7')
acceptedAmountLabel.grid(pady=10, row=0, column=1, sticky=W)


for x, order in enumerate(returnAcceptedOrdersList(currentUserId)):
    acceptedFrame.rowconfigure(x + 1, weight=5)
    certainOrderFrame = CTkFrame(acceptedFrame, bg_color="#FFFFFF", corner_radius=10)
    certainOrderFrame.grid(pady=10, padx=10, row=x + 1, column=0, columnspan=3, sticky=W + E + S + N)
    certainOrderFrame.columnconfigure(0, weight=3)
    certainOrderFrame.columnconfigure(1, weight=1)
    certainOrderFrame.columnconfigure(2, weight=2)
    certainOrderFrame.rowconfigure(0, weight=1)
    certainOrderFrame.rowconfigure(1, weight=3)
    certainOrderFrame.rowconfigure(2, weight=3)

    idLabel = CTkLabel(certainOrderFrame, text="#"+str(order[0]), font=("Kanit", 23),
                       bg_color='transparent')
    idLabel.grid(pady=5, padx=25, row=0, column=0, sticky=W)
    customerNameLabel = CTkLabel(certainOrderFrame, text=str(order[5]), font=("Kanit", 18),
                                 bg_color='transparent')
    customerNameLabel.grid(pady=4, padx=25, row=1, column=0, sticky=W)

    takeAwayButton = CTkButton(certainOrderFrame, text="Takeaway", width=25, height=20, fg_color="green",
                               corner_radius=30)
    takeAwayButton.grid(pady=4, padx=20, row=2, column=0, sticky=W)

    # additional frame for items list
    orderItemListFrame = CTkFrame(certainOrderFrame, bg_color="#F4F5F7", corner_radius=10)
    orderItemListFrame.grid(pady=10, padx=10, row=0, rowspan=2, column=1, columnspan=2, sticky=W + E + S + N)
    itemList = returnItemsForOrderList(order[0])
    for count, item in enumerate(itemList):
        if count > 2:
            xMoreLabel = CTkLabel(orderItemListFrame, text="+"+str(int(len(itemList)) - count)+" more", font=("Kanit", 19),
                                  bg_color='transparent')
            xMoreLabel.grid(pady=4, padx=25, row=count + 1, column=2, sticky=W)
            break
        itemWithCountLabel = CTkLabel(orderItemListFrame, text=str(item[6]) + "x "+str(item[2]), font=("Kanit", 19),
                                      bg_color='transparent')
        itemWithCountLabel.grid(pady=4, padx=25, row=count + 1, column=2, sticky=W)

    timeButton = CTkButton(certainOrderFrame, text="", width=25, height=25, fg_color="#F2F7ED", text_color="#589A1D", corner_radius=30)
    timeButton.grid(pady=4, padx=20, row=2, column=1, sticky=E)
    minutesValueLabel = CTkLabel(timeButton, text="15", font=("Kanit", 19),
                          bg_color='transparent', text_color="#589A1D")
    minutesValueLabel.grid(pady=1, padx=20, row=0, column=0, sticky=W+E+S+N)
    minutesLabel = CTkLabel(timeButton, text="min.", font=("Kanit", 13),
                            bg_color='transparent', text_color="#589A1D")
    minutesLabel.grid(pady=1, padx=20, row=1, column=0, sticky=W+E+S+N)

    acceptButton = CTkButton(certainOrderFrame, text="Ready", width=25, height=40, fg_color="green", corner_radius=30)
    acceptButton.grid(pady=25, padx=20, row=2, column=2, sticky=E)

# accepted list

# ready

readyFrame = CTkFrame(ordersWindow, fg_color="#FFFFFF")
readyFrame.grid(pady=10, padx=10, row=2, column=6, sticky=W + E + S + N)

readyFrame.columnconfigure(0, weight=1)
readyFrame.columnconfigure(1, weight=1)
readyFrame.columnconfigure(2, weight=15)

readyLabel = CTkLabel(readyFrame, text="Ready", font=("Kanit", 20, "bold"))
readyLabel.grid(pady=25, padx=25, row=0, rowspan=2, column=0, sticky=E + N + S)
readyAmountLabel = CTkLabel(readyFrame, text=str(returnAmountOfReady(currentUserId)), font=("Kanit", 16),
                            corner_radius=10, fg_color='#E8EAED')
readyAmountLabel.grid(pady=25, row=0, rowspan=2, column=1, sticky=W + N + S)
newOrdersReadyLabel = CTkLabel(readyFrame, text="1 new order is ready", font=("Kanit", 18),
                               text_color='#589A1D')
newOrdersReadyLabel.grid(pady=25, padx=25, rowspan=2, row=0, column=2, sticky=E + N + S)

# ready list

"""

allUserOrders: list = returnAllOrdersForUser(currentUserId)

print(allUserOrders)

for index, order in enumerate(allUserOrders):
    CTkLabel(ordersWindow, text=str(order), font=("Kanit", 16), text_color="red").grid(pady=5, padx=10, row=index + 1,
                                                                                        column=0, columnspan=6)"""

ordersWindow.mainloop()
