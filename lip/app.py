from fastapi import FastAPI
import json
from guide_functions import *
from prompt_ai import VideoScriptGeneratorExamplesDraft,VideoScriptGeneratorExamplesOutline,VideoScriptGeneratorExamplesScenes, CreateMain,PromptSectionDescription, create_main, create_draft_example ,create_section_description,create_outline_example, create_scenes_example


app = FastAPI()
 
@app.post("/create_main")  
async def create_main_service(item: CreateMain):
    return create_main(item)
   
@app.post("/Create_Description")    
async def update_prompt(item: PromptSectionDescription):
    
    with open('Guides/On Process/' + item.GuideFor.lower().replace(' ', '_') + '.json', 'r') as f:
        main_data = json.load(f)
    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']
    
    if item.Status == "main_created" :
        result = await create_section_description(item)
        return {"status": "description_created", "data": result}
    
    elif item.Status == "description_created":
        result = await create_section_description(item)
        return {"status": "description_updated", "data": result}
    
    elif item.Status == 'Delete':
            for key in keys:
                if 'Examples' in main_data[key]:
                    del main_data[key]["Examples"]        
                    return {"status": "examples_deleted", "data": main_data}
                
    with open('Guides/On Process/' + item.GuideFor.lower().replace(' ', '_') + '.json', 'w') as f:
        json.dump(main_data, f, indent=4)

@app.post("/create_draft")
async def GenerateExample(ExamplesDraft: VideoScriptGeneratorExamplesDraft):
    if ExamplesDraft.Status == "main_created":
        return {"error": "Section Description needed"}
    else:
        return create_draft_example(ExamplesDraft)
    
@app.post("/create_outline")
async def GenerateExampleOutline(ExamplesOutline: VideoScriptGeneratorExamplesOutline):
    if ExamplesOutline.Status == "main_created":
        return {"error": "Section Description needed"}
    else:
        return create_outline_example(ExamplesOutline)

@app.post("/create_scenes")
async def GenerateExampleScenes(ExamplesScenes: VideoScriptGeneratorExamplesScenes):
    if ExamplesScenes.Status == "main_created":
        return {"error": "Section Description needed"}
    else:
        return create_scenes_example(ExamplesScenes)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)

