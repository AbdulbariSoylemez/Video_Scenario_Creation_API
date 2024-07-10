import json, openai
from pydantic import BaseModel
from true_example import example_true_json
from false_example import example_false_json
from main_json import json_file
from typing import Optional
from fastapi import HTTPException


# open ai key inputs 
class  CreateMain(BaseModel):
    GuideFor: str
    Status: Optional[str] = 'Create'
    
def create_main(item: CreateMain):
      
    json_format = json_file()
    json_format["GuideFor"] = item.GuideFor
    GuideForPrompt = json_format["GuideFor"]
    true_json = example_true_json()
    false_json = example_false_json()
    
    prompt = f"""
    You are a scriptwriter and you create many different types of video scripts.
    The guide for this scenario is '{GuideForPrompt}', you need to use these values to create scenario.
    And never change the 'GuideFor' key value. First you will write a Description for the 'GuideFor'. Then you will write the TargetAudienceCharacteristics, ContentObjectives, CalltoAction and SuccessMetrics.
    This guide should be used as the basis for the scenario creation. You will receive two json file structure that includes many keys for a scenario creation template. 
    Scenario will start to create from "GuideFor" Key, the first one on the json. Don't forget this is a guide for interactive video creation scenario.
    You will proceed sequentially, according to the 'guide for', you will write things related to each other in all values. TopicSelection key values will be same for all VideoDraft, VideoOutline and VideoScenes.
    Depending on the scenario you will write you should determine the 'IsAdditionalInformationNeeded' value.
    if it is true you need to fill the AdditionalInformation blocks. If it is false, you must delete AdditionalInformation blocks. 
	If not, there is no need for an AdditionalInformation block, delete it. And the AdditionalInformation blocks will be same on all Prerequisites keys.
    You can determine number of CallToAction values, number of which platforms.
    You can use {true_json} and {false_json} as an example but only the structural parts, the scenario you will create is will be different. 
    Video time is crucial it should be not so long or not so short. You can think 1 scene is approximately 1 minute for very brief videos. On the other hand in short videos 1 scene could be 15 seconds to 45 seconds.
    You need to fill json key's values.
    {{
        "Answer": "The text of what you Answer will come to this part "}}"""
        
    file_name = item.GuideFor.lower().replace(' ', '_') + '.json'
    on_process_file_path = 'Guides/On Process/' + file_name
    
    if item.GuideFor == "" or None:
        return {item.Status : "Couldn't initialized", "Error": "GuideFor Is Empty"}
    else:
        response = openai.chat.completions.create(
                messages=[ 
                    {'role': 'user', 'content': prompt},
                ],
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                temperature=0.3,
            )
        processing_answer = response.choices[0].message.content

    if processing_answer is None:
         return {"Main Creation": "Not Initiated", "Error": "Couldn't reach openai"}
    clean_content = json.loads(processing_answer.strip())

    with open('/Users/abdulbarisoylemez/Desktop/Cinema8ProjectFinis/Guides/guide_templates/main_template.json', 'r') as f:
        main_template = json.load(f)

    for key, value in clean_content.items():
        if key in main_template:
            main_template[key] = value

    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']

    additional_info = clean_content.get('Prerequisites', {}).get('AdditionalInformation', None)

    if not main_template.get('IsAdditionalInformationNeeded', False) and additional_info:
        main_template['Prerequisites']['AdditionalInformation'] = additional_info

    for key in keys:
        if not main_template[key]['Prerequisites'].get('AdditionalInformation', False) and additional_info:
            main_template['VideoDraft']['Prerequisites']['AdditionalInformation'] = additional_info
            main_template['VideoOutline']['Prerequisites']['AdditionalInformation'] = additional_info
            main_template['VideoScenes']['Prerequisites']['AdditionalInformation'] = additional_info
            
        main_template['VideoDraft']['Prerequisites']['TopicSelection'] = clean_content['Prerequisites']['TopicSelection']
        main_template['VideoOutline']['Prerequisites']['TopicSelection'] = clean_content['Prerequisites']['TopicSelection']
        main_template['VideoScenes']['Prerequisites']['TopicSelection'] = clean_content['Prerequisites']['TopicSelection']
             
        with open(on_process_file_path, 'w') as f:
            json.dump(main_template, f, indent=4)        
            result = {"status": "main_created", "data": clean_content}
            return result
    else:
        return ("Invalid status. Expected 'create'.")

