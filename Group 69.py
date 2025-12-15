import random
import datetime

#Text Files
STF=open("Show Timings.txt", "a+")                                                      #Show Timings File
TF=open("Issues.txt", "a+")                                                             #Issues File
ORF=open("Overall Report.txt", "a+")                                                    #Overall Report File
PF=open("Payment.txt", "a+")                                                            #Payment File
CPF=open("Cash Payment.txt", "a+")                                                      #Cash Payment File
UF=open("Users.txt", "a+")                                                              #User ID File
BF=open("Bookings.txt", "a+")                                                           #Bookings File
FF=open("Food.txt", "a+")                                                               #Online Food Orders File
RF=open("Rewards.txt", "a+")                                                            #Rewards File
FBF=open("Feedback.txt", "a+")                                                          #Feedback File

#Functions
#Cinema Manager
def AddC():                                                                             #Adding a Movie Listing
    cname=input("Enter Cinema Name : ").title()
    clang=input("Enter Cinema Language : ").title()
    sdate=input("Enter Date of the show (DD-MM-YYYY): ")
    stime=input("Enter Time of the show : ")
    clocation=input("Enter Cinema Location : ").title()
    hallno=int(input("Enter Hall Number : "))
    if hallno<=4:
        seatcount=120
    elif hallno>4:
        seatcount=100
    showid=Cinemaid()
    cn=cname
    cn={"Cinema Name":cname, "Cinema Language":clang, "Show Date":sdate, "Show Time":stime, "Cinema Location":clocation, 
        "Hall Number":hallno, "Seating Capacity":seatcount, "Seats Available":seatcount, "Show ID":showid}
    STF.write(str(cn) + "\n")                                                           #Writes the data into the text file

def UpdateC():                                                                          #Updating a Movie Listing
    STF.seek(0)
    lines = STF.readlines()
    shoid = input("Enter Cinema ID : ").strip()
    ul = []
    u = False
    for line in lines:
        if f"'Show ID': {shoid}" in line or f"'Show ID': '{shoid}'" in line:
            x = input("Enter What to Update : ").strip()
            up = input("Enter Updated Data : ").strip()
            if f"'{x}':" in line:
                parts = line.strip().strip("{}").split(",")                             #Find the field and update its value
                new_parts = []
                for part in parts:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        key_clean = key.strip().strip("'")
                        if key_clean == x:
                            new_parts.append(f"'{key_clean}': '{up}'")
                        else:
                            new_parts.append(f"{key.strip()}: {value.strip()}")
                new_line = "{" + ", ".join(new_parts) + "}\n"
                ul.append(new_line)
                print("Data Updated Successfully.")
                u = True
            else:
                print(f"Field '{x}' not found in record.")
                ul.append(line)
            continue
        else:
            ul.append(line)
    if not u:
        print("Specified Show ID does not exist.")
    STF.seek(0)
    STF.truncate()
    STF.writelines(ul)
    STF.flush()

def RemoveC():                                                                          #Removing a Movie Listing
    STF.seek(0)
    lines = STF.readlines()
    shoid = input("Enter Cinema ID : ").strip()
    new_lines = []
    removed = 0
    for line in lines:
        if f"'Show ID': {shoid}" in line or f"'Show ID': '{shoid}'" in line:
            print("Movie Listing removed successfully.")
            removed += 1
            continue
        new_lines.append(line.strip() + "\n")
    if removed == 0:
        print("Specified Show ID does not exist.")
    STF.seek(0)
    STF.truncate()
    STF.writelines(new_lines)
    STF.flush()

def Overall_Report():                                                                   #Overall Report
    ORF.seek(0)
    lines = ORF.readlines()
    for line in lines:
        print(line)

def OR_Payment(x):                                                                      #Payment Methods Used (Overall Report)
    ORF.seek(0)
    lines = ORF.readlines()
    updated = False
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("{") and ":" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            payment = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    try:
                        value = int(value.strip())
                    except:
                        value = 0
                    payment[key] = payment.get(key, 0) + value
            payment[x] = payment.get(x, 0) + 1
            lines[i] = "{" + ", ".join([f"'{k}': {payment[k]}" for k in payment]) + "}\n"
            updated = True
            break
    if not updated:
        lines.append(f"{{'{x}': 1}}\n")
    ORF.seek(0)
    ORF.truncate()
    ORF.writelines(lines)
    ORF.flush()

def cancel_OR_Payment(x):                                                               #Payment Methods Used (Overall Report) (After Cancellation)
    ORF.seek(0)
    lines = ORF.readlines()
    payment = {}
    for line in lines:
        if line.strip().startswith("{") and ":" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    try:
                        value = int(value.strip())
                    except:
                        value = 0
                    payment[key] = payment.get(key, 0) + value
    if x in payment and payment[x] > 0:
        payment[x] -= 1
    new_line = "{" + ", ".join([f"'{k}': {payment[k]}" for k in payment]) + "}\n"
    ORF.seek(0)
    ORF.truncate()
    ORF.write(new_line)
    ORF.flush()

def OR_Revenue(a):                                                                      #Total Revenue (Overall Report)
    ORF.seek(0)
    lines = ORF.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.strip().startswith("Total Revenue ="):
            try:
                cr = float(line.strip().split("=")[1].strip())
            except:
                cr = 0.0
            n = cr + a
            lines[i] = f"Total Revenue = {n:.2f}\n"
            break
    else:
        lines.append(f"Total Revenue = {a:.2f}\n")
    ORF.seek(0)
    ORF.truncate()
    ORF.writelines(lines)
    ORF.flush()

