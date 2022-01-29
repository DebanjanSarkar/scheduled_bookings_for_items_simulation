import datetime
import os

class BOOKING:
    slot_length = 7
    slot_interval = datetime.timedelta( slot_length )                                             #No of days for which booking will be done for deault slot case.
    def book( self , user , item , sdate , edate=None ):
            self.user = user
            self.item = item
            self.startDate = sdate
            if(edate==None):
                self.endDate = sdate + BOOKING.slot_interval
            else:
                self.endDate = edate
            return(self.endDate)                                #Returns end date as this value will be usefull to update the last date till item is booked.

    @staticmethod
    def isPermissible( uid , itemId ):
        if(item_isBooked[itemId]==None):
            return 1
        else:
            for i in bookings_list:
                if( i.user==uid and i.item==itemId):
                    return 0
            else:
                return 1

    @staticmethod
    def showBookings_all():
        if(len(bookings_list)==0):
            print("NO Bookings Done Yet!")
        else:
            for i in range(len(bookings_list)):
                print(f"\nBooking #{i+1}:-")
                print("------------------\n")
                print("User id :",bookings_list[i].user)
                print("Item being booked :",bookings_list[i].item)
                print("Booked from :",bookings_list[i].startDate)
                print("Booked till :",bookings_list[i].endDate)

    @staticmethod
    def showBookings_user(uid):
        if(len(bookings_list)==0):
            print("NO Bookings Done Yet!")
        else:
            j=0
            for i in bookings_list:
                if(i.user==uid):
                    j+=1
                    print(f"\nBooking #{j}:-")
                    print("------------------\n")
                    print("User id :",i.user)
                    print("Item being booked :",i.item)
                    print("Booked from :",i.startDate)
                    print("Booked till :",i.endDate)
            if(j==0):
                print("\nThe user has still not done any bookings yet!\n")

    @staticmethod
    def cancel( userid , itemid ):
        if( not(BOOKING.isPermissible(userid,itemid)) ):
            for i in range(len(bookings_list)):
                if( bookings_list[i].user==userid and bookings_list[i].item==itemid ):
                    bookings_list.pop(i)
                    print(f"\nThe booking for useId {userid} and itemId {itemid} has been deleted successfully!")
                    break
            if( bookings_perItem[itemid] > 1 ):
                item_isBooked[itemid] = item_isBooked[itemid] - datetime.timedelta( BOOKING.slot_length + 1 )
            elif( bookings_perItem[itemid] == 1 ):
                item_isBooked[itemid] = None

            bookings_perItem[itemid] -= 1
            bookings_perUser[userid] -= 1

            while(i<len(bookings_list)):
                if( bookings_list[i].item==itemid ):
                    bookings_list[i].startDate = bookings_list[i].startDate - datetime.timedelta( BOOKING.slot_length + 1 )
                    bookings_list[i].endDate = bookings_list[i].endDate - datetime.timedelta( BOOKING.slot_length + 1 )
                    print(f"Each further bookings for item {itemid} has been shifted by 7 days ahead, due to cancellation.\n\n")
                i+=1;
        else:
            print("\nThe specified user does not have a booking for the specified item.\n\n")


users = [int(x) for x in input("Enter the User Ids(integers only) of the Users(separated by spaces, without commas):\n").split()]
items = [x for x in input("Enter the Items(alphabets or alphanumeric with alphabet as first letter of items, e.g. a, b1 , cd52 , etc.):\n").split()]

bookings_perUser = {}.fromkeys(users,0)
bookings_perItem = {}.fromkeys(items,0)
item_isBooked = {}.fromkeys(items)      #This dictionary will map each item to the last date till which it is booked.
bookings_list = []                      #This will contain the list of BOOKING class objects, where each object denotes one booking each

options = """
a. Show ids of available users who can place bookings for items.
b. Show all items which can be booked.
c. Check the next closest date from which an item is available for booking.
d. Book any item to the closest avaible slot, for default slot interval of 7 days.
e. Show total number of bookings done till now.
f. Show all bookings in detail(done till now).
g. Show bookings for any particular user.
h. Show for how many consecutive slots, an item is booked currently for.
i. Cancel any booking.
j. Clear the console screen.
k. Exit
"""

