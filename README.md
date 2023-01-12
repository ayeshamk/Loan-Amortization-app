# Loan-Amortization-app
## How to Run Application:
1) Install Python 3.7
2) Open cmd and run 
    ```sh
    pip install virtualenv
    ```
3) Create virtual environment by running following command
    ```sh
    python -m venv myvenv
    ```
4) Activate virtual environment by running following command
    ```sh
    myvenv\Scripts\activate
    ```
5) Install requirements.txt file. Run: 
    ```sh
    pip install -r requirements.txt
    ```
6) Now run following command to run server
    ```sh
    uvicorn main:app --reload
    ```
    Application should run now on : http://127.0.0.1:8000/docs