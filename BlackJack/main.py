"""
ICS4U1
Names: Muaj and Sadiq
Class Assignment: Blackjack
Date: 10/11/2021
Program Description: Blackjack Tkinter
"""

from tkinter import Tk, Label, Button, Entry,Frame, PhotoImage, Toplevel
from card import card
import random, time
from PIL import Image, ImageTk

#first window of program
class Intro(object):
    def __init__(self, master):
        self.master = master
        master.title(" ")
        #Create background image and essentially window size
        img = PhotoImage(file="deal.png")
        self.background = Label(master,image=img)
        self.background.photo = img
        self.background.place(x=0, y=0)

        #Text
        self.label_balance = Label(master, text="Enter your Balance and Press Play!",font = "Times 10 italic",bg="white")
        self.label_balance.place(x=70,y=64)

        self.label_balance1 = Label(master, text="The minimum is $10",font = "Times 10 italic",bg="white")
        self.label_balance1.place(x=120,y=94)

        self.label_title = Label(master, text="BLACKJACK!",font = "Roman 25 bold italic",bg="white")
        self.label_title.place(x=75,y=5)

        self.play = Button(master, text = "Play", command = self.new_window, font= "Times 9 italic", bg="white",fg="green",activebackground="gray")
        self.play.place(x=205,y=180)

        self.bet_entry = Entry(master,bg="white",font="Times 13 italic",fg="green",width=6)
        self.bet_entry.place(x=125,y=181)

    #window made when player presses play
    def new_window(self):
        balance = self.bet_entry.get()
        #valid input
        if len(self.bet_entry.get())!=0 and balance.isnumeric() and int(balance)>=10:
          self.newWindow = Toplevel(self.master)
          self.app = BabyBlackJack(self.newWindow,balance)
        #invalid input
        else:
          self.label_balance.config(text="Please enter a valid input!")

#player wins round
class Win(object):
    def __init__(self, master,win):
        self.master = master
        master.title(" ")
        master.config(cursor="cross")

        self.win=int(win)

        #Create background image and essentially window size
        img = PhotoImage(file="win.png")
        self.background = Label(master,image=img)
        self.background.photo = img
        self.background.grid(row=0, column=0)


        self.label_win = Label(master, text="NICELY DONE 😎 You won $%d" % self.win, font = "Times 15 bold italic", bg="white")
        self.label_win.place(x=220,y=380)

        root.after(5000, lambda: self.master.destroy())

#player loses round
class Lose(object):
    def __init__(self, master,loss):
        self.master = master
        master.title(" ")
        master.config(cursor="exchange")
        
        self.reason=int(loss)

        #Create background image and essentially window size
        img = PhotoImage(file="lose.png")
        self.background = Label(master,image=img)
        self.background.photo = img
        self.background.place(x=0, y=0)
        
        if self.reason ==0:
          self.label_lose = Label(master, text="You went over 21", font="Times 13 italic", bg="white")
          self.label_lose.place(x=330,y=300)

        elif self.reason==1:
          self.label_lose = Label(master, text="The dealer was closer to 21", font="Times 13 italic", bg="white")
          self.label_lose.place(x=280,y=300)
          
        else:
          self.label_lose = Label(master, text="The dealer had the same sum", font="Times 13 italic", bg="white")
          self.label_lose.place(x=280,y=300)


        root.after(5000, lambda: self.master.destroy())

#user presses quit, or doesn't have enough money to continue playing
class Over(object):
  def __init__(self, master):
        self.master = master
        master.title(" ")
        master.config(cursor="spider")
        

        #Create background image and essentially window size
        img = PhotoImage(file="over.png")
        self.background = Label(master,image=img)
        self.background.photo = img
        self.background.grid(row=0, column=0)

        root.after(4000, lambda: self.master.destroy())
  
