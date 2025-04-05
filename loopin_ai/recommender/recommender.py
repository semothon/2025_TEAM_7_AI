import os
import json
import logging
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

DAYS = {"MON": "월요일", "TUE": "화요일", "WED": "수요일", "THU": "목요일", "FRI": "금요일", "SAT": "토요일", "SUN": "일요일"}

SYS_PROMPT_MSG = "당신은 모임 애플리케이션에서 사용자에게 모임을 추천하는 AI입니다."

DATA_KNOWLEDGE_DESCRIPTION = """모임 {n}개의 정보를 보여드리겠습니다.
각 모임 정보는 아래와 같은 항목들로 구성되어 있습니다.

1. ID: 모임 ID                    
2. Name: 모임 이름
3. Category: 모임 카테고리
4. Subcategory: 모임 서브 카테고리
5. Description: 모임 설명
6. Date/Time: 모임 요일 및 시간
7. Location: 모임 장소
8. Maxmember: 최대 인원 수"""

TASK_DESCRIPTION = """이상으로 제가 원하는 모임에 대해 설명했습니다.
이제 다음 절차에 따라 모임을 추천해주세요.

1. 위에서 설명한 모임들 중 제가 원하는 모임에 해당할 것 같은 모임을 최대 5개 선택하세요.
2. 선택된 모임의 ID 값들을 콤마(,)로 구분해 출력해주세요.
3. 모임 ID 값 외에 다른 정보는 출력하지 마세요.
4. 만약 제가 원하는 모임이 없다면 '없음'이라고 출력해주세요.
출력 예시 1) 1, 3, 4, 7, 9
출력 예시 2) 3, 8
출력 예시 3) 없음"""

load_dotenv(override=True)
logging.debug(f"API KEY: {os.environ.get('OPENAI_API_KEY')[:4]}****")

llm = ChatOpenAI(model="gpt-4o-mini")

def create_template_message(json):
    msg_list = []
    msg_list.append(SystemMessage(SYS_PROMPT_MSG))
    msg_list.append(HumanMessage(DATA_KNOWLEDGE_DESCRIPTION.format(n = len(json))))
    
    for club in json:
        day_and_time = club['whenMeet'] # 비어있으면 None
        print(day_and_time)
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
            if len(time) == 2:
                day_time_string += time[0][:2] + ":" + time[0][2:] + " - " + time[1][:2] + ":" + time[1][2:]
            else:
                day_time_string += "시간 정보 미정"
        else:
            day_time_string = "미정"
            
        input_msg = (f"1. ID = {club['id']}\n"
                     f"2. Name: {club['name']}\n"
                     f"3. Category: {club['category']}\n"
                     f"4. Subcategory: {club['subCategory']}\n"
                     f"5. Description: {club['description']}\n"
                     f"6. Date/Time: {day_time_string}\n"
                     f"7. Location: {club['whereMeet']}\n"
                     f"8. Maxmember: {club['maximumMember']}")
        msg_list.append(HumanMessage(content = input_msg))
        
    msg_list.append(HumanMessage("이상으로 모든 모임에 대한 정보를 설명했습니다. 이제 제가 원하는 모임에 대해 설명하겠습니다."))
    msg_list.append(MessagesPlaceholder("UserInput"))
    msg_list.append(HumanMessage(TASK_DESCRIPTION))
    return msg_list

def make_recommendation(json: list[dict], req_message: str) -> list:
    prompt = ChatPromptTemplate.from_messages(create_template_message(json))
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"UserInput": [HumanMessage(content=req_message)]})
    print(result)
    if result == "없음":
        return []
    else:
        try:
            result = result.split(",")
            for i, elem in enumerate(result):
                elem = elem.strip()
                if elem.isdigit():
                    result[i] = int(elem)
            return result
        except:
            return []

if __name__ == "__main__":
    # 테스트용 json 파일 로드
    with open(Path(__file__).parent / "example.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    result = make_recommendation(json_data, "활동적인 사람에게 적합한 모임을 골라줘.")