# -- Import section --
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# MODEL = 'text-ada-001'
MODEL = 'text-davinci-003'
# -- Initialization section --
app = Flask(__name__)
app.debug = True


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    global NEEL_STATE
    NEEL_STATE = {
        'curr_q': 0,
        'q': [],
        'f': [],
        'a': [],
        'prompt': ""
    }
    args = request.args.to_dict()
    input = args.get("input")
    if args.get("dluzano2"):
        print("dluzano2! ", url_for('dluzano2', input=input))
        return redirect(url_for('dluzano2', input=input), code=307)
    if args.get("neel4"):
        print("neel4! ", url_for('neel4', input=input))
        return redirect(url_for('neel4', input=input), code=307)
    if args.get("billjz2"):
        print("billjz2! ", url_for('billjz2', input=input))
        return redirect(url_for('billjz2', input=input), code=307)
    
    
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

@app.route("/billjz2")
def billjz2():
    args = request.args.to_dict()
    print(args)
    build_prompt_suffix = f'''Passage: {args.get('input')} 
    10 Questions:
    '''
    resp = openai.Completion.create(
        model=MODEL,
        prompt=billjz2_prompt + build_prompt_suffix,
        temperature=0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Topic:"]
    )
    print(resp)
    data = resp['choices'][0]['text'].replace("\n", "<br>")
    
    return render_template('billjz2.html', title='billjz2', data=data)



@app.route("/neel4")
def neel4():
    args = request.args.to_dict()
    print(args)
    if args.get('input'):

        build_prompt_suffix = f'''Passage: 
        {args.get('input')}
        Flashcards:
        Question 1:
        '''
        full_prompt = neel4_prompt + build_prompt_suffix

        resp = openai.Completion.create(
            model=MODEL,
            prompt=full_prompt,
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["Answer:"]
        )
        print(resp)
        data = resp['choices'][0]['text']
        NEEL_STATE['curr_q'] = 1 
        NEEL_STATE['q'].append(data)
        NEEL_STATE['prompt'] = full_prompt

        
    else:
        ans = args.get('answer')
        NEEL_STATE['a'].append(ans)
        print(ans)
        NEEL_STATE['prompt'] = NEEL_STATE['prompt'] + "\n Answer:" + ans
        resp = openai.Completion.create(
            model=MODEL,
            prompt=NEEL_STATE['prompt'],
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["Answer:"]
        )

        lines = resp['choices'][0]['text'].split("\n")
        print(lines)
        # print(NEEL_STATE)
        NEEL_STATE['q'].append(lines[1])
        NEEL_STATE['f'].append(lines[0])
        NEEL_STATE['curr_q'] = NEEL_STATE['curr_q'] + 1        
    return render_template('neel4.html', title='neel4', data=NEEL_STATE)


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
Study Notes:
• Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into chemical energy. 
• This chemical energy is used to produce carbohydrates, such as glucose, from carbon dioxide and water. 
• Photosynthesis occurs in two stages: the light-dependent reactions and the Calvin cycle. 
• During the light-dependent reactions, light energy is absorbed by chlorophyll molecules and converted into chemical energy. 
• This energy is then used to produce ATP and NADPH, which are used in the Calvin cycle to produce carbohydrates from carbon dioxide. 
• The Calvin cycle also requires the presence of enzymes, such as rubisco, and other molecules, such as ribulose biphosphate. 
• Photosynthesis is an essential process for all life on Earth, as it provides the energy needed for plants to grow and produce oxygen.
'''

neel4_prompt = '''Generate free response questions,  example answers, and corresponding feedback based on the following passage.

