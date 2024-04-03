import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic AbZr2__i9EuqqR55lJlvSEuwBj-2Hhp-IFZg8MjZ_QeBIrHOZbIlUBy7Lf5YPB6_0IFznLH4Yv7ZJbe9:EBnOxb78Wnru21O1qJB_ZTz0o1WJrODesTXXIEjL-l1XR0v9rguJMSb1EWV7WO0JdKosHCPe11fo2_ku',
}

response = requests.get('https://api-m.sandbox.paypal.com/v2/payments/authorizations/0VF52814937998046', headers=headers)
print(response)