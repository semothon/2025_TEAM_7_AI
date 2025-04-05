import os
import tiktoken
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from dotenv import load_dotenv
import json
import openai

DAYS = {"MON": "월요일", "TUE": "화요일", "WED": "수요일", "THU": "목요일", "FRI": "금요일", "SAT": "토요일", "SUN": "일요일"}

load_dotenv()
print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}\n")

# 테스트용 json 파일 로드. 배포용 코드에서는 사용 X
with open("loopin_ai/example.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

llm = ChatOpenAI(model="gpt-4o-mini")

def create_template_message(json):
    msg_list = []
    msg_list.append(SystemMessage("당신은 모임 애플리케이션에서 사용자에게 모임을 추천하는 AI입니다."))
    msg_list.append(HumanMessage(f"""모임 {len(json)}개의 정보를 보여드리겠습니다.
각 모임 정보는 아래와 같은 항목들로 구성되어 있습니다.

1. ID: 모임 ID                    
2. Name: 모임 이름
3. Category: 모임 카테고리
4. Subcategory: 모임 서브 카테고리
5. Description: 모임 설명
6. Date/Time: 모임 요일 및 시간
7. Location: 모임 장소
8. Maxmember: 최대 인원 수 """))
    
    for club in json:
        day_and_time = club['whenMeet'] # 비어있으면 None
        # date_and_time 문자열에서 요일과 시간 정보 추출
        day_time_string = ""
        if day_and_time is not None:
            day_and_time = day_and_time.split(",")
            for elem in day_and_time:
                elem.strip()
            day_list = day_and_time[0:len(day_and_time) - 1]
            time = day_and_time[len(day_and_time) - 1].split(" ")
            for elem in day_list:
                day_time_string += DAYS[elem] + ", "
            day_time_string += time[0][:2] + ":" + time[0][2:] + " - " + time[1][:2] + ":" + time[1][2:]
        else:
            day_time_string = "미정"
            

        input_msg = f"""1. ID = {club['id']}
2. Name: {club['name']}
3. Category: {club['category']}
4. Subcategory: {club['subCategory']}
5. Description: {club['description']}
6. Date/Time: {day_time_string}
7. Location: {club['whereMeet']}
8. Maxmember: {club['maximumMember']}
"""
        msg_list.append(HumanMessage(content = input_msg))
        
    msg_list.append(HumanMessage("""이상으로 모든 모임에 대한 정보를 설명했습니다.
이제 제가 원하는 모임에 대해 설명하겠습니다."""))
    msg_list.append(MessagesPlaceholder("UserInput"))
    msg_list.append(HumanMessage("""이상으로 제가 원하는 모임에 대해 설명했습니다.
이제 다음 절차에 따라 모임을 추천해주세요.
                                 
1. 위에서 설명한 모임들 중 제가 원하는 모임에 해당할 것 같은 모임을 최대 5개 선택하세요.
2. 선택된 모임의 ID 값들을 콤마(,)로 구분해 출력해주세요.
3. 모임 ID 값 외에 다른 정보는 출력하지 마세요.
4. 만약 제가 원하는 모임이 없다면 '없음'이라고 출력해주세요.
출력 예시 1) 1, 3, 4, 7, 9
출력 예시 2) 3, 8
출력 예시 3) 없음"""))
    return msg_list

prompt = ChatPromptTemplate.from_messages(create_template_message(json_data))

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"UserInput": [HumanMessage(content="활동적인 사람에게 맞는 모임을 5개 추천해줘.")]})
print(result)

"""
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 모임 애플리케이션에서 사용자에게 추천을 제공하는 AI입니다."),
    ("user", "{input}"),
])
"""




"""
client = openai.OpenAI()
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
print(response.choices[0].message.content)
"""