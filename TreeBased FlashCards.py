from fuzzywuzzy import fuzz
#Add functions (time complexity=O(1) constant time)___________________________________________________________________________________________________________________________________________________________________________________________
def MakeNode(data): # Function to create a node with given data
    return {"data": data, "children": {}}
    
def AddSubject(root,subject): # Function to add a subject node to the hierarchy
    root["children"][subject] = MakeNode({})  

def AddTopic(root,subject,topic): # Function to add a topic node to the hierarchy under a subject
    if subject not in root["children"]: #check for existance of subject node
        AddSubject(root,subject)
    root["children"][subject]["children"][topic] = MakeNode({})

def AddSubTopic(root,subject,topic,subtopic): # Function to add a subtopic node to the hierarchy under a subject and topic
    if subject not in root["children"]: #check for existance of subject node
        AddSubject(root,subject)
    if topic not in root["children"][subject]["children"]: #check for existance of topic node
        AddTopic(root,subject,topic)
    root["children"][subject]["children"][topic]["children"][subtopic] = MakeNode({})   

def AddFlashcard(root,subject,topic,subtopic,flashcard): # Function to add a flashcard node to the hierarchy under a subject, topic, and subtopic
    if subject not in root["children"]: #check for existance of subject node
        AddSubject(root,subject)
    if topic not in root["children"][subject]["children"]: #check for existance of topic node
        AddTopic(root,subject,topic)
    if subtopic not in root["children"][subject]["children"][topic]["children"]: #check for existance of subtopic node
        AddSubTopic(root,subject,topic,subtopic)
    root["children"][subject]["children"][topic]["children"][subtopic]["children"][flashcard["question"]] = flashcard

#search functions___________________________________________________________________________________________________________________________________________________________________________________________
def list_to_dict(items):
    """Convert a list to a dictionary with serial numbers as keys."""
    return {str(i + 1): item for i, item in enumerate(items)}

def search(root, subject=None, topic=None, subtopic=None, question=None): # Function to search for subjects, topics, subtopics, or questions in the hierarchy
    if not subject: # If no subject is provided, return a dictionary of all subjects with serial numbers
        return list_to_dict(list(root["children"].keys()))
    elif subject and not topic: # If no subject is provided, return a dictionary of all subjects with serial numbers
        if subject in root["children"]:
            return list_to_dict(list(root["children"][subject]["children"].keys()))
        else:
            return {}  
    elif subject and topic and not subtopic: # If subject and topic are provided, return a dictionary of subtopics under that topic with serial numbers
        if subject in root["children"] and topic in root["children"][subject]["children"]:
            return list_to_dict(list(root["children"][subject]["children"][topic]["children"].keys()))
        else:
            return {}  
    elif subject and topic and subtopic and not question: # If subject, topic, and subtopic are provided, return a dictionary of questions under that subtopic with serial numbers
        if subject in root["children"] and topic in root["children"][subject]["children"] and subtopic in root["children"][subject]["children"][topic]["children"]:
            return list_to_dict(list(root["children"][subject]["children"][topic]["children"][subtopic]["children"].keys()))
        else:
            return {} 
    elif subject and topic and subtopic and question: # If all parameters are provided, return the flashcard corresponding to the provided question

        if subject in root["children"] and topic in root["children"][subject]["children"] and subtopic in root["children"][subject]["children"][topic]["children"] and question in root["children"][subject]["children"][topic]["children"][subtopic]["children"]:
            return root["children"][subject]["children"][topic]["children"][subtopic]["children"].get(question)
        else:
            return None
    else:
        return None



#delete function___________________________________________________________________________________________________________________________________________________________________________________________
def delete(root, subject=None, topic=None, subtopic=None, question=None):
    if not subject:
        return None  # If no subject provided, nothing to delete
    
    # If only subject is provided, delete the subject and all its children
    if subject in root["children"]:
        if not topic:
            del root["children"][subject]
            return True  
        
        # If topic is provided, delete the topic and all its children
        if topic in root["children"][subject]["children"]:
            if not subtopic:
                del root["children"][subject]["children"][topic]
                return True  
            
            # If subtopic is provided, delete the subtopic and all its children
            if subtopic in root["children"][subject]["children"][topic]["children"]:
                if not question:
                    del root["children"][subject]["children"][topic]["children"][subtopic]
                    return True  
                
                # If question is provided, delete the flashcard with the specified question
                if question in root["children"][subject]["children"][topic]["children"][subtopic]["children"]:
                    del root["children"][subject]["children"][topic]["children"][subtopic]["children"][question]
                    return True  
    
    return False

