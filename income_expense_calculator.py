# Income/Expense Calculator
"""
This program is designed to help users analyze their monthly spending habits by processing a list of financial transactions stored in a text file.
When the program runs, you input your categories such as Food, Rent, Entertainment, etc, a small description of each category and the price.
It calculates the total income, total expenses, and net balance for the month.
Using conditional statements, the program determines whether the user is under or over budget based on a predefined spending limit.
The program outputs a detailed financial summary to both the terminal and an output file named 'budget_report.txt'.
This output file report includes total income, total expenses, net balance, and a breakdown of expenses by category, plus whether or not you’re within your budget limit.
The program uses loops for data aggregation, a user-defined function for calculating category totals, and a while loop to allow the user to re-analyze the budget multiple times or exit the program.
"""
#Goes through all transactions and adds up money spent/earned by category.
def calculate_category_totals(transactions):
    category_totals={}                            #dictionary to store totals per category
    for category, desc, amount in transactions:     #unpack each transaction tuple
        if category not in category_totals:         #create key if new category
            category_totals[category]=0
        category_totals[category]+=amount         #add income or expense to category total
    return category_totals

#Saves the report to a text file with all results.
def write_report(filename, income, expenses, balance, category_totals, over_budget):
    f = open(filename, "w")
    f.write("===== Monthly Budget Report =====")
    f.write("\n")       
    f.write("Total Income: $" + str(round(income, 2)))
    f.write("\n")
    f.write("Total Expenses: $" + str(abs(round(expenses, 2))))
    f.write("\n")
    f.write("Net Balance: $" + str(round(balance, 2)))
    f.write("\n")
    if balance < 0:                                         #check for negative balance
        f.write("WARNING: Your net balance is negative. You overspent this month.")  
        f.write("\n")
    if over_budget:
        f.write("You are over your budget limit!")           
    else:
        f.write("You are within your budget limit.")         
    f.write("\n")
    f.write("Expense Breakdown by Category:")
    f.write("\n")

    for category in category_totals:                        #list each category total
        total = category_totals[category]
        f.write("- " + category + ": $" + str(round(total, 2)))
        f.write("\n")
    f.write("Thank you for using Budget Analyzer!")
    f.close()

#Lets user type income/expense items until they type "done".
def get_user_transactions():
    transactions=[]                                       #list to store all entries
    print("Enter your transactions below.")                 
    print("Use positive values for income and negative values for expenses.")  
    print('Type "done" when finished.')                     
    while True:                                              #keeps asking until user stops
        category=input("Enter category or 'done': ").strip()   
        if category.lower()=="done":
            break
        description=input("Enter a short description: ").strip()
        amount_input=input("Enter amount: ")
        try:                                                #handles bad input
            amount=float(amount_input)
        except ValueError:
            print("Invalid amount. Try again.")                  
            continue
        transactions.append((category, description, amount))     #stores tuple
        print("Transaction added!") 
    return transactions

#Main function: runs entire program
def main():
    print("______ Welcome to the Interactive Budget Analyzer ______")
    budget_limit=2000.0
    while True:
        transactions=get_user_transactions()                 # collect user entries
        if len(transactions)==0:                             # check if list empty
            print("No transactions entered. Exiting program.") 
            break
        income=0                                             # start income counter
        for t in transactions:                                 # loop through each transaction
            amt=t[2]                                         # extract amount
            if amt>0:                                        # if income
                income=income+amt                          # add to income

        expenses=0                                           # start expense counter
        for t in transactions:
            amt=t[2]                                         # extract amount
            if amt < 0:                                     # if expense
                expenses=expenses+amt                       # add (negative value)

        balance=income+expenses

        category_totals=calculate_category_totals(transactions)  # totals by category

        over_budget=abs(expenses) > budget_limit             # check if expenses > limit

        expense_only={}
        for cat in category_totals:
            if category_totals[cat]<0:                       # check if category spent money
                expense_only[cat]=category_totals[cat] 

        if len(expense_only) > 0:
            max_expense_cat=min(expense_only, key=expense_only.get)
        else:
            max_expense_cat="None"

        print("_______ Budget Summary _______")                
        print("Total Income: $" + str(round(income, 2)))
        print("Total Expenses: $" + str(abs(round(expenses, 2))))
        print("Net Balance: $" + str(round(balance, 2)))
        print("Highest Expense Category: " + max_expense_cat)

        if balance<0:                                        
            print("Warning: Your net balance is negative. You overspent this month.")

        if over_budget:
            print("You are over your budget limit.")
        else:
            print("You are within your budget limit.")

        write_report("budget_report.txt", income, expenses, balance, category_totals, over_budget)
        print("A detailed report has been written to budget_report.txt") 
        again = input("Run another analysis? (y/n): ")       
        if again.lower()!="y":                              
            print("Thank you for using Budget Analyzer.")
            break

#Run program only if executed directly
if __name__ == "__main__":
    main()
