#### Assignment: Bank System

Design a system for a bank to lend money to borrowers and receive payment for the loans.

The system should have the following functions:

LEND: The bank can give loans to customers. There is no restriction on the loan amount and number of loans given to a customer. The function should take customer_id, loan_amount(P), loan_period(N) and rate of interest(I) as input. It should return the Total amount(A) to be paid and the monthly EMI to be paid.

PAYMENT: Customers can pay back loans either in the form of EMI or through LUMP SUM amounts. In the case of Lump sum payment, the lump sum amount will get deducted from the total amount. This can reduce the number of EMIs.

LEDGER: Customers can check all the transactions for a loan id. Along with all the transactions, It should also return the balance amount, monthly EMI and number of EMI left.

ACCOUNT OVERVIEW: This should list all the loans customers have taken. For each loan, it should tell the loan amount(P), Total amount(A), EMI amount, Total Interest(I), the amount paid till date, number of EMI left.

Calculations:

I(Interest) = P (Principal) _ N (No of Years) _ R (Rate of interest)

A(Total Amount) = P + I

Assumption:

Feel free to take any assumption

Note:

- Use restful APIs to expose the functions.
- You can use any programming language and framework of your choice.
- To persist data use any database / file based system.
- Keep things simple. The system should not be at the production level. But you should be able to explain your design decision.

---

## How to Use This Project

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/bank_system.git
cd bank_system
```

### 2. Install Dependencies

Install the required dependencies using your preferred package manager.  
For example, if using Python and `requirements.txt`:

```sh
pip install -r requirements.txt
```

### 3. Run the Application

Start the server (update the command as per your framework, e.g., Flask, FastAPI, Node.js):

```sh
python app.py
```
or  
```sh
uvicorn main:app --reload
```

### 4. API Endpoints

- **LEND**: Create a new loan for a customer.
- **PAYMENT**: Make EMI or lump sum payments for a loan.
- **LEDGER**: View all transactions and loan details for a loan.
- **ACCOUNT OVERVIEW**: List all loans and their status for a customer.

Use tools like [Postman](https://www.postman.com/) or `curl` to interact with the RESTful APIs.

### 5. Data Persistence

The system uses a simple database or file-based storage (see project files for details).  
No setup required for basic usage.

