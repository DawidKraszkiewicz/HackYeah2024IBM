from openai import OpenAI
import os
OPENAI_KEY = os.getenv("OPENAI_KEY")

PROCESSOR_PROMPT = f'''
You are a text processing agent working with a description of a workout.


Extract specified values from the source text.
Return answer as a JSON format summary of the exercises in the workout structured as follows:
-"exercise_name" <string>
-"weight_kilograms" <number>
-"repetitions" <number>
-"sets" <number>
-"distance_kilometers" <number>
-"duration_minutes" <number>
-"kilocalories_burned" <number>


Calculate any missing values based on the source text.
Do any necessary conversions to metric units.
For kilocalories_burned, use the average kilocalories burned per minute / repetition / distance for a given exercise.
In the output do not include any calculations, conversions or any text besides the result JSON.
Do not infer any data based on previous training, strictly use only source text given below as input.

=====
'''


TRAINER_PROMPT = f'''
You are a personal trainer working with a client. You are provided with a list of a clients' previous workouts in a JSON format and their height, weight and age.
Based on the data, suggest the next workout for the client. It should be challenging but not too difficult. The provided data is structured as follows:
-"exercise_name" <string>
-"weight_kilograms" <number>
-"repetitions" <number>
-"sets" <number>
-"distance_kilometers" <number>
-"duration_minutes" <number>
-"kilocalories_burned" <number>

Do not infer any data based on previous training, strictly use only source text given below as input.
=====
'''

class TextProcessor:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_KEY
        )
    
    def workout_to_json(self, text):
        prompt = PROCESSOR_PROMPT + text
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
    
    def suggest_workout(self, text):
        prompt = TRAINER_PROMPT + text
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        result = completion.choices[0].message.content
        return result
    
