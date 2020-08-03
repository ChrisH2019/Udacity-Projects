# Data Engineering Capsone Project: I94 Immigration Data Warehouse
 
## Intruduction

This project is aim to create a data warehouse with ETL pipeline. The analytical data warehouse will enable U.S. officials to find untrivial insights of travellers/immigrants' patterns to the U.S. For example, is there any collrelation between temperature and the number of travellers? If so, is the correlation postisive or negative? And how strong is the correlation?

## Project Datasets

The main dataset will include data on immigration to the United States, and supplementary datasets will include data on airport codes, U.S. city demographics, temperature data and immigration label description dataset.

## Data Warehousing Schema

### Fact Table: immigrations

| Column Name | Data Type |
| :--- | :--- |
| cicid | VARCHAR PRIMARY KEY |
| cit | VARCHAR |
| res | VARCHAR |
| biryear | SMALLINT |
| gender | VARCHAR |
| iata | VARCHAR |
| arrdate | BIGINT|
| mode | VARCHAR |
| city | VARCHAR |
| state | VARCHAR |
| depdate | BIGINT |
| visa | VARCHAR |
| visatype | VARCHAR |
| admnum | DOUBLE PRECISION |
| airline | VARCHAR |
| fltno | VARCHAR|
| count | SMALLINT |

The immigrations table will serve as a fact table and will store the I94 immigration data as events. The `iata` column will be used to join the `iata` column of the airports table. Value of the `city` column is derived from the immigration label description file and is used to join the `city` column of temperature and demographics, repsectively.


### Dim Table: temperature

| Column Name | Data Type |
| :--- | :--- |
| city | VARCHAR  PRIMARY KEY |
| average_temperature | REAL |
| latitude | VARCHAR |
| longitude | VARCHAR |

The temperature table will serve as a dimension table and will the average historical temperauture of each U.S. city along with its latitude and longitude.

### Dim Table: demographics

| Column Name | Data Type |
| :--- | :--- |
| city | VARCHAR PRIMARY KEY |
| state | VARCHAR PRIMARY KEY |
| median_age | REAL |
| male_population | INTEGER |
| female_population | INTEGER |
| number_of_veterans | INTEGER|
| number_of_foreign_born | INTEGER |
| average_household_size | REAL |
| race | VARCHAR |
| count | INTEGER|

The demographics table will serve as a dimension table and will store demographic information of U.S. cities.

### Dim Table: airports

| Column Name | Data Type |
| :--- | :--- |
| ident | VARCHAR PRIMARY KEY |
| type | VARCHAR |
| name | VARCHAR |
| elevation_ft | REAL |
| iso_country | VARCHAR |
| iso_region | VARCHAR |
| municipality | VARCHAR |
| gps_code | VARCHAR |
| iata | VARCHAR |

The airports table will serve as a dimentsion table and will store information of U.S. airports.

## ETL Pipeline

1. Create fact and dim tables
2. Extract i94 immigration, i94 immigration data dictionary, temperature, demogratphic and airport data
3. Transform the above extracted data
4. Load the transoformed data into fact and dim tables
5. Data quality check
    - Check unique key
    - Check table join
    - Check source/count completeness
    - Check table contents