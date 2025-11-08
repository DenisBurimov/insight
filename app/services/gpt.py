import openai
from config import config
from app.logger import log


CFG = config()

openai.api_key = CFG.OPENAI_API_KEY
client = openai.OpenAI()


class ChatGPT:

    def ask(self, prompt, file_path=None):
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
            # Combine the prompt with the file content
            full_prompt = f"{prompt}\n\nFile content:\n{file_content}"
        else:
            full_prompt = prompt

        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": full_prompt}],
        )

        message = response.choices[0].message.content
        return message

    def answer_question(self, question: str):
        resp = client.responses.create(
            model="gpt-5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Ви юридичний помічник. Відповідайте ЛИШЕ за результатами file_search і ЛИШЕ українською.\n"
                                "Обовʼязково наводьте цитати з файлів з vectore stores\n"
                                "Обовʼязково вказуйте з якої статті якого саме документу.\n\n"
                                f"Питання: {question}"
                            ),
                        }
                    ],
                }
            ],
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [CFG.VECTOR_STORE_ID],
                    "max_num_results": 12,
                    # optional metadata filters:
                    # "filters": {
                    #   "type": "and",
                    #   "filters": [
                    #     {"type": "eq",  "key": "jurisdiction", "value": "HU"},
                    #     {"type": "in",  "key": "tags", "value": ["employment"]}
                    #   ]
                    # }
                }
            ],
        )
        # simplest way to get the model’s text:
        return resp.output_text
