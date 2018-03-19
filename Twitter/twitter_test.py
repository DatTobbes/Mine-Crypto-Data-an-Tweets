from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('mysql+mysqldb://root:@localhost:3306/coindata')
d=pd.read_sql("SELECT * FROM actual_coindata limit 10;", engine)
print(d)