
**Interactive Video Script Generation with OpenAI**

This project provides a streamlined workflow for generating interactive video scripts using OpenAI's GPT-3.5-turbo language model. It leverages a guided approach, breaking down script creation into distinct phases (Main Structure, Section Descriptions, Draft, Outline, Scenes) to create detailed and engaging scripts.

**Features**

* **Guided Script Creation:** The system guides you through the script creation process step-by-step.
* **OpenAI Integration:**  Leverages OpenAI's GPT-3.5-turbo to generate high-quality script content based on your input.
* **Example Generation:** Creates multiple examples for each stage (Draft, Outline, Scenes) to offer creative options.
* **Customization:** Allows you to provide a guide (topic/theme) to tailor the script to your specific needs.
* **Iterative Refinement:** You can update and refine the script at each stage.
* **JSON Output:**  The generated scripts are formatted as JSON for easy integration with other tools or systems.

**Usage**

1. **Create Main Structure:**
   ```bash
   curl -X POST http://localhost:8080/create_main -H "Content-Type: application/json" -d '{"GuideFor": "Your video topic"}'
   ```
   This will generate and save the main structure of your script in the "Guides/On Process" directory.

2. **Add Section Descriptions/Delete Examples:**
   ```bash
   curl -X POST http://localhost:8080/Create_Description -H "Content-Type: application/json" -d '{"GuideFor": "Your video topic", "Status": "main_created"}'  # To add descriptions
   curl -X POST http://localhost:8080/Create_Description -H "Content-Type: application/json" -d '{"GuideFor": "Your video topic", "Status": "Delete"}'   # To delete examples
   ```

3. **Generate Examples (Draft, Outline, Scenes):**
   ```bash
   curl -X POST http://localhost:8080/create_draft -H "Content-Type: application/json" -d '{"GuideFor": "Your video topic", "Status": "description_created"}'
   # Repeat for outline and scenes with appropriate endpoints and statuses.
   ```

4. **Finalize Script:**
   ```bash
   curl -X POST http://localhost:8080/create_scenes -H "Content-Type: application/json" -d '{"GuideFor": "Your video topic", "Status": "Finish"}'
   ```

**File Structure**

* `Guides/`: Stores the generated and template JSON files.
* `guide_functions.py`: Contains functions to create and manage the script's structure.
* `prompt_ai.py`: Contains classes and functions for generating script content using OpenAI.
* `true_example.py`, `false_example.py`: Sample JSON structures for reference.
* `main_json.py`: Initializes a basic JSON structure.

**Key Points**

* You need to replace placeholders (`your-repository-url`, `your_openai_api_key`, etc.) with your actual values.
* Customize the prompts in `guide_functions.py` and `prompt_ai.py` to better suit your specific script generation needs. 

Let me know if you'd like any adjustments to this README file!