def cancel_OR_Revenue(a):                                                               #Total Revenue (Overall Report) (After Cancellation)
    ORF.seek(0)
    lines = ORF.readlines()
    PF.seek(0)
    lis = PF.readlines()
    ra = None
    for i in range(len(lis)):
        line = lis[i].strip()
        if f"'Payment ID': {a}" in line or f"'Payment ID': '{a}'" in line:
            # Extract Amount Paid
            parts = line.split(",")
            for part in parts:
                if "'Amount Paid':" in part:
                    try:
                        ra = int(part.split(":")[1].strip())
                    except:
                        ra = 0
                    break
            # Mark as refunded
            if "'Status':" in line:
                line = line.replace("'Status': 'Paid'", "'Status': 'Refunded.'")
            else:
                line += ", 'Status': 'Refunded.'"
            lis[i] = line + "\n"
            break
    if ra is not None:
        cancel_OR_Bookings(a)
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("Total Revenue ="):
                try:
                    current = int(line.split("=")[1].strip())
                except:
                    current = 0
                new_total = current - ra
                lines[i] = f"Total Revenue = {new_total}\n"
                break
    print("Your refund has been initiated.\n"
          "It will take up to 14 business days for the refund to reflect in your account, depending on your bank or payment provider.")
    PF.seek(0)
    PF.truncate()
    PF.writelines(lis)
    PF.flush()
    ORF.seek(0)
    ORF.truncate()
    ORF.writelines(lines)
    ORF.flush()

def OR_Bookings(a):                                                                     #Total Seats Booked (Overall Report)
    ORF.seek(0)
    lines = ORF.readlines()
    for i in range(0, len(lines)):
        line=lines[i]
        if line.strip().startswith("Total Seats Booked ="):
            try:
                cr = int(line.strip().split("=")[1].strip())
            except:
                cr= 0
            n = cr + a
            lines[i]= "Total Seats Booked = " + str(n) + "\n"
            break     
    else:
        lines.append("Total Seats Booked = " + str(a) + "\n")
    ORF.seek(0)
    ORF.truncate()
    ORF.writelines(lines)
    ORF.flush()

def cancel_OR_Bookings(a):                                                              #Total Seats Booked (Overall Report) (After Cancellation)
    ORF.seek(0)
    lines = ORF.readlines()
    PF.seek(0)
    lis = PF.readlines()
    x = 0  
    for line in lis:
        if f"'Payment ID': {a}" in line or f"'Payment ID': '{a}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            for part in parts:
                if "'Number of Seats':" in part:
                    try:
                        x = int(part.split(":")[1].strip())
                    except:
                        x = 0
                    break
            break
    if x > 0:
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("Total Seats Booked ="):
                try:
                    cr = int(line.split("=")[1].strip())
                except:
                    cr = 0
                n = cr - x
                lines[i] = f"Total Seats Booked = {n}\n"
                break
    ORF.seek(0)
    ORF.truncate()
    ORF.writelines(lines)
    ORF.flush()

def Pay(x):                                                                             #Payment
    print()
    if penal=="Yes":
        Penalty()                                                                       #Penalty Payment
    print("You have to Pay RM", x)                                                      #Payment Amount
    global PM                                                                           #For Booking
    co=0                                                                                #For Entering Correct Payment Method
    while co<3:
        PM=input("Enter Payment Method (Card/Online Banking/E-Wallet/Cash): ").title()
        if PM in ["Card", "Online Banking", "E-Wallet", "Cash"]:
            PD={}                                                                       #To Store Payment Details
            global Payid
            Payid=PayID()
            if PM=="Card":
                cc=0
                while cc<3:
                    CNo=input("Enter Card Number : ")
                    if len(CNo)!=16 or not CNo.isdigit():
                        print("Invalid Card Number. Please Try Again")
                        cc+=1
                    else:  
                        CNa=input("Enter Name on Card : ")
                        CV=input("Enter Card Valdity : ")
                        CCVV=input("Enter Card CVV Code : ")
                        PN=input("Enter 'Pay Now' to pay : ")
                        if PN=="Pay Now":
                            print("Payment Success")
                            PD["Card Number"]=CNo
                            PD["Card Holder's Name"]=CNa
                            PD["Card Validity"]=CV
                            PD["Amount Paid"]=x
                            if fo=="y":
                                PD["Food ID"]=foodid
                            PD["Status"]="Paid"
                            PD["Payment ID"]=Payid
                            PF.write(str(PD) + "\n")
                            cc+=3
                            co+=3
                        else:
                            print("Payment failed")
            elif PM=="Online Banking":
                OB=input("Enter Bank Name : ")
                print("Redirecting to Online Banking...")
                print("Enter your banking details (We do not store your banking details.)")
                un=input("Username ")
                pw=input("Password ")
                PN=input("Enter 'Pay Now' to pay : ")
                if PN=="Pay Now":
                    print("Payment Success")
                    PD["Bank Name"]=OB
                    PD["Amount Paid"]=x
                    if fo=="y":
                        PD["Food ID"]=foodid
                    PD["Payment ID"]=Payid
                    PD["Status"]="Paid"
                    PF.write(str(PD) + "\n")
                    co+=3
                else:
                    print("Payment failed")      
            elif PM=="E-Wallet":
                EW=input("Enter E-wallet Name : ")
                print("Redirecting to E-wallet site...")
                PN=input("Enter 'Pay Now' to pay : ")
                if PN=="Pay Now":
                    print("Payment Success")
                    PD["Ewallet Service Name"]=EW
                    PD["Amount Paid"]=x
                    if fo=="y":
                        PD["Food ID"]=foodid
                    PD["Payment ID"]=Payid
                    PD["Status"]="Paid"
                    PF.write(str(PD) + "\n")
                    co+=3
                else:
                    print("Payment failed")
            elif PM=="Cash":
                Cashid=PayID()
                TBP={}                                                                  #To Be Paid
                print("You have to walkin to your Cinema location to pay with Cash.")
                print("Use this Number to Pay at Counter : ", Cashid)
                TBP["Booked By"]=email
                TBP["Amount To Be Paid"]=x
                TBP["Number of Seats"]=nop
                TBP["Seats"]=seats
                if fo=="y":
                    TBP["Food ID"]=foodid
                TBP["Payment ID"]=Cashid
                TBP["Status"]="Not Paid"
                TBP["Show ID"]=mid
                CPF.write(str(TBP) + "\n")
                co+=3
            OR_Payment(PM)
        else:
            print("Enter a Valid Payment Method.")
            co+=1

