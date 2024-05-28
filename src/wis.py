from datetime import datetime, timedelta
import whisper
import sys
import json
import os
def format_delta_time(seconds):
        m, s = divmod(seconds, 60)
        # Format in "0:00:00.xxx"
        formatted_time = f'{int(m)}.{int(s)}'
        return formatted_time
def convert_audio():

    video_files = [f for f in os.listdir("input_files")]

    for item in video_files:
        json_file = os.path.join("output_data", f"{item[:-4]}.v4.json")
        model = whisper.load_model("base")
        result = model.transcribe(os.path.join("input_files", item), language="en", fp16=False, verbose=True)
        all = {}
        sentences = []
        
        for index, segment in enumerate(result['segments']):
            sentence = {}

            start = format_delta_time(segment['start'])
            end = format_delta_time(segment['end'])

            sentence['sentence'] = segment['text'].strip()
            sentence['starttime'] = start
            sentence['endtime'] = end
            sentences.append(sentence)
        all['metadata'] =  {
            "text_id": item[:-4] + '.mp4',
            "collection": item[:-4],
            "file": "/db/tv/2016/2016-02/2016-02-02/2016-02-02_0000_US_FOX-News_On_the_Record_with_Greta_Van_Susteren.txt",
            "date": "2016-02-02",
            "year": "2016",
            "month": "02",
            "day": "02",
            "time": "0000",
            "duration": "0:59:54.87",
            "country": "US",
            "channel": item[:-4],
            "title": item[:-4],
            "video_resolution": "640x352",
            "video_resolution_original": "1920x1088",
            "language": "ENG",
            "recording_location": "UCLA Library",
            "original_broadcast_date": "N/A",
            "original_broadcast_time": "N/A",
            "original_broadcast_timezone": "N/A",
            "local_broadcast_date": "2016-02-01",
            "local_broadcast_time": "16:00",
            "local_broadcast_timezone": item[:-4]
            }
        all['sentences'] = sentences

        with open(json_file, 'w') as fp:
            json.dump(all, fp)
        


    


convert_audio()
