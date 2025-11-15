import openai
import json
import base64
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

    def recognize(self, file_path: str):
        with open(file_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        response_text = None
        payment_data = None
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # or gpt-4o or "gpt-4-vision-preview"
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Could you please recognize all data from this document\n"
                                    "This is a ukrainian bank payment instruction\n"
                                    "Please, return a json with these fields: ['number', 'payment_date', 'receiving_date', 'summ', 'summ_words', 'payment_purpose', 'payer_name', 'payer_code', 'payer_bank_name', 'payer_bank_code', 'payer_iban', 'recipient_name', 'recipient_code', 'recipient_bank_name', 'recipient_bank_code', 'recipient_iban']\n"
                                    "Do not make up anything. If it's a problem to recognize some value, please, set null for it.\n"
                                    "Extract the information and return ONLY valid JSON without any markdown formatting or additional text. Do not wrap the response in code blocks.\n"
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                },
                            },
                        ],
                    }
                ],
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            log(log.ERROR, "Failed to get a LLM response. %", e)
            return None, None

        try:
            payment_data = json.loads(response_text)
            log(log.INFO, "Payment data has been successfully recognized")
            return payment_data, None
        except Exception as e:
            log(log.ERROR, "Failed to recognize data. %", e)
            return None, response_text


gpt_service = ChatGPT()