class End(object):
  def __init__(self, master, balance,winnings):
        self.master = master
        master.title(" ")
        master.config(cursor="star")

        self.balance=int(balance)
        self.winnings=int(winnings)

        #Create background image and essentially window size
        img = PhotoImage(file="endscreen.png")
        self.background = Label(master,image=img)
        self.background.photo = img
        self.background.place(x=0, y=0)
        
        #result of specific round
        if self.winnings>0:
          self.label_winnings = Label(master, text="Overall, You won: $%d" % self.winnings,font="Times 13 italic",fg="black", bg="white")
        elif self.winnings==0:
          self.label_winnings = Label(master, text="Overall, You broke even!",font="Times 13 italic",fg="black", bg="white")
        else:
          self.winnings*=-1
          self.label_winnings = Label(master, text="Overall, You lost: $%d" % self.winnings,font="Times 13 italic",fg="black", bg="white")
        
        self.label_winnings.place(x=320,y=50)
        
        if self.balance<10:
          self.label_balance = Label(master, text="Your balance is below 10. You can no longer play!" ,font="Times 13 italic",fg="black", bg="white")
          self.label_balance.place(x=200,y=370)
        else:
          self.label_balance = Label(master, text="Your balance: $%d" % self.balance,font="Times 13 italic",fg="black", bg="white")
          self.label_balance.place(x=330,y=370)

