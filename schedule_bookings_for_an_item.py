"""
Created and Finalised on Sat Jan 29 10:48:01 2022

This script simulates Scheduled bookings for an item by a user, for closest available 7-days slot, adhering to following rules:-
1. 1 user can book multiple items for the same time.
2. 1 user can only have only one booking for a given item.
3. Multiple users can not book the same item for same slot.
   When booking is done for same item by multiple users, the script automatically does the booking of the item for the next 7-days of availability.

Features of this booking-simulation script:-
1. For the first time, user needs to enter the user ids of Users, and the item ids (same as name of item in terms of this program functioning), seperated
   by spaces, and then for that list of users and items, several operations can be performed(booking, cancellations, etc), for several times, till the EXIT
   of the program. Throughout each execution, the user ids and items remains preserved, that are entered at the start of the script.
2. The user does not have to provide any starting date or ending date of booking as input. Just the item to be booked and the uid of the user who is booking.
3. Each booking will be of 7-days slot only, and the user cannot change the slot-interval for booking. However slot selngth can be easily changed by just
   chaning the Static variables of the BOOKING object, and it is set globally for the entire program.
4. For the first booking of each item, the starting date of booking automatically will be the current system date automatically.
5. Bookings can even be cancelled! For cancellation of booking for any item, if the item has been booked for further upcoming slots, each further slots
   of that specific item booking will be shifted by 1 7-day slot ahead, automatically!
6. The whole program runs as a menu driven program, where repeated operations can be performed till EXIT option is chosen, which is designed mainly
   to run in console. At each operation at every step, the user gets clear and lucid messages what he has to do to perform something, or what he has
   done. So it is made to be USER-FRIENDLY !
7. At almost all steps the code is well-managed to handle exceptions, and user credibility and type is validated at each step. Thus, the program handle
   almost all types of errors and exceptions!

@author: Debanjan Sarkar
"""

import datetime
import os

class BOOKING:
    """
    This class objects will store each inidividual bookings, that is for each booking made, one object of this class will be created, and in it
    -> The 'user' instance variable stores userId of the user who has done the booking.
    -> The 'item' instance variable stores the item which is booked.
    -> The 'startDate' instance variable stores the day from which the booking starts.
    -> The 'endDate' instance variable stores the day till which the booking is done.
    and in the static variables of this clas, the slot-interval objects are stored, which is of 7 days by default.
    """
    slot_length = 7
    slot_interval = datetime.timedelta( slot_length )            #No of days for which booking will be done for deault slot case.
    def book( self , user , item , sdate , edate=None ):
            """
            Main instance function which creates instance variable and stores the metadata of each booking in them.
            """
            self.user = user
            self.item = item
            self.startDate = sdate
            #This if-else block is made to add further functionality, which will make this function able to handle customised end date of booking!
            if(edate==None):
                self.endDate = sdate + BOOKING.slot_interval
            else:
                self.endDate = edate
            return(self.endDate)                                #Returns end date as this value will be usefull to update the last date till item is booked.

    @staticmethod
    def isPermissible( uid , itemId ):
        '''
        This function checks whether the user is permissible to place booking for the specified argument, obtained as argument.
        If user is allowed to place the order, it returns 1, else 0 for the case when the user already has booked this same item.
        '''
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
        """
        This method is to print metadata of all the bookings existing, on the output screen.
        """
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
        """
        This method is to print metadata of all the bookings for the userId passed as argument, on the output screen.
        """
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
        """
        This method is to cancel the booking for the userId-itemId combination passed as argument.
        """
        if( not(BOOKING.isPermissible(userid,itemid)) ):                #Checks whether this UserId-ItemId combination of booking exists or not.
            #This loop actually does the deletion of the booking, by removing the specific BOOKING object from the list storing all the bookings
            for i in range(len(bookings_list)):
                if( bookings_list[i].user==userid and bookings_list[i].item==itemid ):
                    bookings_list.pop(i)
                    print(f"\nThe booking for useId {userid} and itemId {itemid} has been deleted successfully!")
                    break
            #This statement is to update the last-date till which the item is booked, after cancellation happens.
            if( bookings_perItem[itemid] > 1 ):
                item_isBooked[itemid] = item_isBooked[itemid] - datetime.timedelta( BOOKING.slot_length + 1 )
            elif( bookings_perItem[itemid] == 1 ):
                item_isBooked[itemid] = None

            #Updation of the no of bookings per item and per user of the specific user and item in the global variables.
            bookings_perItem[itemid] -= 1
            bookings_perUser[userid] -= 1

            """
            If the specific Item has further bookings(made after the booking that is cancelled, was made), this while-loop shifts
            starting and ending date of all the further booking objects for this specific Item of which the booking is cancelled.
            """
            while(i<len(bookings_list)):
                if( bookings_list[i].item==itemid ):
                    bookings_list[i].startDate = bookings_list[i].startDate - datetime.timedelta( BOOKING.slot_length + 1 )
                    bookings_list[i].endDate = bookings_list[i].endDate - datetime.timedelta( BOOKING.slot_length + 1 )
                    print(f"Each further bookings for item {itemid} has been shifted by 7 days ahead, due to cancellation.\n\n")
                i+=1;
        else:
            print("\nThe specified user does not have a booking for the specified item.\n\n")

