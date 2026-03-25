from dotenv import load_dotenv

# 保证有一个.env的文件，作为敏感信息的环境变量文件
load_dotenv('project.env')

import os

# 保证变量名一一对应
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
openai_api_key = os.getenv('OPENAI_API_KEY')

print(f'{db_user =}')
print(f'{db_password =}')
print(f'{openai_api_key =}')

