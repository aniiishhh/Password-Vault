import random
import string

class PassGenerator:

    def __init__ (self):
        self.__pass_list = list()
        self.__basic_password = ""
        self.__final_password = ""
        self.__chosen_keyword_part = ""
        self.__chosen_keynumber = ""
        self.__length_tuple = ()
    
    def keyword_selection (self, pass_keywords, pass_keywords_questions_list, pass_minimum_length):
        # ----------------------------------------------------------------------------- # 
        # Choosing a random keyword list
        
        if not pass_keywords and len(pass_keywords_questions_list)>0:        
            chosen_keyword_list = pass_keywords_questions_list
        elif not pass_keywords_questions_list and len(pass_keywords)>0:
            chosen_keyword_list = pass_keywords
        elif not pass_keywords_questions_list and not pass_keywords:
            chosen_keyword_list = []
        elif len(pass_keywords_questions_list) > 0 and len(pass_keywords)>0:
            list_id = random.randint(1,2)
            if list_id == 1:
                chosen_keyword_list = pass_keywords
            elif list_id == 2:
                chosen_keyword_list = pass_keywords_questions_list

        # ----------------------------------------------------------------------------- #
        # Choosing 1 random keyword from the keyword list and appending it to a list     

        if pass_minimum_length < 16:
            
            if len(chosen_keyword_list)>0:
                chosen_keyword = random.choice(chosen_keyword_list)

                if len(chosen_keyword) > 5:
                    self.__chosen_keyword_part = random.choice([chosen_keyword[: random.randint(5,6)], chosen_keyword[-random.randint(5,6):]])
                else:
                    self.__chosen_keyword_part = chosen_keyword

                self.__pass_list.append(self.__chosen_keyword_part.lower())

        # ----------------------------------------------------------------------------- #
        # Choosing 2 random keywords from the keyword list and appending it to a list    
            
        elif pass_minimum_length >= 16:

            if len(chosen_keyword_list)>0:      
                chosen_keywords = random.sample(chosen_keyword_list,2)

                for keyword in chosen_keywords:
                    if len(keyword) > 5:
                        self.__chosen_keyword_part = random.choice([keyword[: random.randint(5,6)], keyword[-random.randint(5,6):]])
                    else:
                        self.__chosen_keyword_part = keyword

                    self.__pass_list.append(self.__chosen_keyword_part.lower())
        
        # ----------------------------------------------------------------------------- #
        # Storing the String form of the list in a temporary String variable for calculating length later           
            
        self.__chosen_keyword_part = ''.join(self.__pass_list)

        # -------------------------------------------------------------------------------------------------- #

    def keynumber_selection(self, pass_keynumbers):
        # ----------------------------------------------------------------------------- # 
        # Choosing a random key number and appending it to a list

        if len(pass_keynumbers)>0:
            self.__chosen_keynumber = random.choice(pass_keynumbers)
            self.__chosen_keynumber = str(self.__chosen_keynumber)
            self.__pass_list.append(self.__chosen_keynumber)
        else:
            self.__chosen_keynumber = ""
 
        # -------------------------------------------------------------------------------------------------- #

    def minimum_characters_remaining(self, pass_minimum_length):
        # -------------------------------------------------------------------------------------------------- #
        # Calculating minimum characters to include after counting the keyword and key number lengths

        initial_length = len(self.__chosen_keyword_part) + len(self.__chosen_keynumber)
        initial_difference = pass_minimum_length - initial_length
        
        self.__length_tuple = (initial_length, initial_difference)

        # -------------------------------------------------------------------------------------------------- #

    def choose_remaining_random_char(self, pass_minimum_length, pass_special_char):
        # -------------------------------------------------------------------------------------------------- #
        # Defining a string of various characters, choosing random number of random characters to satisfy 
        # minimum length, and appending chosen random character to a list

        pass_special_char_string = ''.join(pass_special_char)
        characters = string.ascii_letters.lower() + string.digits + pass_special_char_string

        # ----------------------------------------------------------------------------- #

        initial_length, initial_difference = self.__length_tuple
        
        # ----------------------------------------------------------------------------- #
        # Choosing required number of random charcaters

        if pass_minimum_length < 16:
            initial_max_chars = 16
            max_chars = initial_max_chars - initial_length
        
            num_chars = random.randint(initial_difference, max_chars)

            for j in range(num_chars):
                random_char = random.choice(characters)
                self.__pass_list.append(random_char)

        # ----------------------------------------------------------------------------- #  
        # Choosing required number of random charcaters      

        elif pass_minimum_length >= 16:
            initial_max_chars = 24
            max_chars = initial_max_chars - initial_length
        
            num_chars = random.randint(initial_difference, max_chars)

            for j in range(num_chars):
                random_char = random.choice(characters)
                self.__pass_list.append(random_char)
 
        # -------------------------------------------------------------------------------------------------- #

    def shuffle(self):
        # -------------------------------------------------------------------------------------------------- #
        # Shuffling the list containing keyword, key number and random characters

        random.shuffle(self.__pass_list)
        self.__basic_password = ''.join(self.__pass_list)

        # -------------------------------------------------------------------------------------------------- #
    
    def random_caps_pass(self):
        # -------------------------------------------------------------------------------------------------- #

        def random_capitalize(password):
    
            pass_random_caps = ""
            for char in password:
                if char.isalpha():
                    if random.choice([True, False]):
                        pass_random_caps += char.upper()
                    else:
                        pass_random_caps += char.lower()
                else:
                    pass_random_caps += char
            return pass_random_caps
        
        self.__final_password = random_capitalize(self.__basic_password)

        # -------------------------------------------------------------------------------------------------- #

    def __str__ (self):
        # -------------------------------------------------------------------------------------------------- #
        # Printing password and repeating above steps for specified range

        return self.__final_password
    
# -------------------------------------------------------------------------------------------------------------------------------- #