while(1):
    print("\nSelect the choice corresponding to the operation you want to perform:",options,"Enter your choice: ",sep='\n',end=' ')
    choice = input("\n")[0].lower()

    if(choice=='a'):
        print("\nUsers and their ids:-")
        for i in range(1,len(users)+1):
            print(f"User id (uid) of user {i} :  {users[i-1]}")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='b'):
        print("\nList of items:")
        for i in range(len(items)):
            print(f"Item id of item {i+1} :  {items[i]}")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='c'):
        itemid = input("\nEnter the item id of the item for which you want to know the closest date from which it is available for booking: \n")
        if(itemid not in items):
            print("No such item Id exists.")
            input("Press Enter to try again...\n")
            continue
        if(item_isBooked[itemid]==None):
            print(f"Item {itemid} is available for booking from {datetime.date.today()}")
        else:
            print(f"Item {itemid} is available for booking from { item_isBooked[itemid] + datetime.timedelta(1) }")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='d'):
        b1 = BOOKING()
        try:
            userid = int(input("\nEnter the user id of the user who wants to do the booking: "))
        except ValueError:
            print("User Id must be of integer type.")
            input("Press Enter to try again...\n")
            continue
        if(userid not in users):
            print("No such user Id (uid) exists.")
            input("Press Enter to try again...\n")
            continue
        itemid = input("Enter the item id of the item which you want to book: ")
        if(itemid not in items):
            print("No such item Id exists.")
            input("Press Enter to try again...\n")
            continue
        if( BOOKING.isPermissible( userid , itemid ) ):
            if(item_isBooked[itemid]==None):
                end_date = b1.book( userid , itemid , datetime.date.today() )
            else:
                end_date = b1.book( userid , itemid , item_isBooked[itemid] + datetime.timedelta(1) )

            item_isBooked[itemid] = end_date
            bookings_list.append(b1);
            bookings_perItem[itemid] += 1
            bookings_perUser[userid] += 1
            print(f"\nBooking SUCCESSFULL! \nItem {itemid} is booked from {b1.startDate} to {b1.endDate} for user with uid {userid}")
        else:
            print("\nBooking NOT PERMISSIBLE.\nThe user already has one booking for this item.")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='e'):
        print(f"\nTotal number of bookings done till now:  {len(bookings_list)} bookings.")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='f'):
        BOOKING.showBookings_all()
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='g'):
        try:
            userid = int(input("\nEnter the user id of the user whose bookings you want to view: "))
        except ValueError:
            print("User Id must be of integer type.")
            input("Press Enter to try again...\n")
            continue
        if(userid not in users):
            print("No such user Id (uid) exists.")
            input("Press Enter to try again...\n")
            continue
        print(f"User with uid {userid} has done {bookings_perUser[userid]} bookings till now.\n")
        BOOKING.showBookings_user(userid)
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='h'):
        itemid = input("Enter the item id of the item : ")
        if(itemid not in items):
            print("No such item Id exists.")
            input("Press Enter to try again...\n")
            continue
        print(f"\nItem {itemid} has been booked for {bookings_perItem[itemid]} consecutive 7-day slots currently.\n")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='i'):
        try:
            userid = int(input("\nEnter the user id of the user whose booking is to be cancelled: "))
        except ValueError:
            print("User Id must be of integer type.")
            input("Press Enter to try again...\n")
            continue
        if(userid not in users):
            print("No such user Id (uid) exists.")
            input("Press Enter to try again...\n")
            continue
        itemid = input("Enter the item id of the item for which the booking is to be cancelled: ")
        if(itemid not in items):
            print("No such item Id exists.")
            input("Press Enter to try again...\n")
            continue
        BOOKING.cancel(userid,itemid)
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='j'):
        input("\n\nPress Enter to Clear the console screen, and get the menu (the users, items and bookings(if fon any), will remain)...\n")
        os.system('cls')

    elif(choice=='k'):
        input("\nPress Enter to exit...")
        break

    else:
        print("\n\nInvalid choice entry...")
        input("\n\nPress Enter to get the main menu...\n")
