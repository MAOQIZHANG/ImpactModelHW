# ImpactModelHW
ImpactModel HW for Algo Trading

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