class PromptSectionDescription(BaseModel):
    GuideFor: str
    Status: str
 
async def create_section_description(item: PromptSectionDescription):
        
        json_format= f"Guides/On Process/{item.GuideFor.lower().replace(' ', '_')}.json"
        with open('lip/sectionPromtExample.json', 'r') as f:
            SectionExample = json.load(f)       
                    
        prompt=f""" You need to write 'SectionDescription' for '{json_format}' guide. You need to write SectionDescription for  VideoDraft, VideoOutline and VideoScenes.
        You only need to change SectionDescriptions nothing more will change, on these 3 parts. Your output should be just sectiondescriptions and their parents.
        The key and value stuructuer must be same with the original file.
        Example: '{SectionExample}'
            {{"Answer": "The text of what you Answer will come to this part "}}"""
            
        if item.GuideFor == "" or None:
            return {"Error": "GuideFor Is Empty"}
        else:
            response = openai.chat.completions.create(
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            temperature=0.3,
            )
            processing_answer = response.choices[0].message.content
            
        if processing_answer is None:
            return {"Main Creation": "Not Initiated", "Error": "Couldn't reach openai"}
        clean_content = json.loads(processing_answer.strip())
    
        with open('Guides/On Process/' + item.GuideFor.lower().replace(' ', '_') + '.json', 'r') as f:
            main_data = json.load(f)
            main_data['VideoDraft']['SectionDescription'] = clean_content['VideoDraft']['SectionDescription']
            main_data['VideoOutline']['SectionDescription'] = clean_content['VideoOutline']['SectionDescription']
            main_data['VideoScenes']['SectionDescription'] = clean_content['VideoScenes']['SectionDescription']
            
        with open('Guides/On Process/' + item.GuideFor.lower().replace(' ', '_') + '.json', 'w') as f:
            json.dump(main_data, f, indent=4)
        return main_data


