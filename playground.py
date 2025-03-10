import streamlit as st  # Import the Streamlit library for creating interactive web apps

class SymbolicKnowledge:
    def __init__(self):
        # This part sets up a "knowledge base" which is like a container for our facts and rules.
        self.knowledge = {}  # A dictionary to store facts (concepts and their relationships).
        self.rules = [rule1, rule2, rule3]      # A list to store the "rules" that the AI uses to think.

    def add_concept(self, concept):        # This function adds a new "concept" (like "Dog" or "Animal") to our knowledge base.
        if concept not in self.knowledge:
            self.knowledge[concept] = {}  # If the concept is new, create a space for it.

    def add_relation(self, concept1, relation, concept2):
        # This function adds a "relationship" between two concepts.
        # For example, "Dog is Mammal" or "Car uses FuelData".
        self.add_concept(concept1)  # Make sure both concepts exist.
        self.add_concept(concept2)
        if relation not in self.knowledge[concept1]:
            self.knowledge[concept1][relation] = []  # If the relation is new, create a space for it.
        self.knowledge[concept1][relation].append(str(concept2))  # Add the relationship to the knowledge base.

    def add_rule(self, rule):
        # This function adds a new "rule" to our AI's thinking process.
        self.rules.append(rule)

    def infer(self, question):
        print(f"Inferring: {question}")
        results = []
        for rule in self.rules:
            print(f"Applying rule: {rule.__name__}")
            result = rule(self.knowledge, question)
            if result is not None:
                results.extend(result)
        print(f"Results: {results}")
        return results

def _check_transitive_relation(knowledge, subject, target):
    if target in [str(x) for x in knowledge.get(subject, {}).get("is",[])]:
        return [f"{subject} is {target} (inferred)"]
    for intermediate in knowledge.get(subject, {}).get("is", []):
        if intermediate in knowledge and "is" in knowledge[intermediate]:
            if target in [str(x) for x in knowledge[intermediate]["is"]]:
                return [f"{subject} is {target} (inferred)"]
            else:
                result = _check_transitive_relation(knowledge, intermediate, target)
                if result:
                    return result
    return None


# Example Rules (Illustrating EU AI Act & Data Act Concerns)
def rule1(knowledge, question):  # Rule 1: Basic Inference (Transparency)
    # This rule checks basic "is" relationships.
    # It helps show how the AI can explain its reasoning (transparency).
    if len(question) == 3:
        subject, _, target = question
        if subject in knowledge and _ in knowledge[subject]:
            print(f"Within In Rule 1 :  {subject,_,target}")
            if target in [str(x) for x in knowledge[subject][_]]:
                return [f"{subject} is {target} (inferred)"]
            else:
                return _check_transitive_relation(knowledge, subject, target)
    return None

def rule2(knowledge, question):  # Rule 2: Data Quality Check
    # This rule checks if data has certain attributes.
    # It helps show how the AI can check data quality (EU AI Act).
    if len(question) == 3 and question[1] == "has":
        subject, _, attribute = question
        print(f"Within In Rule 2 :  {subject,_,attribute}")
        if subject in knowledge and "has" in knowledge[subject]:
            if attribute in knowledge[subject]["has"]:
                return [f"{subject} has {attribute} (verified)"]
        else:
            return [f"Data Quality Issue: Missing or Inconsistent Data for {subject}"]
    return None

def rule3(knowledge, question):  # Rule 3: Data Privacy (Simplified)
    # This rule checks if data is "sensitive".
    # It helps show how the AI can consider data privacy (EU Data Act).
    if len(question) == 3 and question[1] == "uses":
        subject, _, data_source = question
        if subject in knowledge and "uses" in knowledge[subject]:
            print(f"Within In Rule 3 :  {subject,_,data_source}")
            if "sensitive" in knowledge[data_source]["has"]:
                return [f"Data Privacy Concern: {subject} uses sensitive data from {data_source}"]
    return None

if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = SymbolicKnowledge()  # Create our knowledge base if it doesn't exist.
knowledge_base = st.session_state.knowledge_base  # Get the knowledge base.

st.title("Symbolic Reasoning Playground (EU AI Act & Data Act Considerations)")  # Title of our web app.

# Input for adding relations
st.subheader("Add Relation")  # Section for adding relationships.
concept1 = st.text_input("Concept 1")  # Input box for the first concept.
relation = st.text_input("Relation")  # Input box for the relationship.
concept2 = st.text_input("Concept 2")  # Input box for the second concept.

if st.button("Add Relation"):  # Button to add the relation.
    knowledge_base.add_relation(concept1, relation, concept2)
    st.success(f"Relation added: {concept1} {relation} {concept2}")  # Show a success message.

# Input for adding data source properties
st.subheader("Add Data Source Properties") # Section for adding properties.
data_source = st.text_input("Data Source") # input box for the data source
property = st.text_input("Property")  # e.g., "sensitive" # Input box for the property.

if st.button("Add Data Source Property"): # button to add the property.
    knowledge_base.add_relation(data_source, "has", property)
    st.success(f"Property added: {data_source} has {property}")

# Input for questions
st.subheader("Ask a Question") # section to ask questions.
question_input = st.text_input("Enter question (e.g., Dog is animal)") # input box for questions.

if st.button("Infer"): # button to infer.
    question = tuple(question_input.split()) # convert the input into a format the AI understands.
    results = knowledge_base.infer(question) # get the results
    if results:
        for result in results:
            st.write(result) # show the results.
    else:
        st.write("No inference found.") # show a message if no answer is found.

# Display current knowledge.
st.subheader("Current Knowledge")
st.write(knowledge_base.knowledge) # shows all the relationships and concepts.

# Display current rules.
st.subheader("Current Rules")
st.write(knowledge_base.rules) # shows all the rules the AI is using.
