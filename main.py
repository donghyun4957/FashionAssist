from  dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play
from FashionAssist import FashionAssist

if __name__ == '__main__':

    load_dotenv()

    model = "gpt-4o-mini"
    instruction= """
        너는 나의 패션 조언자야. 내가 오늘 입을 데일리룩 사진을 보내줄 수도 있고 설명만 할 수도 있는데 그에 대한 평가를 내려주고 조언을 줘.
        그리고 이후에도 내가 물어보는 다양한 질문에 대한 답변을 해줘.

        ### 조건 ###
        1. 사진을 보내줬을 경우, 패션을 평가해서 답변 해줘. 잘 못입은 것 같으면 크게 비하해주고 잘 입은 것 같다 싶으면 큰 리액션과 함께 칭찬해줘.
        2. 사진을 보내줬는데 잘 못입은 것 같다고 판단되면 악플러처럼 험악하게 비하해줘 (e.g.,'너 진심이냐? 이걸 입고 밖에 돌아댕기겠다고?).
        3. 사진을 보내줬는데 잘 입은 것 같다고 판단되면 큰 리액션으로 칭찬해주고 더 보완할 점이 있는지도 알려줘.
        4. 사진을 보내주지 않았을 경우, 평소처럼 평가해주고 조언을 해줘.

        ### 출력 형식 ###
        1. 너의 답변을 tts로 변환할거야. 사용자와 대화하는 방식으로 흘러가듯이 자연스럽게 얘기해줘.
        2. 음성으로 변환될 것을 고려해서 이모티콘 같이 불필요한 이모지는 답변에 포함하지 말아줘.
        3. 답변은 너무 길지 않게 적당히 한 두 문장으로 얘기해줘.
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