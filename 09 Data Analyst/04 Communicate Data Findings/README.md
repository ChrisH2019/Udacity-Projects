# Insights for Loan Data from Prosper

## Dataset Overview

The dataset is provided by Udacity.com. There are 113,937 loans with 81 variables on each loan, including loan amount, borrower rate (or interest rate), current loan status, borrower income, and many others.

Ater data wrangling, a subset of 84,853 loans with the following variables is used to do univariate exploration:
- Term
- LoanStatus
- BorrowerAPR
- ProsperRating
- ListingCategory
- EmploymentStatus
- DelinquenciesLast7Years
- TotalProsperLoans
- LoanOriginalAmount
- LoanOriginationDate
- Recommendations

Since the primary interest is to analyze the loans whose status are either completed or defaulted, data wrangling is performed on the subset of the dataset and the new dataset contains 26,005 loans with the same variables. 
- The LoanStatus variable contains categories of Complted or Defaulted (Chargedoff is re-encoded as Defaulted).
- For the ListingCategory variable, categories that do not belong to Debt Consolidation, Home Improvement, Business and Auto are re-encoded as Other.

## Findings in the Exploratory Data Analysis

- The most common terms are 36 months.
- The majority of loan status are Current, Completed, Chargedoff and Defaulted.
- Prosper ratings are almost normally distributed.
- Debt consolidation, Other, Home Improvement and Business are the most common listings among borrowers.
- The bulk of borrowers are Employed.
- The majority are first time borrowers, while the minority have existing loans of 1 to 2. The maximum number of loans is 8.
- The majority of borrowers rarely have any recommendation while applying for loans.
- The majority of BorrowerAPR are in the range between about 0.15 and 0.25. Overall, a generally bimodal distribution is obseraved.
- The majority of borrowers have 0 deliquencies in the last 7 years. the minority have deliquencies between about 1 to 30. The maximum number of deliquencies is 99.
- The majority of original loan amount are about 4,000, 1000 or 15000
- In general, the number of loans grows over time. Starting from around 2013, there is a substancial growth in terms of the number of loans.
- BorrowerAPR and LoanOriginalAmount, LoanOriginalAmount and Term are modetely correlated. TotalProsperLoans and Recommedations, DelinquenciesLast7Years and BorrowerAPR, DelinquenciesLast7Years and LoanOriginalAmount are weakly correlated.
- Defaulted loans tend to have higher BorrowerAPR.
- Defaulted loans have wider IQR in terms of number of deliquencies in the last 7 years than complted ones.
- Defaulted loans tend to have lower original loan amount.
- The better the ratings, the lower the APR.
- Listing categories Debt Consolidation and Home Improvement tend to have lower APR.
- Lower ratings tend to have higher number of deliquencies in last 7 years.
- For a given loan amount, borrower APR tends to be lower in completed loans than that in defaulted ones.
- Defaulted loans in Auto or Business categories tend to have have larger original loan amount.

## Insights for Presentation

- Factors affect a loan’s outcome status
	- Defaulted loans, in general, have higher borrower APR than completed ones.
	- Generally, the lower the Prosper rating, the higher number of defaulted loans is.
	- Borrowers in defaulted loans tend to have higher number of deliquencies in the last 7 years.
	- Borrowers in defaulted loans tend to borrow less in terms of loan original amount.

- Factors affect the borrower’s APR
	- The higher the rating, the lower the APR is and vice versa.
	- Debt Consolidation and Home Improvement categories tend to have lower APR.
	- Full-time, Part-time, Retired and Employed categories tend to have lower APR.
	- The larger the original loan amount, the lower APR is and vice versa.

- Differences between loans depending on how large the original loan amount was
	- For a given original loan amount, borrower APR tends to be lower in completed loans than that in defaulted ones.
	- Auto or Business categories tend to have higher risks in terms of original loan amount.