#Main Driver code of the script starts here:
print("""
This script simulates Scheduled bookings for an item by a user, for closest available 7-days slot, adhering to following rules:-
1. 1 user can book multiple items for the same time.
2. 1 user can only have only one booking for a given item.
3. Multiple users can not book the same item for same slot.
   When booking is done for same item by multiple users, the script automatically does the booking of the item for the next 7-days of availability.
""")
try:
    users = [int(x) for x in input("\n\nEnter the User Ids(integers only) of the Users(separated by spaces, without commas):\n").split()]
except ValueError:
    print("\nInvalid format of input. \nPlease enter integer user Ids only, in the correct format(seperated by spaces only.)")
    input("Press Enter to exit, and try again by restarting the script.\n")
    exit(2)
items = [x for x in input("Enter the Items(alphabets or alphanumeric with alphabet as first letter of items, e.g. a, b1 , cd52 , etc.):\n").split()]

#Metadata containing sequences that is used to optimize the booking and cancellation algorithms
bookings_perUser = {}.fromkeys(users,0)         #This dictionary will map each userId to the number of bookings he has done, and existing currently(excluding the cancelled bookings)
bookings_perItem = {}.fromkeys(items,0)         #This dictionary will map each Item to the number of bookings existing for this item(excluding the cancelled bookings)
item_isBooked = {}.fromkeys(items)              #This dictionary will map each item to the last date till which it is booked.
bookings_list = []                              #This will contain the list of BOOKING class objects, where each object denotes one booking each

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
    choice = input("")[0].lower()

    if(choice=='a'):
        print("\nUsers and their ids:-")
        for i in range(1,len(users)+1):
            print(f"User id (uid) of user {i} :  {users[i-1]}")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='b'):
        print("\nList of items:-")
        for i in range(len(items)):
            print(f"Item id of item {i+1} :  {items[i]}")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='c'):
        itemid = input("\nEnter the item id of the item for which you want to know the closest date from which it is available for booking: \n")
        if(itemid not in items):
            print("No such item Id exists.")
            input("Press Enter to try again...\n")
            continue
        if(item_isBooked[itemid]==None):                                    #Checks if any booking for this items is done or not.
            #If this item is unbooked, shows availability from current system date.
            print(f"Item {itemid} is available for booking from {datetime.date.today()}")
        else:
            #If this item is booked, shows availability from the date after the last date till booked.
            print(f"Item {itemid} is available for booking from { item_isBooked[itemid] + datetime.timedelta(1) }")
        input("\n\nPress Enter to get the main menu...\n")

    elif(choice=='d'):
        b1 = BOOKING()
        #input-validation of the input by user.
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

        #Code that performs the BOOKING according to the input.
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
        #input-validation of the input by user.
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
        #Function-call for cancellation.
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
