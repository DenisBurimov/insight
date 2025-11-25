import os
import openai
from datetime import datetime
from app.logger import log
from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


class FilterDate(BaseModel):
    gte: Optional[str] = None
    lte: Optional[str] = None


class QueryFilters(BaseModel):
    action: Literal["count", "list", "sum"] | None
    filters: Dict[str, Any] = {}


class ChatGPT:
    def get_filters(self, question: str):
        try:
            log(log.INFO, "Asking GPT: %s", question)
            start_time = datetime.now()
            QUERY_SYSTEM_PROMPT = """
            You are a financial query planner. You MUST output ONLY valid JSON. 
            Do NOT include explanations or natural language. 
            Your job is to convert user questions into a JSON query plan with the following structure:

            {
            "action": "sum" | "list" | "count" | null,
            "filters": {
                "date": {
                "gte": "YYYY-MM-DD" | null,
                "lte": "YYYY-MM-DD" | null
                },
                "number": "number" | null,
                "payment_date": "string" | null,
                "receiving_date": "string" | null,
                "summ": "number" | null,
                "summ_words": "string" | null,
                "payment_purpose": "string" | null,
                "payer_name": "string" | null,
                "payer_code": "string" | null,
                "payer_bank_name": "string" | null,
                "payer_bank_code": "string" | null,
                "payer_iban": "string" | null,
                "recipient_name": "string" | null,
                "recipient_code": "string" | null,
                "recipient_bank_name": "string" | null,
                "recipient_bank_code": "string" | null,
                "recipient_iban": "string" | null
            }
            }

            All filter fields MUST exist in the output and MUST be explicit null if not used.

            ---

            ### ACTION RULES

            1. If the question asks:
            - “скільки транзакцій”, “скільки є”, “кількість” 
                → action = "count"
            - “яка сума”, “яка загальна сума”, “сума транзакцій” 
                → action = "sum"
            - “список транзакцій”, “покажи транзакції”, “виведи транзакції”
                → action = "list"
            - If no clear action is present or question is irrelevant → action = null

            2. You must never invent actions not listed above.

            ---

            ### FILTER RULES

            You must extract ANY combination of filters referenced in the user question:

            - Name of the payer or recipient  
            (“платник <name>”, “отримувач <name>”,  
            “платник чи отримувач <name>”)  
            → set `payer_name` = <name> OR `recipient_name` = <name>  
            If text says “платник чи отримувач <name>” → set BOTH fields.

            - IBAN  
            (“платник має <IBAN>”, “рахунок платника чи отримувача <IBAN>”)
            → set payer_iban / recipient_iban as appropriate  
            If question says “чи отримувача”, fill both fields.

            - Date ranges  
            Example: “з 2024-01-10 по 2024-02-01”  
            → date.gte = “2024-01-10”  
            → date.lte = “2024-02-01”

            - Payment purpose  
            (“призначенням платежу <text>”)  
            → payment_purpose = <text>

            - If a filter is NOT mentioned → MUST set it to null.

            ---

            ### IRRELEVANT QUESTION RULE

            If the question is NOT about transactions, sums, counts, lists, 
            payers, recipients, IBANs, payment purpose, dates, or amounts,
            return:

            {
            "action": null,
            "filters": {}
            }

            ---

            ### EXAMPLES (CRITICAL)

            1) “Скільки зберігається в базі транзакцій де платник чи отримувач ТОВ Сонях?”
            → action = "count"
            → payer_name = "ТОВ Сонях", recipient_name = "ТОВ Сонях"

            2) “Яка сума транзакцій де платник чи отримувач має IBAN UA123456789?”
            → action = "sum"
            → payer_iban = "UA123456789", recipient_iban = "UA123456789"

            3) “Скільки транзакцій з призначенням платежу Оренда?”
            → action = "count"
            → payment_purpose = "Оренда"

            4) “Список транзакцій з 2024-01-01 по 2024-02-01”
            → action = "list"
            → date.gte = "2024-01-01", date.lte = "2024-02-01"

            5) “Яка сума транзакцій по рахунку UA7777777?”
            → action = "sum"
            → set payer_iban = "UA7777777" AND recipient_iban = "UA7777777"

            6) “Сума транзакцій з 2024-01-10 по 2024-02-01 де платник ТОВ Агросвіт”
            → action = "sum"
            → date.gte/date.lte set
            → payer_name = "ТОВ Агросвіт"

            7) Time expressions in any language ("last month", "перший квартал минулого року", "минулого тижня", etc.) 
            MUST be converted into ISO dates in the filters.date object.
            
            8). Quarter mapping:
            Q1 = Jan 1 – Mar 31
            Q2 = Apr 1 – Jun 30
            Q3 = Jul 1 – Sep 30
            Q4 = Oct 1 – Dec 31

            Example:
            “перший квартал минулого року” → last year Q1.

            ---

            ### ABSOLUTE REQUIREMENTS

            - ALWAYS output ALL filter fields, even if null.
            - NEVER output extra fields.
            - NEVER output natural language.
            - ONLY output the JSON object.
            - Do not invent missing information.

            """

            response = client.responses.create(
                model="gpt-5.1",
                input=[
                    {"role": "system", "content": QUERY_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": question}],
                    },
                ],
                reasoning={"effort": "low"},
                text={"verbosity": "low"},
            )
            answer_time = datetime.now() - start_time
            log(log.INFO, "Got GPT answer in %s", answer_time)
            return QueryFilters.model_validate_json(response.output_text)
        except Exception as e:
            log(log.ERROR, f"Error while asking GPT: {e}")
            return f"Трясця! Сталася помилка: {e}"
        
    
    def get_answer(self, question: str):
        try:
            log(log.INFO, "Asking GPT for answer: %s", question)
            start_time = datetime.now()

            RESPONSE_SYSTEM_PROMPT = """
            You are a financial assistant. Provide clear and concise answers.
            """

            response = client.responses.create(
                model="gpt-5.1",
                input=[
                    {"role": "system", "content": RESPONSE_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [{"type": "input_text", "text": question}],
                    },
                ],
                reasoning={"effort": "low"},
                text={"verbosity": "low"},
            )
            answer_time = datetime.now() - start_time
            log(log.INFO, "Got GPT answer in %s", answer_time)
            return response.output_text
        except Exception as e:
            log(log.ERROR, f"Error while asking GPT for answer: {e}")
            return f"Трясця! Сталася помилка: {e}"


gpt_service = ChatGPT()