#function to print flashcard on terminal___________________________________________________________________________________________________________________________________________________________________________________________
def Flashcard_Printer(question,answer):
    
    max_length = max(len(question), len(answer), 21) 

    lines = [
        '┌' + '─' * (max_length + 2) + '┐',
        '│' + ' ' * ((max_length - len("Flashcard")) // 2) + "Flashcard" + ' ' * ((max_length - len("Flashcard")) // 2 + (max_length - len("Flashcard")) % 2) + '  │',
        '├' + '─' * (max_length + 2) + '┤',
        '│' + ' ' * ((max_length - len("Question:")) // 2) + "Question:" + ' ' * ((max_length - len("Question:")) // 2 + (max_length - len("Question:")) % 2) + '  │',
        '│' + question.center(max_length) + '  │',
        '│' + ' ' * ((max_length - len("Answer:")) // 2) + "Answer:" + ' ' * ((max_length - len("Answer:")) // 2 + (max_length - len("Answer:")) % 2) + '  │',
        '│' + answer.center(max_length) + '  │',
        '└' + '─' * (max_length + 2) + '┘'
    ]

    return '\n'.join(lines)

#function to use add___________________________________________________________________________________________________________________________________________________________________________________________
def addflashcard_operation():
    # Prompt the user to enter a subject until a valid one is provided
    subject = None
    while not subject:
        # Retrieve existing subjects and check for similarity
        subjectlst = list(search(root).values())
        subject = input("Enter subject: ").lower().strip()
        similarity = check_similarity(subjectlst, subject)

        # If a similar subject exists, prompt the user to use it
        if similarity != False:
            while True:
                user_similarity = input('A similar Subject ' + "'" + similarity + "'" + " already exists, would you like to use that instead? (Y/N): ").upper()
                if user_similarity == "Y":
                    subject = similarity
                    break
                elif user_similarity == "N":
                    break
                else:
                    print("Invalid Input")
        if not subject:
            print("Subject cannot be empty.")

    # Prompt the user to enter a topic until a valid one is provided
    topic = None
    while not topic:
        # Retrieve existing topics under the selected subject and check for similarity
        topiclst = list(search(root, subject).values())
        topic = input("Enter topic: ").lower().strip()
        similarity = check_similarity(topiclst, topic)

        # If a similar topic exists, prompt the user to use it
        if similarity != False:
            while True:
                user_similarity = input('A similar Topic ' + "'" + similarity + "'" + " already exists, would you like to use that instead? (Y/N): ").upper()
                if user_similarity == "Y":
                    topic = similarity
                    break
                elif user_similarity == "N":
                    break
                else:
                    print("Invalid Input")
        if not topic:
            print("Topic cannot be empty.")

    # Prompt the user to enter a subtopic until a valid one is provided
    subtopic = None
    while not subtopic:
        # Retrieve existing subtopics under the selected subject and topic and check for similarity
        subtopiclst = list(search(root, subject, topic).values())
        subtopic = input("Enter subtopic: ").lower().strip()
        similarity = check_similarity(subtopiclst, subtopic)

        # If a similar subtopic exists, prompt the user to use it
        if similarity != False:
            while True:
                user_similarity = input('A similar SubTopic ' + "'" + similarity + "'" + " already exists, would you like to use that instead? (Y/N): ").upper()
                if user_similarity == "Y":
                    subtopic = similarity
                    break
                elif user_similarity == "N":
                    break
                else:
                    print("Invalid Input")
        if not subtopic:
            print("SubTopic cannot be empty.")
        
    # Prompt the user to enter a question until a valid one is provided
    question = input("Enter question: ").strip()
    while not question:
        print("Question cannot be empty.")
        question = input("Enter question: ").strip()

    # Prompt the user to enter an answer until a valid one is provided
    answer = input("Enter answer: ").strip()
    while not answer:
        print("Answer cannot be empty.")
        answer = input("Enter answer: ").strip()

    # Create a flashcard dictionary with the provided question and answer
    flashcard = {"question": question, "answer": answer}

    # Add the flashcard to the hierarchy under the selected subject, topic, and subtopic
    AddFlashcard(root, subject, topic, subtopic, flashcard)
    
    # Print a success message
    print("Flashcard added successfully!")


#function to use search___________________________________________________________________________________________________________________________________________________________________________________________
def searchflashcard_operations(root):
    # Retrieve a list of subjects
    subject_list = search(root)
    
    # Check if the tree is empty
    if len(subject_list) == 0:
        print("The tree is empty.")
        return

    # Display available subjects with serial numbers
    print("Available subjects:")
    for serial, subject in subject_list.items():
        print(f"{serial}. {subject}")

    # Prompt the user to select a subject
    subject_index = input("Enter the serial number of the subject: ")
    subject = subject_list.get(subject_index)
    while not subject:
        print("Invalid input. Try again.")
        print("Available subjects:")
        for serial, subject in subject_list.items():
            print(f"{serial}. {subject}")
        subject_index = input("Enter the serial number of the subject: ")
        subject = subject_list.get(subject_index)

    # Retrieve a list of topics under the selected subject
    topic_list = search(root, subject)
    
    # Check if there are topics under the selected subject
    if len(topic_list) == 0:
        print("No topics under this subject.")
        return

    # Display available topics with serial numbers
    print("Available topics:")
    for serial, topic in topic_list.items():
        print(f"{serial}. {topic}")

    # Prompt the user to select a topic
    topic_index = input("Enter the serial number of the topic: ")
    topic = topic_list.get(topic_index)
    while not topic:
        print("Invalid input. Try again.")
        print("Available topics:")
        for serial, topic in topic_list.items():
            print(f"{serial}. {topic}")
        topic_index = input("Enter the serial number of the topic: ")
        topic = topic_list.get(topic_index)

    # Retrieve a list of subtopics under the selected subject and topic
    subtopic_list = search(root, subject, topic)
    
    # Check if there are subtopics under the selected topic
    if len(subtopic_list) == 0:
        print("No subtopics under this topic.")
        return

    # Display available subtopics with serial numbers
    print("Available subtopics:")
    for serial, subtopic in subtopic_list.items():
        print(f"{serial}. {subtopic}")

    # Prompt the user to select a subtopic
    subtopic_index = input("Enter the serial number of the subtopic: ")
    subtopic = subtopic_list.get(subtopic_index)
    while not subtopic:
        print("Invalid input. Try again.")
        print("Available subtopics:")
        for serial, subtopic in subtopic_list.items():
            print(f"{serial}. {subtopic}")
        subtopic_index = input("Enter the serial number of the subtopic: ")
        subtopic = subtopic_list.get(subtopic_index)

    # Retrieve a list of questions under the selected subject, topic, and subtopic
    question_list = search(root, subject, topic, subtopic)
    
    # Check if there are questions under the selected subtopic
    if not question_list:
        print("No flashcards under this subtopic.")
        return

    # Display available questions with serial numbers
    while True:
        print("Available questions:")
        for serial, question in question_list.items():
            print(f"{serial}. {question}")
        
        # Prompt the user to select a question
        question_index = input("Enter the serial number of the question: ")
        question = question_list.get(question_index)
        
        # Validate the input
        if not question:
            print("Invalid input.")
            continue

        # Display the selected flashcard and prompt for further action
        result = search(root, subject, topic, subtopic, question)
        if result:
            print("Flashcard found!")
            print(Flashcard_Printer(result['question'],"Check answer? (Y/N): "))
            
            # Prompt the user to check the answer or proceed
            while True:
                user_input = input().upper()
                if user_input == "Y":
                    print(Flashcard_Printer(result['question'], result['answer']))
                    break
                elif user_input == "N": 
                    break
                else:
                    print("Invalid Input")

            # Prompt the user to leave the topic or continue
            if input("Enter Y to leave this topic. Enter anything else to continue. ").upper() == "Y":
                break



#function to use delete___________________________________________________________________________________________________________________________________________________________________________________________
def deleteflashcard_operation():
    deleteoperation = input("""What would you like to do?
                          1. Delete subject
                          2. Delete topic
                          3. Delete subtopic
                          4. Delete flashcard
                          5. Exit\n""")
    
    if deleteoperation == '1':
        # Deleting subject
        # Retrieve a list of subjects
        subject_list = search(root)
        if len(subject_list) == 0:
        # Check if the tree is empty
            print("The tree is empty.")
            return
        # Display available subjects with serial numbers
        print("Available subjects:")
        for serial, subject in subject_list.items():
            print(f"{serial}. {subject}")
        # Prompt the user to select a subject for deletion
        subject_index = input("Enter the serial number of the subject you want to delete: ")
        subject = subject_list.get(subject_index)
        while not subject:
            print("Invalid input. Try again.")
            subject_index = input("Enter the serial number of the subject you want to delete: ")
            subject = subject_list.get(subject_index)
        # Attempt to delete the subject and all its contents
        if delete(root, subject):
            print("Subject and all its contents deleted successfully!")
        else:
            print("Failed to delete subject.")
            
    elif deleteoperation == '2':
        # Deleting topic
        # Code for deleting a topic follows a similar structure as deleting a subject
        subject_list = search(root)
        if len(subject_list) == 0:
            print("The tree is empty.")
            return

        print("Available subjects:")
        for serial, subject in subject_list.items():
            print(f"{serial}. {subject}")

        subject_index = input("Enter the serial number of the subject: ")
        subject = subject_list.get(subject_index)
        while not subject:
            print("Invalid input. Try again.")
            subject_index = input("Enter the serial number of the subject: ")
            subject = subject_list.get(subject_index)

        topic_list = search(root, subject)
        if len(topic_list) == 0:
            print("No topics under this subject.")
            return

        print("Available topics:")
        for serial, topic in topic_list.items():
            print(f"{serial}. {topic}")

        topic_index = input("Enter the serial number of the topic you want to delete: ")
        topic = topic_list.get(topic_index)
        while not topic:
            print("Invalid input. Try again.")
            topic_index = input("Enter the serial number of the topic you want to delete: ")
            topic = topic_list.get(topic_index)

        if delete(root, subject, topic):
            print("Topic and all its contents deleted successfully!")
            
        else:
            print("Failed to delete topic.")
            
    elif deleteoperation == '3':
        # Deleting subtopic
        # Code for deleting a subtopic follows a similar structure as deleting a subject and topic
        subject_list = search(root)
        if len(subject_list) == 0:
            print("The tree is empty.")
            return

        print("Available subjects:")
        for serial, subject in subject_list.items():
            print(f"{serial}. {subject}")

        subject_index = input("Enter the serial number of the subject: ")
        subject = subject_list.get(subject_index)
        while not subject:
            print("Invalid input. Try again.")
            subject_index = input("Enter the serial number of the subject: ")
            subject = subject_list.get(subject_index)

        topic_list = search(root, subject)
        if len(topic_list) == 0:
            print("No topics under this subject.")
            return

        print("Available topics:")
        for serial, topic in topic_list.items():
            print(f"{serial}. {topic}")

        topic_index = input("Enter the serial number of the topic: ")
        topic = topic_list.get(topic_index)
        while not topic:
            print("Invalid input. Try again.")
            topic_index = input("Enter the serial number of the topic: ")
            topic = topic_list.get(topic_index)

        subtopic_list = search(root, subject, topic)
        if len(subtopic_list) == 0:
            print("No subtopics under this topic.")
            return

        print("Available subtopics:")
        for serial, subtopic in subtopic_list.items():
            print(f"{serial}. {subtopic}")

        subtopic_index = input("Enter the serial number of the subtopic you want to delete: ")
        subtopic = subtopic_list.get(subtopic_index)
        while not subtopic:
            print("Invalid input. Try again.")
            subtopic_index = input("Enter the serial number of the subtopic you want to delete: ")
            subtopic = subtopic_list.get(subtopic_index)

        if delete(root, subject, topic, subtopic):
            print("Subtopic and all its contents deleted successfully!")
            
        else:
            print("Failed to delete subtopic.")
            
    elif deleteoperation == '4':
        # Deleting flashcard 
        # Code for deleting a flashcard follows a similar structure as deleting a subject, topic, and subtopic
        subject_list = search(root)
        if len(subject_list) == 0:
            print("The tree is empty.")
            return

        print("Available subjects:")
        for serial, subject in subject_list.items():
            print(f"{serial}. {subject}")

        subject_index = input("Enter the serial number of the subject: ")
        subject = subject_list.get(subject_index)
        while not subject:
            print("Invalid input. Try again.")
            subject_index = input("Enter the serial number of the subject: ")
            subject = subject_list.get(subject_index)

        topic_list = search(root, subject)
        if len(topic_list) == 0:
            print("No topics under this subject.")
            return

        print("Available topics:")
        for serial, topic in topic_list.items():
            print(f"{serial}. {topic}")

        topic_index = input("Enter the serial number of the topic: ")
        topic = topic_list.get(topic_index)
        while not topic:
            print("Invalid input. Try again.")
            topic_index = input("Enter the serial number of the topic: ")
            topic = topic_list.get(topic_index)

        subtopic_list = search(root, subject, topic)
        if len(subtopic_list) == 0:
            print("No subtopics under this topic.")
            return

        print("Available subtopics:")
        for serial, subtopic in subtopic_list.items():
            print(f"{serial}. {subtopic}")

        subtopic_index = input("Enter the serial number of the subtopic: ")
        subtopic = subtopic_list.get(subtopic_index)
        while not subtopic:
            print("Invalid input. Try again.")
            subtopic_index = input("Enter the serial number of the subtopic: ")
            subtopic = subtopic_list.get(subtopic_index)

        question_list = search(root, subject, topic, subtopic)
        if len(question_list) == 0:
            print("No flashcards under this subtopic.")
            return
        
        print("Available questions:")
        for serial, question in question_list.items():
            print(f"{serial}. {question}")

        question_index = input("Enter the serial number of the question you want to delete: ")
        question = question_list.get(question_index)
        while not question:
            print("Invalid input. Try again.")
            question_index = input("Enter the serial number of the question you want to delete: ")
            question = question_list.get(question_index)

        if delete(root, subject, topic, subtopic, question):
            print("Flashcard deleted successfully!")
            
        else:
            print("Failed to delete flashcard.")
    
    elif deleteoperation == '5':
        print("Exiting operation")
    else:
        print("Invalid operation try again")


#function to check for similar inputs___________________________________________________________________________________________________________________________________________________________________________________________
def check_similarity(existing_names, new_name):
    # Iterate through existing names
    for name in existing_names:
        # If there's an exact match, return False (not similar)
        if name == new_name:
            return False
        # Check similarity using fuzzy string matching (threshold set to 65)
        similarity_ratio = fuzz.partial_ratio(name.lower(), new_name.lower())
        # If similarity ratio meets threshold, return the existing name
        if similarity_ratio >= 65: 
            return name
    # If no similarity found, return False
    return False


#main function to use all the function___________________________________________________________________________________________________________________________________________________________________________________________
root = MakeNode({})  # Creating the root node of the hierarchy

def main():
    answers = []  # List to store answers
    questions = []  # List to store questions

    while True:
        # Displaying menu options to the user
        operation = input("""Hello, what would you like to do?
                            1. Add flashcard
                            2. Search flashcard
                            3. Delete flashcard
                            4. Exit\n""")
        
        # Perform the selected operation based on user input
        if operation == '1':
            addflashcard_operation()  # Call function to add flashcard
        elif operation == '2':
            searchflashcard_operations(root)  # Call function to search flashcards
        elif operation == '3':
            deleteflashcard_operation()  # Call function to delete flashcard
        elif operation == '4':
            print("Exiting program")  # Exiting the program
            break
        else:
            print("Invalid operation try again")  # Prompt for valid input if operation is not recognized

if __name__ == "__main__":
    main()  # Call the main function to start the program



