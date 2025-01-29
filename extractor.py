import json
import re
from typing_extensions import List
from groq import Groq
from tqdm import tqdm

extractor_system_prompt = (
    "you are a data extractor.\n"
    "you'll ge given a contents of a pitch deck, typically a text for you."
    " you have to extract key information from it.\n"

    "here are the fields you have to look for:\n"
    "- startupName:str name of the startup\n"
    "- url:str url of the startup\n"
    "- industry:str enum[fintech, edtech, healthtech, others] industry of the startup\n"
    "- industry.other:str mention the industry of the startup, if only industry is 'others' else null\n"
    "- problemStatement:str problem statement of the startup\n"
    "- problemStatement2:str problem statement of the startup\n"
    "- problemStatement3:str problem statement of the startup\n"
    "- solution:str solution of the startup\n"
    "- UVP:str UVP of the startup\n"
    "- solutionDifferent:str solution of the startup\n"
    "- features:str features of the startup\n"

    "- tam:str TAM of the startup\n"
    "- sam:str SAM of the startup\n"
    "- marketTrends: str market trends of the startup\n"
    "- competitorAnalysis: str competitor analysis of the startup\n"
    "- revenueModel:str enum[subscription, freemium, Ads, others] revenue model of the startup\n"
    "- revenueModel.other:str mention the revenue model of the startup, if only revenue model is 'others' else null\n"
    "- expectedPricing:str expected pricing of the startup\n"
    "- primaryCustomers:str primary customers of the startup\n"
    "- customerAcquisition:str customer acquisition of the startup\n"

    "- currentRevenue:str current revenue of the startup\n",
    "- revenueProjections:str revenue projections of the startup\n",
    "- fundRaised:str enum[yes, no] fund raised of the startup\n",
    "- funds.*.fundRaisedAmount:str fund raised amount of the startup, if yes\n",
    "- funds.*.fundRaisedSource:str fund raised source of the startup, if yes\n",
    "- customerCount:str customer count of the startup\n",
    "- growthMetrics:str growth metrics of the startup\n",
    "- notableAchievements:str notable achievements of the startup\n",
    "- teamMembers.*.name:str name of the team member\n",
    "- teamMembers.*.email:str email of the team member\n",
    "- teamMembers.*.phone:str phone of the team member\n",
    "- teamMembers.*.role:str enum[CEO, CTO] role of the team member\n",
    "- teamMembers.*.background:str background of the team member\n",
    "- teamMembers.*.linkedin:str linkedin url of the team member\n",
    "- advisors:str advisors of the startup\n",
    "- employeeCount:str employee count of the startup\n",
    "- files.pitchDeck.*.fundRaisedAmount:str fund raised amount of the startup, if yes\n",
    "- files.pitchDeck.*.fundRaisedSource:str enum[angel investors, VCs, grants] fund raised source of the startup, if yes\n",
    "- fundsNeeded:str funds needed of the startup\n",
    "- fundsUsedFor:str funds used for of the startup\n",
    "- expectedRunway:str expected runway of the startup\n",
    "- equityOffered:str equity offered of the startup\n",

    "NOTE:\n",
    "- the fields with * are list of values, you can add as many as you want\n",
    "- make sure to extract the key-value pairs in JSON format.\n",
    "- if you can't find any keys or you not sure about it, then leave as null"
)

print(''.join(extractor_system_prompt))


insighter_system_prompt = (
    "you are a data insight extractor.\n",
    "given the image of silde or a page of a pitch deck, you have to extract key information from it.\n",

    "extract text and understand images i.e., graphs, images, tables etc.\n"
    "describe the image or graph in every aspect possible, that should be understandable without seeing the image.\n"
    
    "respond with neatly formatted markdown format with all necassary insights in it.\n"
    "make sure you have collected all the information and put it in the response."
)


class Insighter:
    def __init__(self):
        self.client = Groq()

    def extract(self, pages: List[str]):
        total_response = ''

        for i, page in tqdm(enumerate(pages)):
            print(f"{i}/{len(pages)}")
            response = self.client.chat.completions.create(
                messages=[
                    {
                        'role': 'user',
                        "content": [
                            {
                                "type": "text",
                                "text": ''.join(insighter_system_prompt)
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{page}"},
                            },
                        ],
                    }
                ],
                model='llama-3.2-11b-vision-preview',
                temperature=1.0,
            )

            total_response += f"Page {i+1}:\n" + response.choices[0].message.content + "\n\n"
        return total_response

class Extractor:
    def __init__(self):
        self.client = Groq()

    def get_answer_response(self, content):
        final_answer = content.split("</think>")[-1].strip()
        print(final_answer)
        return final_answer
    
    def extract(self, page_info: str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': ''.join(extractor_system_prompt)
                },
                {
                    "role": "user",
                    "content": "Extract key-value pairs from the following text in json format:\n\n" + page_info,
                }
            ],
            model="deepseek-r1-distill-llama-70b",
            stream=False,
        )
        raw_res = chat_completion.choices[0].message.content
        main_content = self.get_answer_response(raw_res)
        pattern = r'\```json([\s\S]*?)\```'
        match = re.search(pattern, main_content)
        if match:
            return json.loads(match.group(1))
        else:
            return None