#game commences
class BabyBlackJack(object):
    def __init__(self, master,balance):
        

        #Create background image and essentially window size
        img = PhotoImage(file="bj.png")
        self.background = Label(master,image=img,height=400, width=680)
        self.background.photo = img
        self.background.grid(row=0, column=0)

        #Creates Betting Chips image
        img2 = PhotoImage(file="chipsp.png")
        self.chips = Label(master,image=img2)
        self.chips.photo = img2
        self.chips.place(x=350, y=75)

        #Create empty window title
        self.master = master
        master.title(" ")
        master.config(cursor="circle")
        
        #variables for game
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.player_sum = 0
        self.dealer_sum = 0
      
        self.player_money = int(balance)
        self.player_bet=0
        self.player_winnings=0
   
        # Cycle through clubs, diamonds, spades and hearts
        for letter in ["C","D","S","H"]:
          for number in range(1,14): # 1-10 number cards, ace is 1, jack 11, Q 12 is K is 13
            #filename to be used when creating image
            filename = "cards//%s%s.png" % (number,letter)
            value = number
            #add all cards to deck with their file name and value and shuffle the deck
            self.deck.append(card(filename,value))

        random.shuffle(self.deck)

        #Labels
        self.label_player = Label(master, text="Your Cards",font = "Times 12 bold",bg="white")
        self.label_player.place(x=70,y=25)

        self.label_dealer = Label(master, text="Dealer's Cards",font = "Times 12 bold", bg="white")
        self.label_dealer.place(x=500,y=25)

        self.dealer_draw_label = Label(master,text="Dealer drew:",bg="black",fg="white",font="Times 10")
        self.dealer_draw_label.place(x=400,y=295)

        self.dealer_sum_label = Label(master,text="Dealer's Total:",bg="black",fg="white",font="Times 10")
        self.dealer_sum_label.place(x=400,y=315)

        self.player_draw_label = Label(master,text="You drew:",bg="black",fg="white",font="Times 10")
        self.player_draw_label.place(x=25,y=295)

        self.player_sum_label = Label(master,text="Your total:",bg="black",fg="white",font="Times 10")
        self.player_sum_label.place(x=25,y=315)

        self.label_money = Label(master,text="You have: $%s" % self.player_money,font= "Times 16 bold italic", bg="white",fg="red")
        self.label_money.place(x=220,y=20)

        self.label_wage = Label(master, text="Enter numerical chip amounts:",font= "Times 9 italic", bg="white",fg="red")
        self.label_wage.place(x=240,y=50)

        self.label_instructions = Label(master, text="Instructions:",font = "Times 12 bold",bg="white")
        self.label_instructions.place(x=25,y=100)

        self.label_instructions1 = Label(master, text="1. Enter numerical chip amounts in the  ",font = "Times 10",bg="white")
        self.label_instructions1.place(x=25,y=120)

        self.label_instructions2 = Label(master, text="     grey boxes under their respective values",font = "Times 10",bg="white")
        self.label_instructions2.place(x=25,y=140)
        
        self.label_instructions3 = Label(master, text="2. Click BET to confirm bet amount",font = "Times 10",bg="white")
        self.label_instructions3.place(x=25,y=160)

        self.label_instructions4 = Label(master, text="3. Click DEAL to start game!",font = "Times 10",bg="white")
        self.label_instructions4.place(x=25,y=180)
        
        self.label_instructions5 = Label(master, text="4. Good Luck!",font = "Times 10",bg="white")
        self.label_instructions5.place(x=25,y=200)



        #Frames to hold cards, draws, and sums
        self.cards_dealerframe = Frame(master,bg="black")
        self.cards_dealerframe.place(x=425,y=75)

        self.cards_playerframe = Frame(master,bg="black")
        self.cards_playerframe.place(x=25,y=75)

        
        #Buttons
        self.deal_button = Button(master, text="DEAL",font= "Times 9 italic", bg="white",fg="green",activebackground="gray", command=self.deal,state='disabled')
        self.deal_button.place(x=75,y=340)

        self.hit_button = Button(master, text="HIT",font= "Times 9 italic", bg="white",fg="blue",activebackground="gray", command=self.hit, state='disabled')
        self.hit_button.place(x=320,y=340)

        self.stand_button = Button(master,text="STAND",font= "Times 9 italic", bg="white",fg="red",activebackground="gray", command=self.stand,state='disabled')
        self.stand_button.place(x=550,y=340)

        self.bet_button = Button(master,text="BET",font= "Times 20 italic", bg="white",fg="purple",activebackground="gray", command=self.bet,state='normal')
        self.bet_button.place(x=200,y=220)
      

        #entry
        self.bet_entry10 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry10.place(x=377,y=160)

        self.bet_entry20 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry20.place(x=481,y=160)

        self.bet_entry50 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry50.place(x=585,y=160)

        self.bet_entry100 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry100.place(x=377,y=255)

        self.bet_entry500 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry500.place(x=481,y=255)

        self.bet_entry1000 = Entry(master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry1000.place(x=585,y=255)

    #betting system
    def bet(self):
        global bet
        
        bet10=self.bet_entry10.get()
        bet20=self.bet_entry20.get()
        bet50=self.bet_entry50.get()
        bet100=self.bet_entry100.get()
        bet500=self.bet_entry500.get()
        bet1000=self.bet_entry1000.get()

        if len(self.bet_entry10.get())!=0:
          self.player_bet+=int(bet10)*10

        if len(self.bet_entry20.get())!=0:
          self.player_bet+=int(bet20)*20

        if len(self.bet_entry50.get())!=0:
          self.player_bet+=int(bet50)*50

        if len(self.bet_entry100.get())!=0:
          self.player_bet+=int(bet100)*100

        if len(self.bet_entry500.get())!=0:
          self.player_bet+=int(bet500)*500

        if len(self.bet_entry1000.get())!=0:
          self.player_bet+=int(bet1000)*1000

        bet=self.player_bet
        
        #result of inputted bet
        if int(bet) > self.player_money:
          self.label_wage.config(text="Exceeded balance")
          self.player_bet=0
        elif int(bet)==0:
          self.label_wage.config(text="Cannot bet $0")
        elif int(bet) <= self.player_money:
          self.deal_button.config(state='normal')
          self.bet_button.config(state='disabled')
          
         
          self.label_wage.config(text="You bet: $%s" % bet)
          self.label_money.config(text="You have: $%s" % self.player_money)

          #destroy buttons and continue with game
          self.bet_entry10.destroy()
          self.bet_entry20.destroy()
          self.bet_entry50.destroy()
          self.bet_entry100.destroy()
          self.bet_entry500.destroy()
          self.bet_entry1000.destroy()
          self.bet_button.destroy()
          self.chips.destroy()
    
    #user presses quit
    def quit(self):
        self.newWindow = Toplevel(self.master,height=420, width=860)
        self.app = Over(self.newWindow)
        root.after(1000,self.quit2)

    #aim lab game begins
    def quit2(self):
      #destroy everything
        self.quit_button.destroy()
        self.hit_button.destroy()
        self.deal_button.destroy()
        self.stand_button.destroy()
        self.bet_entry10.destroy()
        self.bet_entry20.destroy()
        self.bet_entry50.destroy()
        self.bet_entry100.destroy()
        self.bet_entry500.destroy()
        self.bet_entry1000.destroy()
        self.bet_button.destroy()
        self.chips.destroy()
        self.label_player.destroy()
        self.label_dealer.destroy()
        self.dealer_draw_label.destroy()
        self.dealer_sum_label.destroy()
        self.player_draw_label.destroy()
        self.player_sum_label.destroy()
        self.label_money.destroy()
        self.label_wage.destroy()         
        self.label_instructions.destroy()
        self.label_instructions1.destroy()
        self.label_instructions2.destroy()
        self.label_instructions3.destroy()
        self.label_instructions4.destroy()
        self.label_instructions5.destroy()

        self.quit_button = Button(self.master, text="QUIT",font= "Times 9 italic", bg="white",fg="brown",activebackground="gray", command=self.quit1, state='normal')

        self.label_lose = Label(self.master, text="Welcome to AIM LAB", font="Times 16 italic bold", bg="black", fg="red")
        self.label_lose.place(x=200,y=170)
        self.label_lose.after(8000,self.label_lose.destroy)

        #quit button moves around
        def move(x,y):
          if x<660:
            self.hit_button           
            self.quit_button.place(x=x, y=y)
            self.quit_button.after(435, lambda: move(random.randint(1,630),random.randint(1,360))) #after every 435ms, quit button moves
              
        move(0,0)
    #actual quit
    def quit1(self):
        self.newWindow = Toplevel(self.master,height=420, width=860)
        self.app = End(self.newWindow,self.player_money,self.player_winnings)
        
      
    #two cards dealt to both dealer and player
    def deal(self):
        self.deal_button.config(state='disabled')
        self.hit_button.config(state='normal')
        self.stand_button.config(state='normal')

        self.label_instructions.destroy()
        self.label_instructions1.destroy()
        self.label_instructions2.destroy()
        self.label_instructions3.destroy()
        self.label_instructions4.destroy()
        self.label_instructions5.destroy()

        #give dealer cards
        #first card
        new = self.deck[0]
        if new.value > 10:
          self.dealer_sum = 10
          if new.value==11:
            c1="Jack"
          elif new.value==12:
            c1="Queen"
          elif new.value==13:
            c1="King"
        if new.value <= 10:
          self.dealer_sum = new.value
          c1=str(new.value)
        if new.value == 1: 
          self.dealer_sum = 11
          c1 = "Ace" 
        self.dealer_hand.append(new)
        self.deck.pop(0)

        #show image of card
        photo = PhotoImage(file=new.filename)
        new.label = Label(self.cards_dealerframe, image=photo,bg="black")      
        new.label.photo = photo
        new.label.grid(row=0,column=self.dealer_hand.index(new))

        #second card
        new = self.deck[0]
        if new.value >= 10:
          self.dealer_sum += 10
        if new.value < 10 and new.value != 1:
          self.dealer_sum += new.value
        if new.value == 1 and self.dealer_sum + 11 <= 21:
          self.dealer_sum += 11
        elif new.value == 1:
          self.dealer_sum += 1
        self.dealer_hand.append(new)
        self.deck.pop(0)
        
        #show image of card
        photo = PhotoImage(file="back.png")
        new.label = Label(self.cards_dealerframe, image=photo,bg="black")      
        new.label.photo = photo
        new.label.grid(row=0,column=self.dealer_hand.index(new))

        self.dealer_draw_label.config(text="Dealer drew: %s and hidden" % c1)
        self.dealer_sum_label.config(text="Dealer's total: Unknown")

        #give player cards
        #first card
        new = self.deck[0]
        if new.value > 10:
          self.player_sum = 10
          if new.value==11:
            c1="Jack"
          elif new.value==12:
            c1="Queen"
          elif new.value==13:
            c1="King"
        if new.value <= 10:
          self.player_sum = new.value
          c1=str(new.value)
        if new.value == 1: 
          self.player_sum = 11
          c1 = "Ace"
        

        self.player_hand.append(new)
        self.deck.pop(0)

        #show image of card
        photo = PhotoImage(file=new.filename)
        new.label = Label(self.cards_playerframe, image=photo,bg="black")      
        new.label.photo = photo
        new.label.grid(row=0,column=self.player_hand.index(new))

        #second card
        new = self.deck[0]
        if new.value >= 10:
          self.player_sum += 10
          if new.value==10:
            c2=str(10)
          if new.value==11:
            c2="Jack"
          elif new.value==12:
            c2="Queen"
          elif new.value==13:
            c2="King"
        if new.value < 10 and new.value != 1:
          self.player_sum += new.value
          c2=str(new.value)
        if new.value == 1 and self.player_sum + 11 <= 21:
          self.player_sum += 11
          c2= "Ace"
        elif new.value == 1:
          self.player_sum += 1
          c2 = "Ace"
        self.player_hand.append(new)
        self.deck.pop(0)   
        
        #show image of card
        photo = PhotoImage(file=new.filename)
        new.label = Label(self.cards_playerframe, image=photo,bg="black")      
        new.label.photo = photo
        new.label.grid(row=0,column=self.player_hand.index(new))
        
        self.player_draw_label.config(text="You drew: %s and %s" % (c1,c2))
        self.player_sum_label.config(text="Your total: %d" % self.player_sum)

    #hit function
    def hit(self):
        #add a new card to hand
        #c3 is what the player drew depending on what new.value is 
        new = self.deck[0]
        if new.value >= 10:
          self.player_sum += 10
          if new.value==10:
            c3=str(10)
          if new.value==11:
            c3="Jack"
          elif new.value==12:
            c3="Queen"
          elif new.value==13:
            c3="King"
        if new.value < 10 and new.value != 1:
          self.player_sum += new.value
          c3=str(new.value)
        if new.value == 1 and self.player_sum + 11 <= 21:
          self.player_sum += 11
          c3= "Ace"
        elif new.value == 1:
          self.player_sum += 1
          c3 = "Ace"
        self.player_hand.append(new)
        self.deck.pop(0)   
      
        #show image of card
        photo = PhotoImage(file=new.filename)
        new.label = Label(self.cards_playerframe, image=photo,bg="black")
        new.label.photo = photo
        #alignment of cards
        if self.player_hand.index(new)==3:
          new.label.grid(row=1,column=0)
        elif self.player_hand.index(new)==4:
          new.label.grid(row=1,column=1)
        elif self.player_hand.index(new)==5:
          new.label.grid(row=1,column=2)
        else:
          new.label.grid(row=0,column=self.player_hand.index(new))
       
        self.player_draw_label.config(text="You drew: %s" % c3)
        self.player_sum_label.config(text="Your total: %d" % self.player_sum)

        #player loses
        if self.player_sum > 21:
            self.deal_button.config(state='disabled')
            self.hit_button.config(state='disabled')
            self.stand_button.config(state='disabled')
            self.player_money -= int(bet)
            self.player_winnings -=int(bet)
            
            root.after(1500, self.losescreen)
            root.after(4000, self.reset)

    #loss screen        
    def losescreen(self):
        self.newWindow = Toplevel(self.master,height=420, width=860)
        self.app = Lose(self.newWindow,0)

    #stand function
    def stand(self):
        
        self.deal_button.config(state='disabled')
        self.hit_button.config(state='disabled')
        self.stand_button.config(state='disabled')

        #reveal hidden card
        hidden = self.dealer_hand[1]
        photo = PhotoImage(file=hidden.filename)
        hidden.label = Label(self.cards_dealerframe, image=photo,bg="black")   
        hidden.label.photo = photo
        hidden.label.grid(row=0,column=self.dealer_hand.index(hidden))

        #c3 is dealer's first card
        if self.dealer_hand[0].value == 13:
          c3 = "King"
        elif self.dealer_hand[0].value == 12:
          c3 = "Queen"
        elif self.dealer_hand[0].value == 11:
          c3 = "Jack"
        elif self.dealer_hand[0].value == 1:
          c3 = "Ace"
        else:
          c3 = str(self.dealer_hand[0].value)

        #c4 is dealer's second card
        if self.dealer_hand[1].value == 13:
          c4 = "King"
        elif self.dealer_hand[1].value == 12:
          c4 = "Queen"
        elif self.dealer_hand[1].value == 11:
          c4 = "Jack"
        elif self.dealer_hand[1].value == 1:
          c4 = "Ace"
        else:
          c4 = str(self.dealer_hand[1].value)

        self.dealer_draw_label.config(text="Dealer drew: %s and %s" %(c3,c4))
        self.dealer_sum_label.config(text="Dealer's total: %s" %(self.dealer_sum) )  
        
        root.after(2000, self.dealer_hit)

        
    #dealer hit function    
    def dealer_hit(self):
        global bet1
        #dealer wins

        if self.dealer_sum > self.player_sum and self.dealer_sum <= 21:
            self.player_money -= int(bet)
            self.player_winnings -= int(bet)
            self.newWindow = Toplevel(self.master,height=420, width=860)
            self.app = Lose(self.newWindow,1)
            root.after(4000, self.reset)
        
        #dealer wins
        elif self.dealer_sum == self.player_sum and self.dealer_sum <= 21:
            self.player_money -= int(bet)
            self.player_winnings -= int(bet)
            self.newWindow = Toplevel(self.master,height=420, width=860)
            self.app = Lose(self.newWindow,2)
            root.after(4000, self.reset)

        #dealer loses        
        elif self.dealer_sum > 21:
            bet1=int(self.player_money)+int(bet)
            self.player_winnings+=int(bet)
            self.player_win=int(bet)
            self.player_money=bet1
            
            self.newWindow = Toplevel(self.master,height=420, width=860)
            self.app = Win(self.newWindow,self.player_win)

            self.label_wage.destroy()
            self.label_money.config(text="You have: $%s" % bet1)
            root.after(4000, self.reset)
            
        #dealer draws new card        
        else:
          new = self.deck[0]
          if new.value >= 10:
            self.dealer_sum += 10
            if new.value==10:
              c3=str(10)
            if new.value==11:
              c3="Jack"
            elif new.value==12:
              c3="Queen"
            elif new.value==13:
              c3="King"
          if new.value < 10 and new.value != 1:
            self.dealer_sum += new.value
            c3=str(new.value)
          if new.value == 1 and self.player_sum + 11 <= 21:
            self.dealer_sum += 11
            c3= "Ace"
          elif new.value == 1:
            self.dealer_sum += 1
            c3 = "Ace"
          self.dealer_hand.append(new)
          self.deck.pop(0)   
        
          #show image of new card
          photo = PhotoImage(file=new.filename)
          new.label = Label(self.cards_dealerframe, image=photo,bg="black")    
          new.label.photo = photo

          #dealer cards alignment
          if self.dealer_hand.index(new)==3:
            new.label.grid(row=1,column=0)
          elif self.dealer_hand.index(new)==4:
            new.label.grid(row=1,column=1)
          elif self.dealer_hand.index(new)==5:
            new.label.grid(row=1,column=2)
          else:
            new.label.grid(row=0,column=self.dealer_hand.index(new))
        
          self.dealer_draw_label.config(text="Dealer drew: %s" % c3)
          self.dealer_sum_label.config(text="Dealer's Total: %s" % self.dealer_sum)
          root.after(2000, self.dealer_hit)

    #reset game function   
    def reset(self):
      
        #player doesn't have enough money to play anymore
        if self.player_money < 10:
          self.newWindow = Toplevel(self.master,height=420, width=860)
          self.app = End(self.newWindow,self.player_money,self.player_winnings)
          

        #Create background image and essentially window size
        img = PhotoImage(file="bj.png")
        self.background = Label(self.master,image=img,height=400, width=680)
        self.background.photo = img
        self.background.grid(row=0, column=0)

        #recreating chips images
        img2 = PhotoImage(file="chipsp.png")
        self.chips = Label(self.master,image=img2)
        self.chips.photo = img2
        self.chips.place(x=350, y=75)

        #resetting variables to orginal
        self.player_hand = []
        self.dealer_hand = []
        self.deck = []
        self.player_sum = 0
        self.dealer_sum = 0
        self.player_bet=0
        

        #recreating deck
        for letter in ["C","D","S","H"]:
          for number in range(1,14): 
            filename = "cards//%s%s.png" % (number,letter)
            value = number
            #add all cards to deck with their file name and value and shuffle the deck
            self.deck.append(card(filename,value))

        random.shuffle(self.deck)

        #recreating titles
        self.label_player = Label(self.master, text="Your Cards",font = "Times 12 bold",bg="white")
        self.label_player.place(x=70,y=25)

        self.label_dealer = Label(self.master, text="Dealer's Cards",font = "Times 12 bold", bg="white")
        self.label_dealer.place(x=500,y=25)

        #recreating labels
        self.dealer_draw_label = Label(self.master,text="Dealer drew:",bg="black",fg="white",font="Times 10")
        self.dealer_draw_label.place(x=400,y=295)

        self.dealer_sum_label = Label(self.master,text="Dealer's Total:",bg="black",fg="white",font="Times 10")
        self.dealer_sum_label.place(x=400,y=315)

        self.player_draw_label = Label(self.master,text="You drew:",bg="black",fg="white",font="Times 10")
        self.player_draw_label.place(x=25,y=295)

        self.player_sum_label = Label(self.master,text="Your total:",bg="black",fg="white",font="Times 10")
        self.player_sum_label.place(x=25,y=315)

        self.label_money = Label(self.master,text="You have: $%s" % self.player_money,font= "Times 18 bold italic", bg="white",fg="red")
        self.label_money.place(x=230,y=20)

        self.label_wage = Label(self.master, text="Enter numerical chip amounts:",font= "Times 9 italic", bg="white",fg="red")
        self.label_wage.place(x=250,y=50)

        self.label_instructions = Label(self.master, text="Instructions:",font = "Times 12 bold",bg="white")
        self.label_instructions.place(x=25,y=100)

        self.label_instructions1 = Label(self.master, text="1. Enter numerical chip amounts in the",font = "Times 10",bg="white")
        self.label_instructions1.place(x=25,y=120)

        self.label_instructions2 = Label(self.master, text="     grey boxes under their respective values",font = "Times 10",bg="white")
        self.label_instructions2.place(x=25,y=140)
        
        self.label_instructions3 = Label(self.master, text="2. Click BET to confirm bet amount",font = "Times 10",bg="white")
        self.label_instructions3.place(x=25,y=160)

        self.label_instructions4 = Label(self.master, text="3. Click DEAL to start game!",font = "Times 10",bg="white")
        self.label_instructions4.place(x=25,y=180)
        
        self.label_instructions5 = Label(self.master, text="4. Click QUIT to exit",font = "Times 10",bg="white")
        self.label_instructions5.place(x=25,y=200)

        #recreating frames to hold cards, draws, and sums
        self.cards_dealerframe = Frame(self.master,bg="black")
        self.cards_dealerframe.place(x=425,y=75)

        self.cards_playerframe = Frame(self.master,bg="black")
        self.cards_playerframe.place(x=25,y=75)

    
        #recreating buttons
        self.deal_button = Button(self.master, text="DEAL",font= "Times 9 italic", bg="white",fg="green",activebackground="gray", command=self.deal,state="disabled")
        self.deal_button.place(x=75,y=340)

        self.hit_button = Button(self.master, text="HIT",font= "Times 9 italic", bg="white",fg="blue",activebackground="gray", command=self.hit, state='disabled')
        self.hit_button.place(x=320,y=340)

        self.stand_button = Button(self.master,text="STAND",font= "Times 9 italic", bg="white",fg="red",activebackground="gray", command=self.stand,state='disabled')
        self.stand_button.place(x=550,y=340)

        self.bet_button = Button(self.master,text="BET",font= "Times 20 italic", bg="white",fg="purple",activebackground="gray", command=self.bet,state='normal')
        self.bet_button.place(x=200,y=220)

        self.quit_button = Button(self.master, text="QUIT",font= "Times 9 italic", bg="white",fg="brown",activebackground="gray", command=self.quit, state='normal')
        self.quit_button.place(x=315,y=300)
        
        
        #recreating entry
        self.bet_entry10 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry10.place(x=377,y=160)

        self.bet_entry20 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry20.place(x=481,y=160)

        self.bet_entry50 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry50.place(x=585,y=160)

        self.bet_entry100 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry100.place(x=377,y=255)

        self.bet_entry500 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry500.place(x=481,y=255)

        self.bet_entry1000 = Entry(self.master,bg="light gray",bd=2,font="Times 9 italic",fg="red",width=5)
        self.bet_entry1000.place(x=585,y=255)

root = Tk()
my_gui = Intro(root)
root.geometry("400x225")
root.config(cursor="plus")
root.mainloop()


