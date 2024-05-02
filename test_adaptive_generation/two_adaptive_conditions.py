import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()
key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=key)

df = pd.read_excel("test_two_kid.xlsx")


# I want to iterate df and use the first element as each row as the key of a dictionary 
# and all the other elements as the values of the dictionary
# generate the code
def get_child_history(df):

    my_dict = {}

    for i in range(len(df)):
        row = df.iloc[i]
        child_id = row[0]
        listOfAnswers = my_dict.get(child_id, "")
        listOfAnswers += (f'{{ question_id: {row[1]} | question: {row[2]} | response: {row[3]} | accuracy: {row[4]} }} ')
        my_dict[child_id] = listOfAnswers
    return my_dict


def get_learning_summary(df):
    child_history = get_child_history(df)
    results = []
    for child_id in child_history:
        completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "I want you to act 'as' a preschool teacher. Your role is to evaluate children’s learning progress based on their responses to science questions so that you know what kinds of questions to ask next. The user will provide children's answers to a set of science questions, including question, child answer, whether it is accurate. Please generate a learning summary based on the information provided by the user, including: 1. Science knowledge mastered 2. Misconceptions 3. Levels of engagement. Keep your summary brief."},
            {"role": "user", "content": f"{child_history[child_id]}"}
        ]
        )
        result_text = completion.choices[0].message.content
        results.append({'child_id': child_id, 'summary': result_text})
        print(result_text)
        # Creating DataFrame from results
    result_df = pd.DataFrame(results)
        # Writing to Excel file
    result_df.to_excel("learning_summaries.xlsx", index=False)
    print("\n learning_summaries.xlsx was saved locally.")

    return 





# get_learning_summary(df)


def get_next_question():
    df_history = pd.read_excel("learning_summaries.xlsx")
    df_show = pd.read_excel("lucky_shirt_base.xlsx")

    instruction_with_seed = """
        You are a conversational agent designed to interact with young children aged 3 to 6 for science learning. Your role is to ask proper questions from an educational story like a preschool teacher based on children’s previous understanding of the knowledge.

        The user will provide the child's learning history summary, current part of the story, one exemplar question based on the learning materials. The exemplar question provides a good example of the length of the question, the intention of the question, and the language style.

        You should review the learning summary to understand what the child has mastered, the misconceptions and levels of engagement. 

        You should generate one question based on the story. Your question should only contain one single question, do not include any subquestion.

        You should consider the exemplar question and adapt its content or difficulty to reflect children's learning history when you think it's necessary.

        Only return the question.

        """
    
    instruction_without_seed = """
        You are a conversational agent designed to interact with young children aged 3 to 6 for science learning. Your role is to ask proper questions from an educational story like a preschool teacher based on children’s previous understanding of the knowledge.

        The user will provide the child's learning history summary and the current part of the story.

        You should review the learning summary to understand what the child has mastered, the misconceptions and levels of engagement. 

        You should generate one question based on the story. 

        Only return the question.

        """
    results = []
    for i in range(len(df_history)):
        summary = df_history.iloc[i][1]
        child_id = df_history.iloc[i][0]
        for j in range(len(df_show)):
            row = df_show.iloc[j]
            story_id =row[0]
            story = row[1]
            seed = row[2]
            user_content_with_seed = f"Learning summary: {summary} | Story: {story} | Exemplar Question: {seed}"
            user_content_without_seed = f"Learning summary: {summary} | Story: {story}"
            completion_with_seed = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"{instruction_with_seed}"},
                    {"role": "user", "content": f"{user_content_with_seed}"}
                ]
                )
            completion_without_seed = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"{instruction_without_seed}"},
                    {"role": "user", "content": f"{user_content_without_seed}"}
                ]
                )
            result_text_with_seed = completion_with_seed.choices[0].message.content
            result_text_without_seed = completion_without_seed.choices[0].message.content
            results.append({'child_id': child_id, 'story_id': story_id, 'summary': summary, 'question_with_seed': result_text_with_seed, 'question_without_seed': result_text_without_seed})
            print(results[len(results)-1])
        # Creating DataFrame from results
        result_df = pd.DataFrame(results)
        # Writing to Excel file
        result_df.to_excel("generated_questions.xlsx", index=False)
    return
            
get_next_question()