class VideoScriptGenerator:
    def __init__(self, guide_path, response_format_file):
        self.guide_path = guide_path
        self.response_format_file = response_format_file
        self.load_guide()
        self.load_draft()

    def load_guide(self):
        with open(self.guide_path, "r") as file:
            self.guide = json.load(file)

    def load_draft(self):
        with open(self.response_format_file, "r") as f:
            self.response_format = json.load(f)



    def create_video_draft_examples(self):
        self.response_format["Inputs"]["Prerequisites"] = self.guide["Prerequisites"]

        prompt=f"""
                You are a scriptwriter and you create many different types of video scripts.
                
                Now, you want to create a video classified as {self.guide["GuideFor"].__str__()},  which is made for the purpose of {self.guide["Description"].__str__()}, in line with the customer's request. 

                The scenarios of the intended purposes of the content of the video ContentObjectives:{self.guide["ContentObjectives"].__str__()}.

                Information scenarios about the profile of the target audience TargetAudienceProfile : {self.guide["VideoDraft"]["ExpectedOutcomes"]["TargetAudienceProfile"].__str__()}.

                Video goals and concept information scenarios VideoGoalsAndConcept :{self.guide["VideoDraft"]["ExpectedOutcomes"]["VideoGoalsAndConcept"].__str__()}.

                Narrator or character's scenarios :{self.guide["VideoDraft"]["ExpectedOutcomes"]["NarratororCharacter"].__str__()}.

                These types of videos are published on these {self.guide["Platforms"].__str__()} platforms and are expected to be approximately this length: {self.guide["EstimatedDuration"].__str__()}.
                
                But to do this, you must determine the Video Draft. This is what you are expected to do in this section: {self.guide["VideoDraft"]["SectionDescription"].__str__()}.

                Prepare the video using this guideline and the topic information and let it be more explanatory. Accordingly, prepare the video draft in JSON format.

                Response Format:{self.response_format}. You need to fill all the values.
            """


        # OpenAI API'sini kullanarak cevap üretme
        response = openai.chat.completions.create(
                messages=[
                    {'role': 'user', 'content': prompt},
                ],
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                temperature=0.3,
            )
        processing_answer=response.choices[0].message.content
        return processing_answer
    

    def create_video_outline_examples(self):
        # Biz bu yapı ile bizim Draft servisi ile oluşturduğumuz Dosyayı burda Outline template dosyamızın input kısmına atıyoruz ve prompt ile eksik kalan Output kısmını oluşturmasını istiyoruz 
        self.response_format["Inputs"]["Prerequisites"] = self.guide["VideoDraft"]["Examples"][0]["Inputs"]["Prerequisites"]
        self.response_format["Inputs"]["Platforms"] = self.guide["VideoDraft"]["Examples"][0]["Inputs"]["Platforms"]
        self.response_format["Inputs"]["EstimatedDuration"] = self.guide["VideoDraft"]["Examples"][0]["Inputs"]["EstimatedDuration"]
        self.response_format["Inputs"]["TargetAudienceProfile"] = self.guide["VideoDraft"]["Examples"][0]["Outputs"]["TargetAudienceProfile"]
        self.response_format["Inputs"]["VideoGoalsAndConcept"] = self.guide["VideoDraft"]["Examples"][0]["Outputs"]["VideoGoalsAndConcept"]
        self.response_format["Inputs"]["NarratororCharacter"] = self.guide["VideoDraft"]["Examples"][0]["Outputs"]["NarratororCharacter"]
 

        prompt=f"""
                You are a scriptwriter and you create many different types of video scripts.
                
                Now, you want to create a video classified as {self.guide["GuideFor"].__str__()},  which is made for the purpose of {self.guide["Description"].__str__()}, in line with the customer's request. 

                The scenarios of the intended purposes of the content of the video ContentObjectives:{self.guide["ContentObjectives"].__str__()}.

                Information scenarios about the profile of the target audience TargetAudienceProfile : {self.guide["VideoOutline"]["Prerequisites"]["TargetAudienceProfile"].__str__()}.

                Video goals and concept information scenarios VideoGoalsAndConcept :{self.guide["VideoOutline"]["Prerequisites"]["VideoGoalsAndConcept"].__str__()}.

                Narrator or character's scenarios :{self.guide["VideoOutline"]["Prerequisites"]["NarratororCharacter"].__str__()}.

                These types of videos are published on these {self.guide["Platforms"].__str__()} platforms and are expected to be approximately this length: {self.guide["EstimatedDuration"].__str__()}.
                
                But to do this, you must determine the Video Draft. This is what you are expected to do in this section: {self.guide["VideoOutline"]["SectionDescription"].__str__()}.

                Defines the starting scene or dialogue that will attract the audience's attention. It also summarizes the context that will allow you to understand the setting and importance of the video: {self.guide["VideoOutline"]["ExpectedOutcomes"]["Introduction"].__str__()}.

                Creates the main section and explains the basic message of each section. Along with the definition of important scenes and their importance in narrative, it strengthens the educational goals of the video:{self.guide["VideoOutline"]["ExpectedOutcomes"]["Development"].__str__()}.

                Summarizes how the video will end and highlights the viewer the main points or actions they should take:{self.guide["VideoOutline"]["ExpectedOutcomes"]["Conclusion"].__str__()}.

                Contains detailed descriptions of important scenes and explains how these scenes convey the main message:{self.guide["VideoOutline"]["ExpectedOutcomes"]["KeyScenesBreakdown"].__str__()}.

                Describes the visual elements and language of the video. This determines the character of the video and how it interacts with the audience:{self.guide["VideoOutline"]["ExpectedOutcomes"]["StyleAndTone"].__str__()}.

                Prepare the video using this guideline and the topic information and let it be more explanatory. Accordingly, prepare the video draft in JSON format.

                Such a structure will turn back {self.response_format} and {self.response_format["Outputs"]} in it: you need to fill in the missing places.

            """

        # OpenAI API'sini kullanarak cevap üretme
        response = openai.chat.completions.create(
                messages=[
                    {'role': 'user', 'content': prompt},
                ],
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                temperature=0.3,
            )
        processing_answer=response.choices[0].message.content
        
        return processing_answer

    def create_video_scenes_examples(self):
        # Biz bu yapı ile bizim Outline servisi ile oluşturduğumuz Dosyayı burda scenes template dosyamızın input kısmına atıyoruz ve prompt ile eksik kalan Output kısmını oluşturmasını istiyoruz 
        self.response_format["Inputs"]["Prerequisites"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["Prerequisites"]
        self.response_format["Inputs"]["Platforms"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["Platforms"]
        self.response_format["Inputs"]["EstimatedDuration"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["EstimatedDuration"]
        self.response_format["Inputs"]["TargetAudienceProfile"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["TargetAudienceProfile"]
        self.response_format["Inputs"]["VideoGoalsAndConcept"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["VideoGoalsAndConcept"]
        self.response_format["Inputs"]["NarratororCharacter"]=self.guide["VideoOutline"]["Examples"][0]["Inputs"]["NarratororCharacter"]    
        self.response_format["Inputs"]["Introduction"]=self.guide["VideoOutline"]["Examples"][0]["Outputs"]["Introduction"]
        self.response_format["Inputs"]["Development"]=self.guide["VideoOutline"]["Examples"][0]["Outputs"]["Development"]
        self.response_format["Inputs"]["Conclusion"]=self.guide["VideoOutline"]["Examples"][0]["Outputs"]["Conclusion"]
        self.response_format["Inputs"]["KeyScenesBreakdown"]=self.guide["VideoOutline"]["Examples"][0]["Outputs"]["KeyScenesBreakdown"]
        self.response_format["Inputs"]["StyleAndTone"]=self.guide["VideoOutline"]["Examples"][0]["Outputs"]["StyleAndTone"]

        prompt=f"""
                    You are a scriptwriter and you create many different types of video scripts.
                    
                    Now, you want to create a video classified as {self.guide["GuideFor"].__str__()},  which is made for the purpose of {self.guide["Description"].__str__()}, in line with the customer's request. 

                    The scenarios of the intended purposes of the content of the video ContentObjectives:{self.guide["ContentObjectives"].__str__()}.

                    Information scenarios about the profile of the target audience TargetAudienceProfile : {self.guide["VideoOutline"]["Prerequisites"]["TargetAudienceProfile"].__str__()}.

                    Video goals and concept information scenarios VideoGoalsAndConcept :{self.guide["VideoOutline"]["Prerequisites"]["VideoGoalsAndConcept"].__str__()}.

                    Narrator or character's scenarios :{self.guide["VideoOutline"]["Prerequisites"]["NarratororCharacter"].__str__()}.

                    These types of videos are published on these {self.guide["Platforms"].__str__()} platforms and are expected to be approximately this length: {self.guide["EstimatedDuration"].__str__()}.
                    
                    But to do this, you must determine the Video Draft. This is what you are expected to do in this section: {self.guide["VideoOutline"]["SectionDescription"].__str__()}.

                    Defines the starting scene or dialogue that will attract the audience's attention. It also summarizes the context that will allow you to understand the setting and importance of the video: {self.guide["VideoOutline"]["ExpectedOutcomes"]["Introduction"].__str__()}.

                    Creates the main section and explains the basic message of each section. Along with the definition of important scenes and their importance in narrative, it strengthens the educational goals of the video:{self.guide["VideoOutline"]["ExpectedOutcomes"]["Development"].__str__()}.

                    Summarizes how the video will end and highlights the viewer the main points or actions they should take:{self.guide["VideoOutline"]["ExpectedOutcomes"]["Conclusion"].__str__()}.

                    Contains detailed descriptions of important scenes and explains how these scenes convey the main message:{self.guide["VideoOutline"]["ExpectedOutcomes"]["KeyScenesBreakdown"].__str__()}.

                    Describes the visual elements and language of the video. This determines the character of the video and how it interacts with the audience:{self.guide["VideoOutline"]["ExpectedOutcomes"]["StyleAndTone"].__str__()}.

                    Indicates the number of the scene, showing its sequence within a section, Provides a detailed description of the scene, including locations, characters, and important objects, Describes the dialogues in the scene, advancing the story or providing important information to the audience,Determines the tone, speed, and emotion of the voice, engaging the audience and assisting in conveying the video's message, Specifies the camera movements, enhancing the visual storytelling and providing dynamism, Defines the lighting and shadow, setting the scene's atmosphere and highlighting important details,Determines scene transitions, supporting fluidity and narrative progression,Defines the style and tone of the scene, aligning with the brand identity and engaging the audience::{self.guide["VideoScenes"]["ExpectedOutcomes"]["Scenes"].__str__()}.

                    Prepare the video using this guideline and the topic information and let it be more explanatory. Accordingly, prepare the video draft in JSON format.

                    Such a structure will turn back {self.response_format} and {self.response_format["Outputs"]} in it: you need to fill in the missing places.

                """
         # OpenAI API'sini kullanarak cevap üretme
        response = openai.chat.completions.create(
                messages=[
                    {'role': 'user', 'content': prompt},
                ],
                model="gpt-3.5-turbo-0125",
                response_format={"type": "json_object"},
                temperature=0.3,
            )
        processing_answer=response.choices[0].message.content
        
        return processing_answer
    
    
class VideoScriptGeneratorExamplesDraft(BaseModel):
    GuideFor: str
    Status: str   
    
def create_draft_example(ExamplesDraft: VideoScriptGeneratorExamplesDraft):
    try:
        guide_path = f'Guides/On Process/{ExamplesDraft.GuideFor.lower().replace(" ", "_")}.json' # Guidefor a göre dosya ismini alıyoruz
        response_format_file = "/Users/abdulbarisoylemez/Desktop/Cinema8ProjectFinis/Guides/guide_templates/draft_example_tempate.json" # Bizim Examples içeriğinin formatını alıyoruz 

        with open(guide_path, "r") as file:
            draftExample = json.load(file)
            
            draft = draftExample["VideoDraft"]["Examples"] # Kontrol sistemlerinin belli bir sırada gerçekleşe bilmesi için Examples içeriklerini atıyoruz 
            outline = draftExample["VideoOutline"]["Examples"] 
            scenes = draftExample["VideoScenes"]["Examples"] 
            
            if "Examples" not in draftExample.get("VideoDraft", {}) or not isinstance(draftExample["VideoDraft"].get("Examples", []), list): # Bizim Example yapısını dick yapısınadan dizi yapısını dönüştürüyoruz 
                draft = []

            elif len(draft) == len(outline) == len(scenes): # Exsample içindeki örek sayılarının karşılaştırıyoruz , Toplam 3 farklı senaryo için 27 faklı olasılık hesaplandı
                # VideoDraft, VideoOutline ve VideoScenes koleksiyonlarında aynı sayıda örnek olduğunda:
                if ExamplesDraft.Status == "description_created":
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_draft_examples()
                    draft.append(json.loads(generated_video_text_examples))
                    
                elif ExamplesDraft.Status == "description_updated" and draft:
                    last_example_index = len(draft) - 1
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_draft_examples()
                    draft[last_example_index].update(json.loads(generated_video_text_examples))
                    

                else:
                    return {"status":"description_created needed"}

            elif len(draft) > len(outline) == len(scenes):
                # VideoDraft'daki örneklerin sayısı VideoOutline ve VideoScenes'teki örneklerin sayısından fazla olduğunda ve diğer iki koleksiyondaki örnek sayıları eşit olduğunda:
                if ExamplesDraft.Status == "description_updated"and draft:
                    last_example_index = len(draft) - 1
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_draft_examples()
                    draft[last_example_index].update(json.loads(generated_video_text_examples))
                    
                elif ExamplesDraft.Status == "description_created":
                    return {"status":"Couldn't create because [Draft->Example] is more"}
                        

        with open(guide_path, 'w') as f:
            json.dump(draftExample, f, indent=4)

        return {"Examples": draft}
    except Exception as e:
        return {"Error": str(e)}
    
class VideoScriptGeneratorExamplesOutline(BaseModel):
    GuideFor: str
    Status :str
    
def create_outline_example(ExamplesOutline: VideoScriptGeneratorExamplesOutline):
    
    try:
        guide_path = f'Guides/On Process/{ExamplesOutline.GuideFor.lower().replace(" ", "_")}.json'
        response_format_file = "/Users/abdulbarisoylemez/Desktop/Cinema8ProjectFinis/Guides/guide_templates/outline_example_template.json"

        with open(guide_path, "r") as file:
            outlineExample = json.load(file)
            draft = outlineExample["VideoDraft"]["Examples"]
            outline = outlineExample["VideoOutline"]["Examples"]
            scenes = outlineExample["VideoScenes"]["Examples"]
             
            if "Examples" not in outlineExample["VideoOutline"] or not isinstance(outline, list):
                outline = []
            
             
            elif (len(draft) > len(outline)) and (len(outline) == len(scenes)):
                if ExamplesOutline.Status == "description_created":
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_outline_examples()
                    outline.append(json.loads(generated_video_text_examples)) 
                   
                elif ExamplesOutline.Status == "description_updated" and outline:
                    last_example_index = len(outline) - 1
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_outline_examples()
                    outline[last_example_index].update(json.loads(generated_video_text_examples))
                    
                
                else:
                    return {"status":"No examples in outline, first create Draft examples"}

                
            elif (len(draft) == len(outline)) and (len(outline) > len(scenes) - 1):
                if ExamplesOutline.Status == "description_created":
                    return {"status":"Outline example can't be more then draft"}
                elif ExamplesOutline.Status == "description_updated":
                    last_example_index = len(outline) - 1
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_outline_examples()
                    outline[last_example_index].update(json.loads(generated_video_text_examples))
                    
                
            elif (len(draft)== len(outline)) and (len(outline) == len(scenes)):
                if ExamplesOutline.Status == "description_updated":
                    last_example_index = len(outline) - 1
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_outline_examples()
                    outline[last_example_index].update(json.loads(generated_video_text_examples))
                elif ExamplesOutline.Status == "description_created":
                    return {'status':'return to "create_draft" service'}
       

        with open(guide_path, 'w') as f:
            json.dump(outlineExample, f, indent=4)

        return {"Examples": outline}
    
    except FileNotFoundError:
        return {"error": "Dosya bulunamadı"}

class VideoScriptGeneratorExamplesScenes(BaseModel): 
    GuideFor: str
    Status : str 
        
def create_scenes_example(ExamplesScenes: VideoScriptGeneratorExamplesScenes):
        
    try:
        guide_path = f'Guides/On Process/{ExamplesScenes.GuideFor.lower().replace(" ", "_")}.json'
        response_format_file = "/Users/abdulbarisoylemez/Desktop/Cinema8ProjectFinis/Guides/guide_templates/scenes_example_template.json"

        with open(guide_path, "r") as file:
            scenesExample = json.load(file)
            
            draft = scenesExample["VideoDraft"]["Examples"]
            outline = scenesExample["VideoOutline"]["Examples"]
            scenes = scenesExample["VideoScenes"]["Examples"]
            
            if "Examples" not in scenesExample["VideoScenes"] or not isinstance(scenes, list):
                scenes = []

            elif ExamplesScenes.Status == "Finish":
                guide_filename = ExamplesScenes.GuideFor.lower().replace(" ", "_") + ".json"
                fil_path = "/Users/abdulbarisoylemez/Desktop/Cinema8ProjectFinis/Guides/Finis/" + guide_filename

                with open(fil_path, "w") as json_file:
                    json.dump(scenesExample, json_file, indent=4)

                return {"status": "Scenes example saved to file."}
            
            elif len(draft) > len(scenes) and len(outline) > len(scenes):
                if ExamplesScenes.Status == "description_created":
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_scenes_examples()
                    scenes.append(json.loads(generated_video_text_examples))
                    

                elif ExamplesScenes.Status == "description_updated":
                    if scenes:
                        generator = VideoScriptGenerator(guide_path, response_format_file)
                        generated_video_text_examples = generator.create_video_scenes_examples()
                        last_example_index = len(scenes) - 1
                        scenes[last_example_index].update(json.loads(generated_video_text_examples))
                        
                    else:
                        return {"error": "Couldn't update because there is no example in scenes. First create an example for scenes."}
                    

            elif len(scenes) == len(draft) and len(outline) == len(scenes):
                if ExamplesScenes.Status == "description_updated" and scenes: 
                    generator = VideoScriptGenerator(guide_path, response_format_file)
                    generated_video_text_examples = generator.create_video_scenes_examples()
                    last_example_index = len(scenes) - 1
                    scenes[last_example_index].update(json.loads(generated_video_text_examples))
                   

                elif ExamplesScenes.Status == "description_created":
                    return {"status": "Scenes example can't be more then draft and outline examples"}
                
            



        with open(guide_path, 'w') as f:
            json.dump(scenesExample, f, indent=4)
        return {"Examples": scenes}

            #return {"Examples": scenes}
    except FileNotFoundError:
        return {"error": "Dosya bulunamadı"}
    except Exception as e:
        return {"error": "Bilinmeyen bir hata oluştu"}
