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
    message1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The following is a PDF syllabus document. Please extract specific key dates and times of relevant events like lectures, midterms, and project deadlines from the document. "
                                "Use the provided template to create a calendar event for each relevant date.\n\n"
                                "If an event does not have specific information for any field, set that field to `null`.\n\n"
                                "Template:\n"
                                "event = {\n"
                                "  'summary': 'Event summary (e.g., Midterm Exam)',\n"
                                "  'location': 'Event location (if provided)',\n"
                                "  'description': 'Brief description of the event',\n"
                                "  'start': {\n"
                                "    'dateTime': 'Start date and time in ISO 8601 format (e.g., 2025-05-28T09:00:00-07:00)',\n"
                                "    'timeZone': 'Time zone (if provided)',\n"
                                "  },\n"
                                "  'end': {\n"
                                "    'dateTime': 'End date and time in ISO 8601 format (if available)',\n"
                                "    'timeZone': 'Time zone (if provided)',\n"
                                "  },\n"
                                "  'recurrence': [\n"
                                "    'Recurrence rule in RRULE format (if applicable)',\n"
                                "  ],\n"
                                "  'attendees': [\n"
                                "    {'email': 'Attendee email (if available)'},\n"
                                "  ],\n"
                                "  'reminders': {\n"
                                "    'useDefault': False,\n"
                                "    'overrides': [\n"
                                "      {'method': 'email', 'minutes': 24 * 60},\n"
                                "      {'method': 'popup', 'minutes': 10},\n"
                                "    ],\n"
                                "  },\n"
                                "}\n\n"
                                "Document:\n"
                                f"{formatted_content}\n\n"
                                "Instructions:\n"
                                "1. Extract key events such as lectures, midterms, finals, and project deadlines.\n"
                                "2. Fill out the `summary`, `start`, `end`, `location`, and `description` fields based on the document content.\n"
                                "3. If the time zone is not mentioned, set it to `null`.\n"
                                "4. If recurrence information (like repeating lectures) is provided, use the `recurrence` field with an RRULE.\n"
                                "5. If no attendees are listed, set the `attendees` field to an empty list.\n"
                                "6. Set any missing fields to `null` if the information is unavailable.\n"
                                "7. Use ISO 8601 format for date and time fields."
                                "Give no further text only the filled out events."
                    }
                ],
            }
        ],
        tools=tools,
        tool_choice={"type": "tool", "name": "build_description_result"}

    )
    out1 = json.dumps(message1.content[0].input['steps'], indent=4)

    message2 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The following is a PDF syllabus document converted using aryn docparse. Please give a summary of all of the important information"
                                f"{formatted_content}\n\n"
                    }
                ],
            }
        ],
        tools=tools,
        tool_choice={"type": "tool", "name": "build_description_result"}

    )
    out2 = json.dumps(message2.content[0].input['steps'], indent=4)

    message3 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "The following is a PDF syllabus document converted using aryn docparse. Please ingest the information of the course, and only return likely or defined prerequisites to ensure the student is prepared for the content of the class with likely prerequisites returned in a list and having external linkes to resources if necessary."
                                f"{formatted_content}\n\n"
                    }
                ],
            }
        ],
        tools=tools,
        tool_choice={"type": "tool", "name": "build_description_result"}

    )
    out3 = json.dumps(message3.content[0].input['steps'], indent=4)

    return out1, out2, out3
