import anthropic
from aryn_sdk.partition import partition_file
import json
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

def format_content(structured_content):
        formatted_text = ""
        for item in structured_content:
            if item.get("type") in ["Section-header", "Text", "List-item"]:
                formatted_text += f"{item['text_representation']}\n\n"
            elif item.get("type") == "table":
                formatted_text += "Table:\n"
                for cell in item['table']['cells']:
                    formatted_text += f"{cell['content']} | "
                formatted_text += "\n\n"
        return formatted_text

def printout(jsonin):
        json_data = json.loads(jsonin)

        for dic in json_data:
            print(f"{dic['image_title']}: \n{dic['image_description']}\n")

def summarize(file_name, aryn_api_key, anthropic_api_key):
    file = open(file_name, 'rb')

    partitioned_file = partition_file(file, aryn_api_key, extract_images=True, extract_table_structure=True, use_ocr=True)

    data = partitioned_file['elements']

    class description(BaseModel):
        image_title: str
        image_description: str

    class diagram_response(BaseModel):
        steps: list[description]

    diagram_response_schema = diagram_response.model_json_schema()

    tools = [
        {
            "name": "build_description_result",
            "description": "build the description object",
            "input_schema": diagram_response_schema
        }
    ]

    formatted_content = format_content(data)

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    # {
                    #     "type": "text",
                    #     "source": {
                    #         "type": "text",
                    #         "media_type": "text",
                    #         "data": f"{formatted_content}",
                    #     },
                    # },
                    {
                        "type": "text",
                        "text": f"The following is a json conversion using aryn docparser to read a pdf syllabus upload, please get key dates and times of relevant events like midterms. As well, give me some prerequisites and information about them to make sure the student is prepared; related links are helpful. {formatted_content}"
                    }
                ],
            }
        ],
            tools=tools,
            tool_choice={"type": "tool", "name": "build_description_result"}

    )
    out = json.dumps(message.content[0].input['steps'], indent=4)

    
    printout(out)