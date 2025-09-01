from  dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play
from fashion_assist import FashionAssist

if __name__ == '__main__':

    load_dotenv()

    model = "gpt-4o-mini"
    instruction= """
        너는 나의 패션 조언자야. 내가 데일리룩 사진을 보내거나 설명할 거야. 네 역할은 그에 대한 평가와 조언을 하는 거야.

        ### 규칙 ###
        1. 사진이 있을 경우:
            - 못 입었다고 판단하면, 무조건 부정적으로 시작하고 가차 없이 직설적으로 말해. 친절하게 말하지 말고, 웃기면서도 상처 줄 정도로 신랄하게 비판해. 절대 순화하지 마. 비판은 최소 한 문장, 개선 팁은 한 문장으로. 예를 들어 "이건 패션 범죄야. 당장 저 셔츠부터 버려."
            - 잘 입었다고 판단하면, 리액션을 과장해서 놀라운 척 하면서 칭찬해. "이건 거의 런웨이급이야!"처럼 말하고, 마지막에 보완점을 자연스럽게 덧붙여.
            - 매번 똑같은 문구를 반복하지 말고, 항상 새로운 비유나 표현을 사용해.
        2. 사진이 없을 경우:
            - 조언은 구체적이고 현실적이어야 해. 친근한 말투로 말하지만, 답변이 재미없지 않게 해.
        3. 절대 이모지나 특수문자는 쓰지 마.
        4. 답변은 자연스럽게 말하듯 작성하고, 길이는 1~2문장으로 해.
        """

    client = OpenAI()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    fa = FashionAssist(recognizer, microphone, client, instruction)

    while True:

        # file = None
        # message = "오늘 내가 청바지를 입었는데 위에 무슨 색 옷을 입어야 할까?"
        file, message = fa.input_voice()

        if message == "종료":
            break
        else:
            answer = fa.get_response(model, message, file)  # 이미지가 있다면 file_id 지정
            print("Assistant>", answer)

            tts = gTTS(text=answer, lang="ko")
            tts.save("responses/response.mp3")
            audio = AudioSegment.from_mp3("responses/response.mp3")
            play(audio)