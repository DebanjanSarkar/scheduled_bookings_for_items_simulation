Author:-
---------
Debanjan Sarkar


This script simulates Scheduled bookings for an item by a user, for closest available 7-days slot, adhering to following rules:-
----------------------------------------------------------------------------------------------------------------------------------
1. 1 user can book multiple items for the same time.
2. 1 user can only have only one booking for a given item.
3. Multiple users can not book the same item for same slot.
   When booking is done for same item by multiple users, the script automatically does the booking of the item for the next 7-days of availability.


Features of this booking-simulation script:-
----------------------------------------------
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