def Price(x, y, z):                                                                     #Pricing For Cinema Tickets
    AdultP=20
    ChildP=15
    SaOP=15                                                                             #For Senior Citizens / OKU
    global TotalP
    TotalP=(x*AdultP)+(y*ChildP)+(z*SaOP)
    GST=6/100                                                                           #GST 6%
    GSTP=TotalP * GST
    TotalP=TotalP + GSTP
    print("Total Price to Pay : RM", TotalP)
    
def Discounts():                                                                        #Discount Codes for discount in price
    c=0
    while c<3:
        Dis=input("Enter Discount Code : ").upper()
        if Dis=="H":
            DisP=TotalP*(30/100)
            break
        elif Dis=="M":
            DisP=TotalP*(20/100)
            break
        elif Dis=="L":
            DisP=TotalP*(10/100)
            break
        else:
            print("Enter a valid discount code.")
            c+=1
    else:
        print("No Valid Code Entered.")
        return
    TotalP=TotalP-DisP
    print("Total Price After Discount :", TotalP)

def Food(mode):                                                                         #Food With Pricing (Inc GST)
    food={}
    global foodid                                                                       #For Receipt
    global FoodP
    FoodP=0
    foodid=FoodID()
    c=int(input("How many items do you want to order? "))
    if c <= 0:
        print("Please enter a positive number.")
        return
    elif mode=="Online" and c>nop:
        print("You cannot order food items more than the number of seats booked.")
        return
    count=1
    while count<=c:
        Table=("1. Popcorn Box (Regular/Large) \n" 
        "2. Combo Box (1 Popcorn box and 1 Drink) \n"
        "3. Drinks")
        print(Table)
        f=input("Please Enter the Number of The Item You want to choose : ")
        if f not in {"1", "2", "3"}:
            print("Invalid item number. Please try again.")
            return
        if f=="1":                                                                      #Only Popcorn
            spf=input("Select Flavour (Salted/Caramel/Mix) : ").strip().title()
            if spf not in ["Salted", "Caramel", "Mix"]:
                print("Enter a Valid Flavour.")
                return
            RoL=input("Regular or Large? ").strip().title()
            if RoL=="Regular":
                food["Food Item "+str(count)]=spf + " Regular Popcorn"
                FoodP+=13
            elif RoL=="Large":
                food["Food Item "+str(count)]=spf + " Large Popcorn"
                FoodP+=15
            else:
                print("Invalid, Please Try Again.")
        elif f=="2":                                                                    #Combo (Popcorn and Drink)
            spf=input("Select Flavour (Salted/Caramel/Mix) : ").strip().title()
            if spf not in ["Salted", "Caramel", "Mix"]:
                print("Enter a Valid Flavour.")
                return
            RoL=input("Regular or Large Popcorn? ").strip().title()
            if RoL=="Regular":
                food["Food Item "+str(count)]=spf + " Regular Popcorn"
                FoodP+=13
            elif RoL=="Large":
                food["Food Item "+str(count)]=spf + " Large Popcorn"
                FoodP+=15
            else:
                print("Invalid, Please Try Again.")
            TableD=("1. Coke / Sprite / Pepsi / A&W / Minute Maid Orange \n"
                "2. Milo / Tea / Coffee \n"
                "3. Water Bottle")
            print(TableD)
            Drink=input("Enter the Number of the Drink you want : ")
            if Drink=="1":
                D=input("Which Drink Do You Want? (Coke / Sprite / Pepsi / A&W / Minute Maid Orange) ").strip().title()
                RoL=input("Regular or Large? ").strip().title()
                if RoL=="Regular":
                    food["Drink Item "+str(count)]="Regular " + D
                    FoodP+= 6
                elif RoL=="Large":
                    food["Drink Item "+str(count)]="Large " + D
                    FoodP+=7
                else:
                    print("Invalid, Please Try Again.")
            elif Drink=="2":
                D=input("Which Drink Do You Want? (Milo / Tea / Coffee) ").strip().title()
                HoC=input("Hot or Iced? ").strip().title()
                if HoC=="Hot":
                    food["Drink Item "+str(count)]="Hot " + D
                    FoodP+=7
                elif HoC=="Iced":
                    food["Drink Item "+str(count)]="Iced " + D
                    FoodP+=7
                else:
                    print("Invalid, Please Try Again.")
            elif Drink=="3":
                RoL=input("Regular or Large? ").strip().title()
                if RoL=="Regular":
                    food["Drink Item "+str(count)]="Regular Water Bottle"
                    FoodP+=3
                elif RoL=="Large":
                    food["Drink Item "+str(count)]="Large Water Bottle"
                    FoodP+=4
                else:
                    print("Invalid, Please Try Again.")
            else:
                print("Invalid drink selection. Please try again.")
                return
        elif f=="3":                                                                    #Only Drink
            TableD=("1. Coke / Sprite / Pepsi / A&W / Minute Maid Orange \n"
                "2. Milo / Tea / Coffee \n"
                "3. Water Bottle")
            print(TableD)
            Drink=input("Enter the Number of the Drink you want : ")
            if Drink=="1":
                D=input("Which Drink Do You Want? (Coke / Sprite / Pepsi / A&W / Minute Maid Orange) ").strip().title()
                RoL=input("Regular or Large? ").strip().title()
                if RoL=="Regular":
                    food["Drink Item "+str(count)]="Regular " + D
                    FoodP+=6
                elif RoL=="Large":
                    food["Drink Item "+str(count)]="Large " + D
                    FoodP+=7
                else:
                    print("Invalid, Please Try Again.")
            elif Drink=="2":
                D=input("Which Drink Do You Want? (Milo / Tea / Coffee) ").strip().title()
                HoC=input("Hot or Iced? ").strip().title()
                if HoC=="Hot":
                    food["Drink Item "+str(count)]="Hot " + D
                    FoodP+=7
                elif HoC=="Iced":
                    food["Drink Item "+str(count)]="Iced " + D
                    FoodP+=7
                else:
                    print("Invalid, Please Try Again.")
            elif Drink=="3":
                RoL=input("Regular or Large? ").strip().title()
                if RoL=="Regular":
                    food["Drink Item "+str(count)]="Regular Water Bottle"
                    FoodP+=3
                elif RoL=="Large":
                    food["Drink Item "+str(count)]="Large Water Bottle"
                    FoodP+=4
                else:
                    print("Invalid, Please Try Again.")
            else:
                print("Invalid drink selection. Please try again.")
                return
        count+=1
    if not food:
        print("No valid food selected.")
        return
    if mode=="Online":
        global TotalP
        TotalP+=FoodP
    elif mode=="In Store":
        print("Total Amount : ", FoodP)
        food["Status"]="Collected"
        food["Collected At"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        OR_Revenue(FoodP)
    food["Ordered By"]=email
    food["Food ID"]=foodid
    FF.write(str(food) + "\n")

def Food_Collection():                                                              #Food Collection at Store
    FF.seek(0)
    lines = FF.readlines()
    fooid = input("Enter Food ID : ").strip()
    ul = []
    collected = False
    for line in lines:
        if f"'Food ID': {fooid}" in line or f"'Food ID': '{fooid}'" in line:
            print(line.strip())
            if "'Status':" in line:
                line = line.replace("'Status': 'Paid'", "'Status': 'Collected'")
                line = line.replace("'Status': 'Not Paid'", "'Status': 'Collected'")
            else:
                line = line.strip().rstrip("}") + f", 'Status': 'Collected'" + "}"
            if "'Collected At':" in line:
                parts = line.split("'Collected At':")
                line = parts[0].strip() + f"'Collected At': '{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}'" + "}"
            else:
                line = line.strip().rstrip("}") + f", 'Collected At': '{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}'" + "}"
            collected = True
            ul.append(line.strip() + "\n")
        else:
            ul.append(line.strip() + "\n")
    if not collected:
        print("No Food Orders Found.")
    FF.seek(0)
    FF.truncate()
    FF.writelines(ul)
    FF.flush()

def Pricing():                                                                          #Pricing table
    CPT="Cinema Ticket Pricing : \n"\
        "Adult (12years and Above) = RM20 \n"\
        "Childern (12years and Below) = RM15 \n"\
        "Senior Citizens/OKU = RM15 \n"
    FPT="Food Items Pricing : \n"\
        "Popcorn (Regular/Large) = RM13 ~ RM15 \n"\
        "Soft Drinks (Regular/Large) = RM6 ~ RM7 \n"\
        "Milo/Tea/Coffee (Hot/Iced) = RM7"
    print(CPT)
    print(FPT)

def Feedback():                                                                         #Feedback
    feedback={}
    print("We Value Your Feedback. Please Rate Your Booking and leave a comment.")
    r=input("Rate Us Out of 5 Stars : ")
    comment=input("Comment : ")
    feedback["Feedback By"]=email
    feedback["Rating"]=r
    feedback["Comments"]=comment
    FBF.write(str(feedback) + "\n")

def Feedback_read():                                                                    #Displaying Feedbacks
    FBF.seek(0)
    lines=FBF.read()
    print(lines)

#Technician
def rewards(em, r):                                                                     #Giving a Discount to user for facing technical issue during screening
    RF.seek(0)
    lines = RF.readlines()
    fr = 0
    for line in lines:
        if f"'Email': '{em}'" in line or f"'Email': {em}" in line:
            if "'Rewards': 'No'" in line:
                fr += 1
    reward = f"'Email': '{em}', 'Rewards': '{r}'"
    if r == "No":
        if fr + 1 > 5:
            reward += ", 'Penalty': 'Yes'"
        else:
            reward += ", 'Penalty': 'No'"
    RF.seek(0)
    RF.truncate()
    RF.writelines([line.strip() + "\n" for line in lines])
    RF.write("{" + reward + "}\n")
    RF.flush()

def rewards_read(email):                                                                #Reading Rewards File After User Login
    RF.seek(0)
    lines = RF.readlines()
    global penal
    penal = "No"
    for line in lines:
        if f"'Email': '{email}'" in line or f"'Email': {email}" in line:
            if "'Rewards': 'Yes'" in line:
                print("------------------------------------------------------------------ \n"
                      " You Have A Discount Code For Reporting A Recent Technical Issue. \n"
                      "       Use The Code 'H' On Your Next Ticket Purchase. \n"
                      "------------------------------------------------------------------ \n")
            elif "'Penalty': 'Yes'" in line:
                penal = "Yes"
                print("------------------------------------------------------------------ \n"
                      "     You Have Exceeded The Limit for False Technical Reports.\n"
                      " 	   A Penalty will Be Applied To Your Next Booking.\n"
                      "------------------------------------------------------------------ \n")
            elif "'Penalty': 'No'" in line:
                penal = "No"
            break

def Penalty():                                                                          #Penalty Payment (For False Issue Reporting)
    penalty=50
    TotalP=TotalP+penalty
    print("Your Penalty Has Been Added.")
    print("Total Amount : RM", TotalP)

def Technical_Issue():                                                                  #To report any technical issue faced during Screening Time
    TP={}
    count=0
    while count<3:
        ti=input("Describe the Technical Issue : ")
        if not ti.strip():
            print("Technical Issue cannot be empty.")
            count+=1
        else:
            break
    else:
        print("Too Many Failed Attempts.")
        return
    c=0
    while c<3:
        cid=input("Enter the Cinema ID (Given in your receipt text file) : ")
        if cid.isdigit():
            break
        else:
            print("Cinema ID Must Be A Number.")
            c+=1
    else:
        print("Too Many Failed Attempts.")
        return
    toi=input("Enter the Time of when Issue started : ")
    issueid=IssueID()
    TP["Reported by"]=email
    TP["Technical Issue"]=ti
    TP["Time of Issue"]=toi
    TP["Cinema ID"]=cid
    TP["Issue ID"]=issueid
    TP["Current"]="Not Fixed"
    TF.write(str(TP) + "\n")
    
def Technir():                                                                          #Reading Technical Issues File
    TF.seek(0)
    lines = TF.readlines()
    for line in lines:
        print(line.strip())
        
def Techniw():                                                                          #Updating Technical Issues File
    Technir()
    TF.seek(0)
    lines = TF.readlines()
    iid = input("Enter the Issue ID of the issue you want to update : ").strip()
    p = input("1. Update an Issue. \n"
              "2. Issue Fixed. \n"
              "3. No Issue. \n"
              "Enter the Operation Number : ").strip()
    ts = datetime.datetime.now().strftime("%d-%m-%Y")
    updated_lines = []
    for line in lines:
        if f"'Issue ID': {iid}" in line or f"'Issue ID': '{iid}'" in line:
            em = ""
            parts = line.replace("{", "").replace("}", "").split(",")
            for part in parts:
                if "'Reported By':" in part:
                    em = part.split(":")[1].strip().strip("'")
                    break
            if p == "1":
                x = input("Enter What to Update : ").strip()
                if f"'{x}':" not in line:
                    print("Invalid field name.")
                    updated_lines.append(line.strip() + "\n")
                    continue
                up = input("Enter Updated Data : ").strip()
                new_parts = []
                for part in parts:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        key_clean = key.strip().strip("'")
                        if key_clean == x:
                            new_parts.append(f"'{key_clean}': '{up}'")
                        else:
                            new_parts.append(f"{key.strip()}: {value.strip()}")
                new_parts.append(f"'Last Updated': '{ts}'")
                new_line = "{" + ", ".join(new_parts) + "}\n"
                updated_lines.append(new_line)
                print("Data Updated Successfully.")
            elif p == "2":
                line = line.strip().rstrip("}")
                if "'Status':" in line:
                    line = line.replace("'Status': 'Pending'", "'Status': 'Fixed'")
                else:
                    line += ", 'Status': 'Fixed'"
                line += f", 'Last Updated': '{ts}'" + "}"
                updated_lines.append(line + "\n")
                rewards(em, "Yes")
                print("Data Updated Successfully.")
            elif p == "3":
                line = line.strip().rstrip("}")
                if "'Status':" in line:
                    line = line.replace("'Status': 'Pending'", "'Status': 'No Issue'")
                else:
                    line += ", 'Status': 'No Issue'"
                line += f", 'Last Updated': '{ts}'" + "}"
                updated_lines.append(line + "\n")
                rewards(em, "No")
            continue
        else:
            updated_lines.append(line.strip() + "\n")
    if lines == updated_lines:
        print("Specified ID Doesn't Exist.")
    TF.seek(0)
    TF.truncate()
    TF.writelines(updated_lines)
    TF.flush()

#Customer
def load_users():                                                                       #Loading Users File
    global users
    UF.seek(0)
    users = [line.strip() for line in UF.readlines()]

def login():                                                                            #User Login
    load_users()
    print()
    global email
    email = input("Enter Your Email : ").strip().lower()
    if email.endswith("gmail.com") or email.endswith("yahoo.com"):
        for line in users:
            if f"'Email': '{email}'" in line or f"'Email': {email}" in line:
                parts = line.replace("{", "").replace("}", "").split(",")
                user_data = {}
                for part in parts:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        key = key.strip().strip("'").strip('"')
                        value = value.strip().strip("'").strip('"')
                        user_data[key] = value
                count = 1
                while count <= 3:
                    password = input("Enter Password : ").strip()
                    if not password:
                        print("Password cannot be empty.")
                        continue
                    elif len(password) < 6:
                        print("Password must be at least 6 characters.")
                        continue
                    elif user_data.get("Password") == password:
                        print("Login Successful.")
                        return True
                    else:
                        print("Password is wrong.")
                        count += 1
                print("Too many attempts. Please Try again later.")
                return False
        print("No Profile Found with this Email.")
        nu = input("Do You Want To Create A New Account? (Y/N) ").lower()
        if nu == "y":
            new_user()
        elif nu == "n":
            return False
        else:
            print("Session Terminated, Did not Enter A Valid Option.")
            return False
    else:
        print("Enter a valid Email ID.")
        return False

def new_user():                                                                         #New User Login
    load_users()
    user_email = input("Enter Your Email : ").strip().lower()
    if user_email.endswith("gmail.com") or user_email.endswith("yahoo.com"):
        for line in users:
            if f"'Email': '{user_email}'" in line or f"'Email': {user_email}" in line:  #Checking if Email already Exists
                print("Email Already Exists.")
                return
        i = 1
        while i <= 3:
            password = input("Enter Password : ").strip()
            rpassword = input("Re-enter Password : ").strip()

            if len(password) < 6:
                print("Password must be at least 6 characters.")
                i+=1
            if password == rpassword:
                entry = f"{{'Email': '{user_email}', 'Password': '{password}'}}\n"
                UF.seek(0, 2)
                UF.write(entry)
                UF.flush()
                print("Account has been Created.")
                return
            else:
                print("Passwords aren't matching.")
                i += 1
        print("Too many attempts. Please Try again later.")
    else:
        print("Enter a valid Email ID.")

def display_movies():                                                                   #Displaying Movies
    print()
    STF.seek(0)
    lines = STF.readlines()
    global date
    date = input("Enter Movie Date (DD-MM-YYYY) : ").strip()
    for line in lines:
        if f"'Show Date': '{date}'" in line or f"'Show Date': {date}" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            for part in parts:
                if "'Seats Available':" in part:
                    try:
                        seats = int(part.split(":")[1].strip().strip("'").strip('"'))
                    except:
                        seats = 0
                    if seats > 0:
                        print(line.strip())
                    break

def Booking_seatlayout():                                                               #Booking Seats
    print()
    layouts = {}
    STF.seek(0)
    lines = STF.readlines()
    for line in lines:
        if f"'Show ID': {mid}" in line or f"'Show ID': '{mid}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            cn = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    cn[key] = value
            mn = cn.get("Cinema Name")
            capacity = int(cn.get("Seating Capacity", "0"))
            try:
                with open("Seats.txt", "r") as SF:
                    for li in SF:
                        if ":" in li:
                            fmd, layout = li.strip().split(":", 1)
                            layouts[fmd] = list(layout)
            except FileNotFoundError:
                pass
            if mid not in layouts:
                layouts[mid] = ["O"] * capacity

            # Displaying layout
            print(f"\n--- Seat Layout for {mn} --- \n")
            layout = layouts[mid]
            for row_num in range(0, len(layout), 10):
                row = layout[row_num:row_num + 10]
                row_label = chr(65 + row_num // 10)
                row_display = [f"{row_label}{j+1}:{seat}" for j, seat in enumerate(row)]
                print("  ".join(row_display))
            print("-------------------------- SCREEN -------------------------")

            # Booking seats
            count = 0
            while count < 3:
                global seats
                raw = input("Enter Seat Numbers (Eg Format : A1,B3,C10) : ").strip()
                seats = [s.strip().upper() for s in raw.split(",") if s.strip()]
                if not seats:
                    print("Input must contain seat labels.")
                    count += 1
                    continue
                if len(set(seats)) != len(seats):
                    print("Duplicate seat entries detected.")
                    count += 1
                    continue
                if len(seats) == nop:
                    valid = True
                    for s in seats:
                        if not (len(s) >= 2 and s[0].isalpha() and s[1:].isdigit()):
                            print(f"Invalid seat format: {s}")
                            valid = False
                            break
                        row = ord(s[0].upper()) - 65
                        col = int(s[1:]) - 1
                        index = row * 10 + col
                        if index < 0 or index >= len(layout):
                            print(f"Seat {s} is out of range.")
                            valid = False
                            break
                        if layout[index] != "O":
                            print(f"Seat {s} is already booked.")
                            valid = False
                            break
                    if valid:
                        for s in seats:
                            row = ord(s[0].upper()) - 65
                            col = int(s[1:]) - 1
                            index = row * 10 + col
                            layout[index] = "X"
                        with open("Seats.txt", "w") as SF:
                            for fmn, layout in layouts.items():
                                SF.write(f"{fmn}:{''.join(layout)}\n")
                        break
                    else:
                        count += 1
                elif len(seats) < nop:
                    print(f"You Have To Select {nop - len(seats)} More Seat(s).")
                    count += 1
                elif len(seats) > nop:
                    print(f"You Selected {len(seats) - nop} More Seat(s).")
                    count += 1
            return

def seats_available(mid):                                                               #Updating Seats Available
    STF.seek(0)
    lines = STF.readlines()
    updated_lines = []
    for line in lines:
        if f"'Show ID': {mid}" in line or f"'Show ID': '{mid}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            movie = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    movie[key] = value
            try:
                seats_avail = int(movie.get("Seats Available", "0"))
            except:
                seats_avail = 0
            if seats_avail < nop:
                print("Not Enough Seats Available.")
            else:
                seats_avail -= nop
                movie["Seats Available"] = str(seats_avail)
                new_line = "{" + ", ".join([f"'{k}': '{movie[k]}'" for k in movie]) + "}\n"
                updated_lines.append(new_line)
                Booking_seatlayout()
            continue
        else:
            updated_lines.append(line.strip() + "\n")
    STF.seek(0)
    STF.truncate()
    STF.writelines(updated_lines)
    STF.flush()

def cancel_seats_available(x, y):                                                       #Updating Seats Available (After Cancellation)
    STF.seek(0)
    lines = STF.readlines()
    ul=[]
    for line in lines:
        if f"'Show ID': {x}" in line or f"'Show ID': '{x}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            movie = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    movie[key] = value
            try:
                seats_avail = int(movie.get("Seats Available", "0"))
            except:
                seats_avail = 0
            seats_avail += y
            movie["Seats Available"] = str(max(0, seats_avail))
            new_line = "{" + ", ".join([f"'{k}': '{movie[k]}'" for k in movie]) + "}\n"
            ul.append(new_line)
        else:
            ul.append(line.strip() + "\n")
    STF.seek(0)
    STF.truncate()
    STF.writelines(ul)
    STF.flush()

def ticket_numbers():                                                                  #Booking Tickets
    print()
    global nop
    global mid
    mid=input("Enter 'Show ID' : ")
    count=0
    while count < 3:
        try:
            Adult = int(input("Number Of Adults (12years and Above) : "))
            Child = int(input("Number Of Children (12years and Below) : "))
            SaO = int(input("Number Of Senior Citizens/OKU Members : "))
        except ValueError:
            print("Please enter valid numbers.")
            count += 1
            continue
        if Adult <= 0:
            print("There has to be at least 1 adult.")
            count += 1
        else:
            break
    else:
        print("Too many failed attempts. Please try again later.")
        return
    nop=Adult+Child+SaO
    OR_Bookings(nop)
    seats_available(mid)
    Price(Adult, Child, SaO)

def save_bookings():                                                                    #Saving Booking Data into Text File
    STF.seek(0)
    lines = STF.readlines()
    global timestamp
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    global bookid
    bookid = BookingID()
    for line in lines:
        if f"'Show ID': {mid}" in line or f"'Show ID': '{mid}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            cn = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    cn[key] = value
            entry = {"Booked By": email, "Movie Name": cn.get("Cinema Name"), "Hall No.": cn.get("Hall Number"), 
                     "Cinema Date": cn.get("Show Date"), "Location": cn.get("Cinema Location"), "No. of Tickets": nop, 
                     "Seats": seats, "Date & Time of Booking": timestamp,"Show ID": mid, "Payment ID": Payid, "Booking ID": bookid}
            if fo.lower() == "y":
                entry["Food"] = foodid
            booking_line = "{" + ", ".join([f"'{k}': '{entry[k]}'" if not isinstance(entry[k], list) else f"'{k}': {entry[k]}" for k in entry]) + "}\n"
            BF.write(booking_line)
            BF.flush()
            break

def booking_hist():                                                                     #For User's Booking History
    print("Booking History")
    BF.seek(0)
    lines = BF.readlines()
    records = 0                                                                         #Counter For Matching Records
    for line in lines:
        if f"'Booked By': '{email}'" in line or f"'Booked By': {email}" in line or f"'Email': '{email}'" in line:
            print(line.strip())
            records += 1
    if records == 0:
        print("No Booking History Found.")
    else:
        print("Records Found =", records)

def book_tickets():                                                                     #Booking Cinema Tickets
    display_movies()
    ticket_numbers()
    dis=input("Do You Have Discount Codes? ").strip().upper()
    if dis=="Y":
        Discounts()
    global fo                                                                           #For Reciept
    fo=input("Do You Want to Order Food? (Y/N) ").strip().lower()
    if fo=="y":
        mode="Online"
        Food(mode)
    Pay(TotalP)
    if PM=="Cash":
        return
    else:
        OR_Revenue(TotalP)
        save_bookings()
        receipt()

def cancel_booking():                                                                   #Cancellation of a Booking
    BF.seek(0)
    lines = BF.readlines()
    ul = []
    for line in lines:
        if f"'Booked By': '{email}'" in line or f"'Email': '{email}'" in line:
            print(line.strip())
            bid = input("Enter Booking ID : ").strip()
            if f"'Booking ID': '{bid}'" in line or f"'Booking ID': {bid}" in line:
                if "'Status': 'Cancelled'" in line:
                    print("This booking has already been cancelled.")
                    return
                print("Cancelling Booking....")
                parts = line.replace("{", "").replace("}", "").split(",")
                entry = {}
                for part in parts:
                    if ":" in part:
                        key, value = part.split(":", 1)
                        key = key.strip().strip("'")
                        value = value.strip().strip("'")
                        entry[key] = value
                shid = entry.get("Show ID")
                try:
                    nt = int(entry.get("No. of Tickets", "0"))
                except:
                    nt = 0
                cancel_seats_available(shid, nt)
                pm = entry.get("Payment ID")
                cancel_OR_Payment(pm)
                cancel_OR_Revenue(pm)
                entry["Status"] = "Cancelled"
                new_line = "{" + ", ".join([f"'{k}': '{entry[k]}'" if not isinstance(entry[k], list) else f"'{k}': {entry[k]}" for k in entry]) + "}\n"
                ul.append(new_line)
                print("Booking Has Been Cancelled.")
                continue
        else:
            ul.append(line.strip() + "\n")
    BF.seek(0)
    BF.truncate()
    BF.writelines(ul)
    BF.flush()

#Ticketing Clerk
def receipt():                                                                          #Receipt
    print()
    STF.seek(0)
    lines = STF.readlines()
    global cn
    for line in lines:
        if f"'Show ID': {mid}" in line or f"'Show ID': '{mid}'" in line:
            parts = line.replace("{", "").replace("}", "").split(",")
            cn = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    cn[key] = value
            #Creating receipt text
            receipt_text = (
                " ------------------------------------------------------- \n"
                "|                         RECEIPT                       |\n"
                "|-------------------------------------------------------|\n"
                f"{'| Date & Time of Booking :'.ljust(25)}{timestamp.rjust(29)} |\n"
                "|-------------------------------------------------------|\n"
                f"{'| Customer :'.ljust(25)}{email.rjust(30)} |\n"
                f"{'| Movie :'.ljust(25)}{cn.get('Cinema Name', '').rjust(30)} |\n"
                f"{'| Movie Date :'.ljust(25)}{date.rjust(30)} |\n"
                f"{'| Hall Number :'.ljust(25)}{cn.get('Hall Number', '').rjust(30)} |\n"
                f"{'| Location :'.ljust(25)}{cn.get('Cinema Location', '').rjust(30)} |\n"
                f"{'| Number of Tickets :'.ljust(25)}{str(nop).rjust(30)} |\n"
                f"{'| Seats :'.ljust(25)}{str(seats).rjust(30)} |\n"
                "|-------------------------------------------------------|\n"
                f"{'| Total Amount :'.ljust(25)}{str(TotalP).rjust(27)} RM |\n"
                f"{'| Booking ID :'.ljust(25)}{str(bookid).rjust(30)} |\n"
                f"{'| Payment Method :'.ljust(25)}{PM.rjust(30)} |\n"
            )
            if fo == "y":
                receipt_text += f"{'| Food ID :'.ljust(25)}{str(foodid).rjust(30)} |\n"
            receipt_text += (
                "|            Thank you for booking with us!             |\n"
                " ======================================================= \n"
            )
            print(receipt_text)
            #Save to file
            filename = f"receipt_{email}_{date}.txt"
            with open(filename, "w") as f:
                f.write(receipt_text + "\n")
            print(f"Your receipt has been saved as '{filename}'.\n")
            break

def CashP():                                                                            #Cash Payment (In Store)
    CPF.seek(0)
    lines = CPF.readlines()
    updated_lines = []
    global Payid
    Payid = input("Enter Payment ID : ").strip()
    for line in lines:
        if f"'Payment ID': '{Payid}'" in line or f"'Payment ID': {Payid}" in line:
            print(line.strip())
            raw = line.strip()[1:-1]
            buffer = ""
            depth = 0
            parts = []
            for char in raw:
                if char == "," and depth == 0:
                    parts.append(buffer)
                    buffer = ""
                else:
                    buffer += char
                    if char == "[":
                        depth += 1
                    elif char == "]":
                        depth -= 1
            if buffer:
                parts.append(buffer)
            entry = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip().strip("'")
                    value = value.strip().strip("'")
                    if key == "Seats":
                        if value.startswith("[") and value.endswith("]") and "," in value:
                            value = value[1:-1].split(",")
                            value = [v.strip().strip("'").strip('"') for v in value]
                        elif value.startswith("[") and value.endswith("]"):
                            value = [value[1:-1].strip().strip("'").strip('"')]
                    entry[key] = value
            pay = input("Paid (Y/N) : ").strip().lower()
            if pay == "y":
                entry["Status"] = "Paid"
                global mid
                mid = entry.get("Show ID")
                global nop
                nop = entry.get("Number of Seats")
                global seats
                seats = entry.get("Seats")
                global fo
                fo = "y" if "Food ID" in entry else "n"
                global foodid
                foodid = entry.get("Food ID") if fo == "y" else None
                global TotalP
                TotalP = entry.get("Amount To Be Paid")
                global PM
                PM = "Cash"
                global email
                email=entry.get("Booked By")
                STF.seek(0)
                stf_lines = STF.readlines()
                for stf_line in stf_lines:
                    if f"'Show ID': {mid}" in stf_line or f"'Show ID': '{mid}'" in stf_line:
                        parts = stf_line.replace("{", "").replace("}", "").split(",")
                        show_entry = {}
                        for part in parts:
                            if ":" in part:
                                key, value = part.split(":", 1)
                                key = key.strip().strip("'")
                                value = value.strip().strip("'")
                                show_entry[key] = value
                        global date
                        date = show_entry.get("Show Date")
                        break
                OR_Revenue(float(TotalP))
                OR_Bookings(int(nop))
                save_bookings()
                receipt()
                updated_line = line.replace("'Status': 'Not Paid'", "'Status': 'Paid'")
                updated_lines.append(updated_line.strip() + "\n")
            elif pay == "n":
                print("Booking Cancelled")
                entry["Status"] = "Cancelled"
                updated_line = line.replace("'Status': 'Not Paid'", "'Status': 'Cancelled'")
                updated_lines.append(updated_line.strip() + "\n")
            else:
                updated_lines.append(line.strip() + "\n")
        else:
            updated_lines.append(line.strip() + "\n")
    CPF.seek(0)
    CPF.truncate()
    CPF.writelines(updated_lines)
    CPF.flush()

#ID Numbers (For Unique ID Numbers)
ciid=set()
def Cinemaid():                                                                         #For Cinema ID, For it not to get repeated
    while True:
        num=random.randint(00000, 99999)
        if num not in ciid:
            ciid.add(num)
            return num

pid=set()
def PayID():                                                                            #For Payment ID (Cash Payment also)
    while True:
        payid=random.randint(00000, 99999)
        if payid not in pid:
            pid.add(payid)
            return payid

iid=set()
def IssueID():                                                                          #For Issue ID (Technical Issues)
    while True:
        issueid=random.randint(00000, 99999)
        if issueid not in iid:
            iid.add(issueid)
            return issueid

bid=set()
def BookingID():                                                                        #For Booking ID (Cinema Tickets)
    while True:
        bookingid=random.randint(00000, 99999)
        if bookingid not in bid:
            bid.add(bookingid)
            return bookingid

fid=set()
def FoodID():                                                                           #For Food (Online Food Orders)
    while True:
        foodid=random.randint(00000, 99999)
        if foodid not in fid:
            fid.add(foodid)
            return foodid

#Main Program
print("Hello, Welcome to our Cinema Ticket Booking Services!")
print()
print("1. Login \n"
    "2. Register \n"
    "3. View Pricing. \n"
    "4. Report Technical Issue. \n" 
    "5. FeedBack")
choice=input("Please Enter the Number of The Operation : ")                             #Asking The Customer For Process Number
if choice=="1":
    if login():
        rewards_read(email)
        print("\n1. Book Tickets \n" \
            "2. View Booking History \n" \
            "3. Cancel Booking \n" \
            "4. Logout")
        c= input("Please select an option: ")
        if c=="1":
            book_tickets()
        elif c== "2":
            booking_hist()
        elif c== "3":
            cancel_booking()
        elif c== "4":
            print("Logging out…")
            
        else:
            print("Invalid choice. Please select a valid option.")

elif choice == "2":                                                                     #Creating New User Login
        new_user()

elif choice == "3":                                                                     #Displaying Pricing Sheet To Customer
        print("Thank you for using the movie ticket booking system!")
        Pricing()

elif choice=="4":                                                                       #To Report Technical Issues
    print("To Report Technical Issues, Please Login into your account.")
    if login():
        Technical_Issue()

elif choice=="5":                                                                       #Feedback
    print("To Give a Feedback, Please Login into your account.")
    if login():
        Feedback()

elif choice.upper()=="ID":                                                              #Hidden Path that a customer isnt aware of which leads to backend worker's portal
    ID=input("Enter Your ID : ")
    if ID=="Tech":                                                                      #Technician
        print("Hello Technician!")
        print("1. Check Current Technical Issues. \n2. Edit/Update Technical Issues.")
        op=input("Enter the Number Of the Operation : ")
        if op=="1":
            Technir()
        elif op=="2":
            Techniw()
    
    elif ID=="TicketCl":                                                                #Ticketing Clerk
        print("Hello Ticketing Clerk!")
        print("1. Customer Cash Payment. \n" 
        "2. Booking Ticket For Customer. \n" 
        "3. Food Order. \n"
        "4. Food Collection.")
        proc=input("Enter the Number Of the Operation : ")

        email="In Store Booking"
        if proc=="1":
            CashP()
        elif proc=="2":
            book_tickets()
            if PM=="Cash":
                CashP()
        elif proc=="3":
            mode="In Store"
            Food(mode)
            penal="No"
            fo="y"
            Pay(FoodP)
        elif proc=="4":
            Food_Collection()

    elif ID=="CinemaMang":                                                              #Cinema Manager
        print("Hello Cinema Manager!")
        print("1. Add Movie Listings. \n" 
        "2. Update Movie Listings. \n"
        "3. Remove Movie Listing. \n" 
        "4. Overall Report \n" 
        "5. View Feedbacks")
        proc=input("Enter the Number Of the Operation : ")
        if proc=="1":
            AddC()
        elif proc=="2":
            UpdateC()
        elif proc=="3":
            RemoveC()
        elif proc=="4":
            Overall_Report()
        elif proc=="5":
            Feedback_read()