Passage: 
A computer is a digital electronic machine that can be programmed to carry out sequences of arithmetic or logical operations (computation) automatically. Modern computers can perform generic sets of operations known as programs. These programs enable computers to perform a wide range of tasks. A computer system is a nominally complete computer that includes the hardware, operating system (main software), and peripheral equipment needed and used for full operation. This term may also refer to a group of computers that are linked and function together, such as a computer network or computer cluster. A broad range of industrial and consumer products use computers as control systems. Simple special-purpose devices like microwave ovens and remote controls are included, as are factory devices like industrial robots and computer-aided design, as well as general-purpose devices like personal computers and mobile devices like smartphones. Computers power the Internet, which links billions of other computers and users. Early computers were meant to be used only for calculations. Simple manual instruments like the abacus have aided people in doing calculations since ancient times. Early in the Industrial Revolution, some mechanical devices were built to automate long tedious tasks, such as guiding patterns for looms. More sophisticated electrical machines did specialized analog calculations in the early 20th century. The first digital electronic calculating machines were developed during World War II. The first semiconductor transistors in the late 1940s were followed by the silicon-based MOSFET (MOS transistor) and monolithic integrated circuit (IC) chip technologies in the late 1950s, leading to the microprocessor and the microcomputer revolution in the 1970s. The speed, power and versatility of computers have been increasing dramatically ever since then, with transistor counts increasing at a rapid pace (as predicted by Moore's law), leading to the Digital Revolution during the late 20th to early 21st centuries. Conventionally, a modern computer consists of at least one processing element, typically a central processing unit (CPU) in the form of a microprocessor, along with some type of computer memory, typically semiconductor memory chips. The processing element carries out arithmetic and logical operations, and a sequencing and control unit can change the order of operations in response to stored information. Peripheral devices include input devices (keyboards, mice, joystick, etc.), output devices (monitor screens, printers, etc.), and input/output devices that perform both functions (e.g., the 2000s-era touchscreen). Peripheral devices allow information to be retrieved from an external source and they enable the result of operations to be saved and retrieved.
Question: What is a computer?
Answer: A computer is a digital electronic machine that can be programmed to carry out sequences of arithmetic or logical operations automatically. 
Feedback: Correct! Computers can be programmed to carry out a variety of tasks, enabling them to be used in a wide range of contexts.
Question: What components are typically found in a modern computer?
Answer: A modern computer typically includes a central processing unit (CPU) in the form of a microprocessor, along with some type of computer memory, typically semiconductor memory chips, and peripheral devices such as input, output, and input/output devices.
Feedback: Correct! A modern computer is composed of several components that enable it to perform a range of operations.
Question: How has computer technology changed over the years?
Answer: Computer technology has been rapidly increasing since the introduction of semiconductor transistors and monolithic integrated circuits in the late 1950s, leading to the Digital Revolution during the late 20th to early 21st centuries.
Feedback: Correct! Computer technology has been rapidly increasing since the 1950s, leading to the Digital Revolution.
Question: What is Moore's Law?
Answer: Moore's Law is an observation that the transistor count of integrated circuits doubles approximately every two years. 
Feedback: Correct! Moore's Law has been a reliable predictor of the speed, power and versatility of computers since its observation in the mid-1960s.

Passage: 
Plants are predominantly photosynthetic eukaryotes of the kingdom Plantae. Historically, the plant kingdom encompassed all living things that were not animals, and included algae and fungi; however, all current definitions of Plantae exclude the fungi and some algae, as well as the prokaryotes (the archaea and bacteria). By one definition, plants form the clade Viridiplantae (Latin name for "green plants") which is sister of the Glaucophyta, and consists of the green algae and Embryophyta (land plants). The latter includes the flowering plants, conifers and other gymnosperms, ferns and their allies, hornworts, liverworts, and mosses. Most plants are multicellular organisms. Green plants obtain most of their energy from sunlight via photosynthesis by primary chloroplasts that are derived from endosymbiosis with cyanobacteria. Their chloroplasts contain chlorophylls a and b, which gives them their green color. Some plants are parasitic or mycotrophic and have lost the ability to produce normal amounts of chlorophyll or to photosynthesize, but still have flowers, fruits, and seeds. Plants are characterized by sexual reproduction and alternation of generations, although asexual reproduction is also common. There are about 320,000 known species of plants, of which the great majority, some 260,000–290,000, produce seeds.[5] Green plants provide a substantial proportion of the world's molecular oxygen,[6] and are the basis of most of Earth's ecosystems. Plants that produce grain, fruit, and vegetables also form basic human foods and have been domesticated for millennia. Plants have many cultural and other uses, as ornaments, building materials, writing material and, in great variety, they have been the source of medicines and psychoactive drugs. The scientific study of plants is known as botany, a branch of biology.
Question: What is the scientific study of plants called?
Answer: The scientific study of plants is called botany.
Feedback: Correct! Botany is the scientific study of plants and is a branch of biology.
Question: What is the historical definition of the plant kingdom?
Answer: Historically, the plant kingdom encompassed all living things that were not animals, and included algae and fungi.
Feedback: Correct! Historically, the plant kingdom included all living things that were not animals and encompassed algae and fungi.
Question: How do green plants obtain energy?
Answer: Green plants obtain energy from sunlight via photosynthesis by primary chloroplasts that are derived from endosymbiosis with cyanobacteria.
Feedback: Correct! Green plants obtain energy from sunlight via photosynthesis by primary chloroplasts derived from endosymbiosis with cyanobacteria.
Question: What are some common uses of plants?
Answer: Plants have many uses, including as ornaments, building materials, writing material, and sources of food, medicines, and psychoactive drugs.
Feedback: Correct! Plants have many uses, from decorative to medicinal and psychoactive.
'''

# center, put text in boxes, 

billjz2_prompt = '''I am a model that reads a passage and outputs a multiple choice quiz with 4 selections and the answers to the questions based on the passage.

Passage: Illinois Industrial University

The University of Illinois, originally named "Illinois Industrial University", was one of the 37 universities created under the first Morrill Land-Grant Act, which provided public land for the creation of agricultural and industrial colleges and universities across the United States. Among several cities, Urbana was selected in 1867 as the site for the new school.[22][23] From the beginning, President John Milton Gregory's desire to establish an institution firmly grounded in the liberal arts tradition was at odds with many state residents and lawmakers who wanted the university to offer classes based solely around "industrial education".[24] The university opened for classes on March 2, 1868, and had two faculty members and 77 students.[25]

John Milton Gregory, the university's first president
The Library, which opened with the school in 1868, started with 1,039 volumes. Subsequently, President Edmund J. James, in a speech to the board of trustees in 1912, proposed to create a research library. It is now one of the world's largest public academic collections.[23][26][27] In 1870, the Mumford House was constructed as a model farmhouse for the school's experimental farm. The Mumford House remains the oldest structure on campus.[28] The original University Hall (1871) was the fourth building built; it stood where the Illini Union stands today.[29]

University of Illinois
In 1885, the Illinois Industrial University officially changed its name to the "University of Illinois", reflecting its agricultural, mechanical, and liberal arts curriculum.[24]

During his presidency, Edmund J. James (1904–1920) is credited for building the foundation for the large Chinese international student population on campus.[30][31][32][33] James established ties with China through the Chinese Minister to the United States Wu Ting-Fang.[33] In addition, during James's presidency, class rivalries and Bob Zuppke's winning football teams contributed to campus morale.[23]

Alma Mater statue by Lorado Taft

Morrow Plots in front of the Carl R. Woese Institute for Genomic Biology
Alma Mater, a prominent statue on campus created by alumnus Lorado Taft, was unveiled on June 11, 1929. It was established from donations by the Alumni Fund and the classes of 1923–1929.[34]

The Great Depression slowed construction and expansion on the campus. The university replaced the original university hall with Gregory Hall and the Illini Union. After World War II, the university experienced rapid growth. The enrollment doubled and the academic standing improved.[35] This period was also marked by large growth in the Graduate College and increased federal support of scientific and technological research. During the 1950s and 1960s the university experienced the turmoil common on many American campuses. Among these were the water fights of the fifties and sixties.[36]

University of Illinois at Urbana-Champaign
By 1967 the University of Illinois system consisted of a main campus in Champaign-Urbana and two Chicago campuses, Chicago Circle (UICC) and Medical Center (UIMC), and people began using "Urbana-Champaign" or the reverse to refer to the main campus specifically. The university name officially changed to the "University of Illinois at Urbana-Champaign" by 1977. While this was a reversal of the commonly used designation for the metropolitan area, "Champaign-Urbana," most of the campus is located in Urbana. The name change established a separate identity for the main campus within the University of Illinois system, which today includes campuses in Springfield (UIS) and Chicago (UIC) (formed by the merger of UICC and UIMC).

In 1998, the Hallene Gateway Plaza was dedicated. The Plaza features the original sandstone portal of University Hall, which was originally the fourth building on campus.[29] In recent years, state support has declined from 4.5% of the state's tax appropriations in 1980 to 2.28% in 2011, a nearly 50% decline.[37] As a result, the university's budget has shifted away from relying on state support with nearly 84% of the budget coming from other sources in 2012.[38]

On March 12, 2015, the Board of Trustees approved the creation of a medical school, the first college created at Urbana-Champaign in 60 years.[39][40][41] The Carle-Illinois College of Medicine began classes in 2018.[42]

Philanthropy
Over the last twenty years state funding for the university has fallen. Private philanthropy increasingly supplements revenue from tuition and state funding, providing about 19% of the annual budget in 2012.[38] Notable among significant donors, alumnus entrepreneur Thomas M. Siebel has committed nearly $150 million to the university, including $36 million to build the Thomas M. Siebel Center for Computer Science and $25 million to build the Siebel Center for Design. Further the Grainger Foundation (founded by alumnus W. W. Grainger) has contributed more than $300 million to the university over the last half-century,[citation needed] including donations for the construction of the Grainger Engineering Library. Larry Gies and his wife Beth donated $150 million in 2017 to the shortly thereafter renamed Gies College of Business.[43]

10 Questions:

Q1. What is the original name of the University of Illinois?
A. University of Illinois at Urbana-Champaign
B. Illinois Industrial University
C. University Hall
D. Urbana School

Answer: B. Illinois Industrial University

Q2. What was the first building built on the University of Illinois campus?
A. Library
B. Illini Union
C. Mumford House
D. University Hall

Answer: D. University Hall

Q3. Who is credited for building the foundation for the large Chinese international student population on campus?
A. Edmund J. James
B. John Milton Gregory
C. Thomas M. Siebel
D. W. W. Grainger

Answer: A. Edmund J. James

Q4. What was the name of the statue unveiled on June 11, 1929?
A. Illini Union
B. Library
C. Alma Mater
D. Mumford House

Answer: C. Alma Mater

Q5. What percentage of the university's budget came from state support in 1980?
A. 19%
B. 84%
C. 4.5%
D. 2.28%

Answer: C. 4.5%

Q6. What did the Morrill Land-Grant Act provide?
A. Private philanthropy
B. Public land
C. Agricultural and industrial colleges
D. Classes based solely around industrial education

Answer: B. Public land

Q7. What is the name of the college that began classes in 2018?
A. Thomas M. Siebel Center for Computer Science
B. Grainger Engineering Library
C. Gies College of Business
D. Carle-Illinois College of Medicine

Answer: D. Carle-Illinois College of Medicine

Q8. When did the University of Illinois open for classes?
A. June 11, 1929
B. March 12, 2015
C. March 2, 1868
D. April 2, 1912

Answer: C. March 2, 1868

Q9. What did President Edmund J. James propose to create in 1912?
A. A research library
B. A model farmhouse
C. A class rivalry
D. A football team

Answer: A. A research library

Q10. Who founded the Grainger Foundation?
A. Larry Gies
B. Thomas M. Siebel
C. W. W. Grainger
D. John Milton Gregory

Answer: C. W. W. Grainger'''