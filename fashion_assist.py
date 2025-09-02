import os
import base64
from openai import OpenAI
import speech_recognition as sr

class FashionAssist():
    def __init__(self, recognizer, microphone, client, instruction):
        self.recognizer = recognizer
        self.microphone = microphone
        self.client = client
        self.chat_history = [{"role": "system", "content": instruction}]

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def input_voice(self):

        image = input("사진을 첨부하시겠습니까? (파일명 입력, 없으면 엔터) : ")
        if image.strip() == "":
            file = None
        else:
            file = f"images/{image}"
            if not os.path.isfile(file):
                print(f"경고: '{file}' 파일이 존재하지 않습니다.")
                file = None
            else:
                file = self.encode_image(file)

        self.recognizer.energy_threshold = 400
        self.recognizer.pause_threshold = 1

        with self.microphone as source:
            print('말씀하세요.')
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=50)
            txt = self.recognizer.recognize_google(audio, language='ko-KR')
            print(txt)
        return file, txt


    def get_response(self, model, message, image):

        if image is not None:
            content = [
                {"type": "text", "text": message},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
            ]
        else:
            content = [
                {"type": "text", "text": message}
            ]

        self.chat_history.append({"role": "user", "content": content})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    *self.chat_history,
                ],
                response_format={
                    "type": "text"
                },
                temperature=1.0,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": answer})

            return answer

        except Exception as e:
            return f"Error during API request: {e}"
        
    def speak(self, text: str, file_path: str = "responses/response.mp3", voice: str = "echo"):
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text
        ) as response:
            response.stream_to_file(file_path)


