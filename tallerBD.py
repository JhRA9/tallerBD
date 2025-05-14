import comtradeapicall

subscription_key = 'comtrade-v1.json'

mydf = comtradeapicall.previewFinalData( partnerCode='842',
    typeCode='C', freqCode='A', clCode='HS', period='2021,2022',
    reporterCode='170',  cmdCode='0901', flowCode='X',
    includeDesc=True, partner2Code='0', customsCode='C00', motCode='0', 
)

mydf.head()

print(mydf.columns)
print(mydf.describe())
mydf.to_excel('exportaciones_cafe_col_usa.xlsx', index=False)