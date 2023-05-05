import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

# Define a list of possible responses to customer queries
responses = {
    "greeting": ["Hello, how may I assist you?", "Welcome, how can I help you today?"],
    "booking": ["You may proceed to UltronAirline.com for booking!"],
    #notyet
    #"support_channel": ["You can contact our support team at support@example.com or by calling 1-800-123-4567."],
    "available-country": ["\nOur flights only operate within Southeast Asian countries.\nWhich only included:\n1. Brunei\n2. Cambodia\n3. Indonesia\n4. Laos\n5. Malaysia\n6. Myanmar\n7. Philippines\n8. Singapore\n9. Thailand\n10. Timor-Leste\n11. Vietnam"],
    "country_name": ["Yes, we have flight that are reaching {country_name}"],
    "not_understand": ["Sorry, currently, we are only supporting Asean Country!!!", "I'm sorry, I didn't understand your query. Please try again."],
    #"packages": ["2 Way Tickets", "1 Way Tickets"],
    "user_Intro": ["Hello {name}"],
    "my_name": ["Your name is {name}"]
}

# Create a lemmatizer object
lemmatizer = WordNetLemmatizer()
name = ""
asean_countries = {'Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 'Vietnam'}

# Define a function to lemmatize a given sentence
def lemmatize_sentence(sentence):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
    # Lemmatize each word
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    # Join the lemmatized words back into a sentence
    lemmatized_sentence = " ".join(lemmatized_words)
    return lemmatized_sentence

import nltk

# Define a function to extract names and country names from a sentence(Chunking)
def extract_names_and_countries(query):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(query)
    # Tag the words with their part of speech
    tagged_words = nltk.pos_tag(words)
    # Extract the named entities from the tagged words
    named_entities = nltk.ne_chunk(tagged_words)
    # Filter out non-person named entities
    person_entities = [entity for entity in named_entities if isinstance(entity, nltk.tree.Tree) and entity.label() == "PERSON"]
    # Extract the person names from the person named entities
    person_names = [ " ".join([word[0] for word in entity.leaves()]) for entity in person_entities]
    # Filter out non-country named entities
    country_entities = [entity for entity in named_entities if isinstance(entity, nltk.tree.Tree) and entity.label() == "GPE"]
    # Extract the country names from the country named entities
    country_names = [ " ".join([word[0] for word in entity.leaves()]) for entity in country_entities]
    return person_names, country_names

#Synonyms
def booking_synonym(query):
    synonyms = []
    words = ["book", "buy"]
    for word in words:
        for syn in wordnet.synsets(word, pos='v'):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
    return synonyms


# Define a function to handle customer queries and generate responses
def chatbot_response(query):
    global name  # Declare global variable to modify name inside the function
    query_lemmas = lemmatize_sentence(query.lower())
    # Extract person names and country names from the query
    names, country_names = extract_names_and_countries(query)
    if "hello" in query_lemmas or "hi" in query_lemmas and ("my" in query_lemmas and "name" in query_lemmas):
        # Check if the query includes the user's name
        if names:
            name = names[0]
            return responses["user_Intro"][0].format(name=name)
        else:
            return random.choice(responses["greeting"])
    elif "what" in query_lemmas and "is" in query_lemmas and "my" in query_lemmas and "name" in query_lemmas:
        if name:
            return responses["my_name"][0].format(name=name)
        else:
            return "I'm sorry, I didn't catch your name. Can you please tell me your name?"
    elif any(lemma in query_lemmas for lemma in booking_synonym(query)):
        return responses["booking"][0]
    elif "where" in query_lemmas or ("which" in query_lemmas and "country"in query_lemmas):
        return responses["available-country"][0]
    elif country_names:
        country_name = country_names[0]
        if country_name not in asean_countries:
            return responses["not_understand"][0].format(country_name=country_name) 
        else:
            for country in asean_countries:
                if country == country_name:
                    return responses["country_name"][0].format(country_name=country_name)
    else:
        return responses["not_understand"][1]

# Define a function to handle user interaction
'''def chatbot():
    print("Welcome to Ultron Airline customer service chatbot!")
    while True:
        query = input("You: ")
        #print(booking_synonym(query))
        if query.lower() == "exit":
            break
        response = chatbot_response(query)
        print("Chatbot: " + response)
        print(booking_synonym(query))
        #print(person_names)

# Run the chatbot function
chatbot()
'''