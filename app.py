# -- Import section --
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = 'text-ada-001'
# -- Initialization section --
app = Flask(__name__)
app.debug = True


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    args = request.args.to_dict()
    input = args.get("input")
    if args.get("dluzano2"):
        print("dluzano2! ", url_for('dluzano2', input=input))
        return redirect(url_for('dluzano2', input=input), code=307)
    
    return render_template('index.html')
        


@app.route("/dluzano2")
def dluzano2():
    args = request.args.to_dict()
    print(args)
    build_prompt_suffix = f'''Topic: {args.get('input')} 
    Study Notes:
    '''
    resp = openai.Completion.create(
        model=MODEL,
        prompt=dluzano2_prompt + build_prompt_suffix,
        temperature=0,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Topic:"]
    )
    print(resp)
    data = resp['choices'][0]['text']
    data = data.split("\u2022")
    
    return render_template('dluzano2.html', title='Dluzano2', data=data)



dluzano2_prompt = '''Generate study notes when given a topic.
Topic: The Fall of the Berlin Wall
Study Notes: 
• The Berlin Wall was a barrier that separated East and West Berlin from 1961-1989. 
• The wall was built by the German Democratic Republic (GDR) to prevent East Germans from fleeing to the West. 
• The fall of the Berlin Wall was a major event in the history of the Cold War and marked the end of the Soviet Union’s control over East Germany. 
• The fall of the wall was a result of a series of events, including the growing dissatisfaction of East Germans with the GDR’s oppressive rule, the rise of pro-democracy movements in East Germany, and the increasing pressure from Western countries. 
• On November 9, 1989, the East German government announced that citizens of East and West Germany would be allowed to travel freely between the two countries. 
• This announcement sparked a wave of celebration and jubilation in Berlin and other cities in East Germany. 
• The fall of the Berlin Wall symbolized the end of the Cold War and the reunification of Germany.

Topic: Mitosis
Study Notes: 
• Mitosis is a type of cell division that produces two identical daughter cells from a single parent cell. 
• It is a part of the cell cycle, which is the process by which cells reproduce. 
• During mitosis, the genetic material in the parent cell is replicated and then divided into two identical sets of chromosomes. 
• The chromosomes are then distributed into two new daughter cells. 
• Mitosis consists of four main stages: prophase, metaphase, anaphase, and telophase. 
• During prophase, the chromosomes condense and the nuclear envelope breaks down. 
• During metaphase, the chromosomes line up in the center of the cell. 
• During anaphase, the chromosomes are pulled apart and move to opposite sides of the cell. 
• During telophase, the chromosomes decondense and the nuclear envelope reforms. 
• After telophase, the cell splits into two daughter cells.

Topic: Deep Learning
Study Notes: 
• Deep learning is a type of artificial intelligence (AI) that uses algorithms to learn from data and make predictions. 
• It is a subset of machine learning, which is a branch of AI that focuses on developing algorithms that can learn from data without being explicitly programmed. 
• Deep learning algorithms use multiple layers of neurons, or nodes, to process data and make predictions. 
• These algorithms are able to learn complex patterns and relationships in data, which makes them useful for a variety of applications, such as computer vision, natural language processing, and robotics. 
• Deep learning algorithms are trained using large datasets and powerful computing resources, such as GPUs. 
• Deep learning has become increasingly popular in recent years due to its ability to solve complex problems and its potential to revolutionize many industries.

Topic: Photosynthesis
• Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. 
• This chemical energy is used to produce carbohydrates, such as glucose, from carbon dioxide and water. 
• Photosynthesis occurs in two stages: the light-dependent reactions and the Calvin cycle. 
• During the light-dependent reactions, light energy is absorbed by chlorophyll molecules and converted into chemical energy. 
• This energy is then used to produce ATP and NADPH, which are used in the Calvin cycle to produce carbohydrates from carbon dioxide. 
• The Calvin cycle also requires the presence of enzymes, such as rubisco, and other molecules, such as ribulose biphosphate. 
• Photosynthesis is an essential process for all life on Earth, as it provides the energy needed for plants to grow and produce oxygen.

'''