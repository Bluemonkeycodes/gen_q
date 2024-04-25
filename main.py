import os
from dotenv import load_dotenv
from openai import OpenAI
import time


load_dotenv()
key = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=key)


"""
Condition 1: generate 16 questions based on the learning materials provided by the user.
Condition 2: generate one question for each question category under different levels based on the learning materials provided by the user. (list the levels and categories below)
Condition 3: Given the learning materials and the question provided by the user, first, classify the question into its corresponding level and category. Then, adapt the user-provided question into each of the 16 categories. (list the levels and categories below)
"""

#Stores to file 1,2 or 3 depending on which condition is being tested 
condition = 1 
num_questions = 16

#date stamp responses


#We can move to file if needed
text = """Ari says, WHAT? NAH.

[Grunting]

Ari says, I CAN'T MOVE MY
ARMS VERY MUCH, BUT IT'S FINE.

I JUST HAVEN'T WORN IT IN A
WHILE. I'M SURE IT WILL STRETCH
OUT. NOW, LET'S PLAY SOCCER.

[Grunting, Olive clears her throat]

Olive opens a door for Ari.

[Creak]

Olive says, HERE YOU GO.

Elinor picks up a green shirt.

[Rustling]

Elinor says, HMM. I'LL ALSO BRING
A BIGGER SHIRT. YOU KNOW, JUST
IN CASE.

Ari says, OKAY, BUT WE WON'T NEED
IT. WE HAVE MY LUCKY SHIRT ON
OUR SIDE. WHOA.

[Boing]

Ari says, WHOA, WHOA.

Olive, Elinor, and Ari arrive at a soccer field.

Ari asks, WHO'S READY TO BE
A SUPER SOCCER GOALIE?

Olive notices Ranger Rabbit standing beside a goal net.

Olive asks, RANGER RABBIT?

Ari says, NO. I MEANT ME.

NOW THAT I HAVE MY LUCKY SHIRT,
I'M GOING TO STOP EVERY BALL.
THE ONES TO THE LEFT... HA.

...AND THE ONES TO THE RI--OOPS.

Ranger Rabbit says, CAREFUL THERE,
ARI. HI, KIDS.

Elinor says, HI, MOM.
WHAT ARE YOU DOING HERE?

Ranger Rabbit says, WELL, THERE
WAS AN ANIMAL ON THE SOCCER
FIELD THAT SHOULDN'T BE THERE,
SO I CAME TO TAKE IT BACK TO THE
FOREST WHERE IT BELONGS.

Olive says, OOH. WHAT IS IT?

[Rustling]

Ranger Rabbit says, IT'S A CUTE
LITTLE BABY GARTER SNAKE.

[Hiss, Ari screams]

Ari says, SNAKE?

[Grunting]

Ari says, LITTLE HELP, PLEASE?

[Rustling]

Ranger Rabbit says, NOW, REMEMBER,
KIDS, IF YOU SEE A SNAKE, YOU
SHOULDN'T GET NEAR IT UNLESS
YOU'RE WITH A GROWN-UP
LIKE ME.

Elinor asks, ARE SNAKES
DANGEROUS, MOM?

Ranger Rabbit says, SOME ARE.
THIS ONE ISN'T POISONOUS,
BUT IT CAN STILL BITE, SO WE
HAVE TO BE CAREFUL.

AND IT'S A LIVING CREATURE,
SO WE SHOULD TREAT IT WITH
GENTLENESS AND RESPECT.

[Insects chirp, hissing]

Olive says, LOOK AT ITS TONGUE
FLICKING. WHY DOES IT DO THAT?

Ranger Rabbit says, TO SMELL
THINGS. SNAKES SMELL WITH
THEIR TONGUES.
"""

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": f"You are a conversational AI designed to interact with young children aged 3 to 6. Your role is to ask proper educational questions like a preschool teacher. "},
    {"role": "user", "content": f"Generate {num_questions} questions that you would ask a child in this age group about the given text. Below \n {text}"}
  ]
)

# Read the existing content
with open(f"response_{condition}.txt", "r") as file:
    old_content = file.read()

# Write the new content followed by the old content
with open(f"response_{condition}.txt", "w") as file:
    file.write("["+time.strftime("%Y-%m-%d %H:%M:%S") + "]\n")
    file.write(str(completion.choices[0].message.content) + "\n")
    file.write(old_content)