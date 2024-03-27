# ImpactModelHW
Team Members:
Maoqi Zhang, Jiaying Chen, Yunei Lu  

## Project Structure
The project is organized as follows to ensure easy navigation and understanding:
```bash
ImpactModelHW/  
│  
├── data/ # Data files and directories (Note that will also introduce how the data is downloaded in section 1.2)  
│ ├── quotes/ # quotes data
│   ├── 20070620
│   └── ...
│ └── trades/ # trades data
│   ├── 20070620
│   └── ...
│ └── SP500.txt # files for stocks tickers of interest  
│  
├── impactUtils/ # Main source code for the project  
│ ├── FirstPriceBuckets.py  # function for calculating arrival price
│ └── ImbalanceValue.py  # function for calculating imbalance
│ └── LastPriceBuckets.py  # function for calculating last price
│ └── MidQuoteReturnBuckets.py  
│ └── ReturnBuckets.py  
│ └── TickTest.py  
│ └── VWAP.py  
│
├── taq/ # taq read functions  
│ ├── ... 
│  
├── tests/ # Test suite for the project's code  
│ ├── ...  
│  
├── README.md # Overview and setup instructions (this file)  
│  
└── requirements.txt # Project dependencies  
```

## Environment Setup

To get started with the Impact Model Project, follow these steps to set up your environment:

```bash
# Clone the project repository
git clone https://github.com/MAOQIZHANG/ImpactModelHW.git

# Navigate to the project directory
cd ImpactModelHW

# Optional: Set up a virtual environment
python -m venv env
source env/bin/activate  # Use `env\Scripts\activate` on Windows

# Install the required dependencies
pip install -r requirements.txt
```
## Obtaining Data
download data from the following google drive and extract them to a single folders XXX.  
https://drive.google.com/drive/folders/1-miz6sr56bghLPonGFWkKBMh57axuoa9  
https://drive.google.com/drive/folders/1-kOZsUVQZwr-Lo-ybU-7ChRqFnrxLWGj  

```python
parent_directory = "XXX"  #replace this with ur folder after extraction
```
then run `extract_data.py`
It should print 
```bash
...
finish extracting data
finish removing data
Trades directories in correct format: 65
Quotes directories in correct format: 65
```
## Data processing
Calculation function are located in ImpactUtils and the final matrices are in 
https://drive.google.com/drive/folders/1mdwMFWPuGOWm_-DKcsIFt-A7e79w7gdp?usp=sharing  

## Filtering high volatility days
Volatility is a standard deviation of a 2 minutemid-quote returns computed using last 10 days of data and scaled to a daily value. 
We filter the volatility by the 95% percent cap.
After the filtering, the matrices for volatility and high vol days are in  
https://drive.google.com/drive/folders/1mdwMFWPuGOWm_-DKcsIFt-A7e79w7gdp?usp=sharing  

## Testing code 
To run unittests for every functions, open a terminal or command prompt, navigate to the project folder and run below:
```bash
python -m unittest discover -s tests
```
## Regression
<img width="845" alt="image" src="https://github.com/MAOQIZHANG/ImpactModelHW/assets/67251502/b0b0e6bb-92f6-4ff3-ada0-3c4f11c6582f">  

Transform it to linear regression as follows:   

<img width="594" alt="image" src="https://github.com/MAOQIZHANG/ImpactModelHW/assets/67251502/f817e84b-676d-4400-9812-d6692fe1f9a4">


## Summary statistics
See the notebook included in the dir



