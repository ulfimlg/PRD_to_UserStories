import streamlit as st
import time
from prd_epic import start_prd_to_epic_conversion
from epic_feature import start_epic_to_feature_conversion
from feature_user import start_feature_to_userstory_conversion
import re
import os
import io
import fitz
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace
from PIL import Image
import tempfile
import requests
from requests.auth import HTTPBasicAuth
import json
import os

load_dotenv()
#Fill in your domain url before running
url = "https://<YOUR_DOMAIN>/rest/api/3/issue"

#Enter your personal email and your API key here
auth = HTTPBasicAuth("<YOUR_EMAIL>", os.getenv("JIRA_API_KEY"))
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

#Function extracts Pictures, Tables and Texts
def extract_media_from_document(file_path: str):
    ''' Extracts texts, tables and images from a pdf document'''
    save_path = os.path.join(os.getcwd(), "media")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    data = {'images': [], 'tables': [], 'texts': []}
    
    print(file_path)
    pdf_file = fitz.open(file_path)
    file_id = 0
    
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        
        # FIND IMAGES
        if 'imgs' not in os.listdir(save_path):
            os.mkdir(os.path.join(save_path, 'imgs'))
        
        for image_index, img in enumerate(page.get_images(full=True), start=1):
            try:
                pix1 = fitz.Pixmap(pdf_file.extract_image(img[0])["image"])
                mask = fitz.Pixmap(pdf_file.extract_image(img[1])["image"])
                pix = fitz.Pixmap(pix1, mask)
                im = Image.open(io.BytesIO(pix.tobytes()))
            except:
                pix = pdf_file.extract_image(img[0])["image"]
                im = Image.open(io.BytesIO(pix))
            
            # Save Images
            img_path = os.path.join(save_path, f"imgs/{page_index}_{file_id}.png")
            im.save(img_path)
            
            data['images'].append(img_path)
            file_id += 1
        
        # FIND TABLES
        tabs = page.find_tables()
        if tabs.tables:
            table = tabs[0].extract()
            data['tables'].append({'table': table, 'page_no': page_index})
        
        # FIND TEXTS
        data['texts'].append({'text': page.get_text(), 'page_no': page_index})
    
    print(f"Found {len(data['texts'])} page(s), {len(data['images'])} image(s) and {len(data['tables'])} table(s).")
    return data

#Function to parse output from Markdown format to a normal text format
def parse_user_stories(text):
    features = {}
    current_feature = None
    additional_stories = []

    lines = text.split('\n')
    for line in lines:
        line = line.strip()

        # Check for feature
        feature_match = re.match(r'^### Feature: "(.*?)"$', line)
        if feature_match:
            current_feature = feature_match.group(1)
            features[current_feature] = []
            continue

        # Check for user story
        user_story_match = re.match(r'^- \*\*User Story \d+:\*\* (.+)$', line)
        if user_story_match and current_feature:
            user_story = user_story_match.group(1)
            features[current_feature].append(user_story)
            continue

        # Check for acceptance criteria
        acceptance_criteria_match = re.match(r'^  - \*Acceptance Criteria:\*$', line)
        if acceptance_criteria_match and current_feature and features[current_feature]:
            features[current_feature][-1] += " (Acceptance Criteria follow)"
            continue

        # Check for additional user stories
        if current_feature == "Additional User Stories":
            additional_story_match = re.match(r'^- \*\*User Story \d+:\*\* (.+)$', line)
            if additional_story_match:
                additional_stories.append(additional_story_match.group(1))

    # Add additional user stories to the features dictionary
    if additional_stories:
        features["Additional User Stories"] = additional_stories

    return features

#Function which sends each User story to Jira (Before running update "key":AA,AT or whatever the key exists for your project)(Also update "issuetype": 10002 or the number shown on Jira issue filter)
def post_jira(story,user_no):
    payload = json.dumps( {
  "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": story,
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "issuetype": { #update here
      "id": "10012"
    },
    "project": { #update here
      "key": "AT"
    },
    "summary": "User story - "+str(user_no),
  },
  "update": {}
} )
    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

st.title("Autogen PRD to User")
#Form for upload
with st.form("prd_upload_form"):
    read_pdf = st.file_uploader("Upload Product Requirement Document here", type="pdf")
    prd=""
    submit_button = st.form_submit_button("Convert2UserStory")
#On submission of the form
if submit_button:
    if read_pdf is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(read_pdf.getvalue())
            tmp_file_path = tmp_file.name

        #Reading the PDF
        all_data = extract_media_from_document(tmp_file_path)
        for text_entry in all_data["texts"]:
            prd+=text_entry["text"]

        #Starting prd to user conversion agents
        epics = start_prd_to_epic_conversion(prd)
        time.sleep(4)
        st.write(epics.chat_history[-2]["content"])
        features = start_epic_to_feature_conversion(epics.chat_history[-2]["content"])
        time.sleep(4)
        st.write(features.chat_history[-1]["content"])
        user_stories=start_feature_to_userstory_conversion(features.chat_history[-1]["content"])
        time.sleep(4)
        
        #User story list 
        st.write(user_stories.chat_history[-1]["content"])
        #parsing user stories
        st.write("The Parsed Contents are Uploaded to Jira: ")
        parsed_features = parse_user_stories(user_stories.chat_history[-1]["content"])
        #Uploading to Jira
        if isinstance(parsed_features, dict) and parsed_features:
            user=0
            for feature, user_stories in parsed_features.items():
                st.write(f"Feature: {feature}")
                for story in user_stories:
                    st.write(f"  - {story}")
                    user+=1
                    post_jira(story,user)
                st.write()
        else:
            print("No valid features found in the input text.")
            print("Parsed content:", parsed_features)
        st.write("The stories have been uploaded to Jira successfully")
    else:
        st.error("Please upload a PDF file before converting.")

