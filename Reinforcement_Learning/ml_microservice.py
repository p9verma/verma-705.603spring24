import numpy as np
import random

age_labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70']
tenure_labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '31-45']

def reinforcement_solution(epsilon, alpha, gamma):
    number_of_actions = 3  # Number of subject lines
    q_table = np.zeros((192, 3)) # Initialize q_table

    for _ in range(1000):
        # Pick random user and get data
        index = random.randint(0, len(userbase) - 1) 
        
        age_group = userbase.iloc[index]['Age_Group']
        tenure_group = userbase.iloc[index]['Tenure_Group']
        gender_code = userbase.iloc[index]['Gender_code']
        type_code = userbase.iloc[index]['Type_code']

        # Get specific state's index in table
        state = (tenure_labels.index(tenure_group) * 24 + age_labels.index(age_group) * 4 + gender_code * 2 + type_code)
        # explore v exploit 
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 2)  #Explore
        else:
            action = np.argmax(q_table[state])  #Exploit
            
        # Determine reward
        if sent_emails.iloc[index]['SubjectLine_ID'] in responded['Responded_Date'].values:
            reward = 10
        else:
            reward = -10
            
        # Update q-table
        q_table[state, action] += alpha * (reward - q_table[state, action])
    return q_table