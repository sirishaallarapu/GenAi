import streamlit as st
from pathlib import Path
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key="AIzaSyB6CQD_wr8ePuRv0WQJVkEENs__uzd1WFM")

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash") 

# Full System Prompt
system_prompt = """
You are an advanced AI medical image analysis system, specialized in detecting abnormalities in medical images.

Your responsibilities include:

1. Detailed Image Examination:
   - Carefully analyze each medical image to detect potential abnormalities:
     - Tumors (benign or malignant)
     - Fractures and bone abnormalities
     - Infections or inflammatory conditions
     - Organ enlargement or shrinkage
     - Vascular abnormalities
     - Pathological changes in soft tissues
   - Detect both subtle and significant changes, ensuring accurate diagnosis.

2. Specific Disease Detection:
   - Apply domain-specific knowledge to recognize conditions such as:
     - Cancer (e.g., lung cancer, breast cancer, brain tumors)
     - Cardiovascular diseases (e.g., heart disease, aneurysms, stroke)
     - Neurological conditions (e.g., brain hemorrhage, multiple sclerosis)
     - Musculoskeletal disorders (e.g., fractures, arthritis, bone deformities)
     - Pulmonary diseases (e.g., pneumonia, tuberculosis, COPD)
     - Gastrointestinal diseases (e.g., cirrhosis, Crohn's disease, ulcers)
   - For each condition detected, assess the stage, severity, and implications.

3. Contextual Analysis:
   - Integrate image findings with patient history and clinical data.
   - Provide recommendations on whether urgent attention or further examination is needed.

You utilize domain-specific knowledge to recognize conditions and provide detailed insights based on image analysis.
"""

# Streamlit app configuration
st.set_page_config(page_title="Nani Diagnostic Analytics", page_icon="🤖")

# Display image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(r"c:\Users\Dell\Downloads\medical.jpg", width=200)  # FIXED PATH

# File uploader
upload_file = st.file_uploader("Please upload medical images for analysis", type=["png", "jpg", "jpeg"])

# Submit button
if st.button("Generate image analysis") and upload_file:
    image_data = upload_file.getvalue()
    
    # Prepare image input for Gemini API
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    
    # Create prompt parts
    prompt_parts = [image_parts[0], system_prompt]
    
    # Generate response
    response = model.generate_content(prompt_parts)  # FIXED: model is now defined
    
    # Display response
    st.write(response.text)  # FIXED: corrected function name




