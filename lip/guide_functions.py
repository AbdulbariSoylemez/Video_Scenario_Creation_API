import json



def update_main_data_function(main_data, item):
    
    main_data.update({
        'GuideFor': item.GuideFor,
        'Description': item.Description,
        'TargetAudienceCharacteristics': item.TargetAudienceCharacteristics,
        'ContentObjectives': item.ContentObjectives,
        'CalltoAction': item.CalltoAction, 
        'SuccessMetrics': item.SuccessMetrics,
        'IsAdditionalInformationNeeded': item.IsAdditionalInformationNeeded,
        'Platforms': item.Platforms,
        'EstimatedDuration': item.EstimatedDuration
    })
    main_data['Prerequisites']['TopicSelection'] = item.TopicSelection
    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']
    for key in keys:
        main_data[key]['Prerequisites']['TopicSelection'] = item.TopicSelection
    return {"success": True, "response": main_data}
          
def update_additional_information_function(data, item):
    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']
    result = {"success": False, "message": ""}
    
    
    if data['IsAdditionalInformationNeeded'] == True:    
        data['Prerequisites']['AdditionalInformation'] = item.AdditionalInformation  
    else: 
        if 'AdditionalInformation' in data['Prerequisites']:
            del data['Prerequisites']['AdditionalInformation']

    for key in keys:
        if 'AdditionalInformation' not in data[key]['Prerequisites']:
            data[key]['Prerequisites']['AdditionalInformation'] = {}

        if data['IsAdditionalInformationNeeded'] == True:
            data[key]['Prerequisites']['AdditionalInformation'] = item.AdditionalInformation  
            result["success"] = True
            result["message"] = "Additional Information has been added successfully"
        else: 
            if 'AdditionalInformation' in data[key]['Prerequisites']:
                del data[key]['Prerequisites']['AdditionalInformation']
                result["success"] = False
                result["message"] = "Additional Information was not added because it is not needed"

    return result
                         
def section_description_function(section_data, item):


    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']

    for key in keys:
        section_data[key]['SectionDescription'] = item.SectionDescription
        
        
        with open('template/draft_example_template.json', 'r') as e:
            example_data = json.load(e)
        section_data['VideoDraft']['Examples'] = example_data


        
def example_prerequisites(data, item):
         
    keys = ['VideoDraft', 'VideoOutline', 'VideoScenes']

    for key in keys:

        if 'Inputs' in data[key]['Examples'] and 'Prerequisites' in data[key]['Examples']['Inputs']:
            data[key]['Examples']['Inputs']['Prerequisites']['TopicSelection'] = item.TopicSelection
            
        if data['IsAdditionalInformationNeeded'] == True:    
            if 'Inputs' in data[key]['Examples'] and 'Prerequisites' in data[key]['Examples']['Inputs']:
                data[key]['Examples']['Inputs']['Prerequisites']['AdditionalInformation'] = item.AdditionalInformation
        else:
            del data[key]['Examples']['Inputs']['Prerequisites']['AdditionalInformation']
        
        data[key]['Examples']['Inputs']['Platforms'] = item.Platforms
        data[key]['Examples']['Inputs']['EstimatedDuration'] = item.EstimatedDuration
        


    