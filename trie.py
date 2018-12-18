# ref https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python
import sys
import string 

# declare global variables
prefix_dict = {}

# end tag
_end = '_end_'

def make_trie(root, prefix, company_name, price):
    current_dict = root

    for digit in prefix:
        # set another dict if the key is not exist already
        current_dict = current_dict.setdefault(digit, {})

    if _end in current_dict:
        # reach the end of trie

        # get current price for current prefix
        current_dict_price = current_dict[_end][1]

        # replace the current price with a cheaper price
        if current_dict_price > price:
            current_dict[_end] = [[company_name], price]

        # if the price is the same as other companies
        elif current_dict_price == price:
            # if company name not in list
            company_name_list = current_dict[_end][0]

            if company_name not in company_name_list:
                # add the company name in list
                company_name_list.append(company_name)
            else:
                current_dict[_end] = [company_name_list, price]
            
    else:
        current_dict[_end] = [[company_name], price]
    
    return root

def in_trie(trie, phone_number):
    current_dict = trie
    current_prefix = ""

    longest_prefix_dict = {}

    for digit in phone_number:

        if digit in current_dict:
            # update current_prefix
            current_prefix += str(digit)

            # move to next node
            current_dict = current_dict[digit]

            if _end in current_dict:
                company_name = current_dict[_end][0]
                price = current_dict[_end][1]
                
                for name in company_name:
                    longest_prefix_dict[name] = [price,current_prefix]
        else:
            if _end in current_dict:
                company_name = current_dict[_end][0]
                price = current_dict[_end][1]
           
                for name in company_name:
                    longest_prefix_dict[name] = [price,current_prefix]

                result = min(longest_prefix_dict.items(), key=lambda x: x[1])
                company_list = [i[0] for i in longest_prefix_dict.items() if i[1][0]==result[1][0]] 

                company_name = company_list
                price = result[1][0]
                prefix = result[1][1]

                return [True, company_name, price, prefix]
            else:

                return [False]
                
    else:
        if _end in current_dict:
            company_name = current_dict[_end][0]
            price = current_dict[_end][1]
           
            for name in company_name:
                longest_prefix_dict[name] = [price,current_prefix]

            result = min(longest_prefix_dict.items(), key=lambda x: x[1])
            company_list = [i[0] for i in longest_prefix_dict.items() if i[1][0]==result[1][0]] 

            company_name = company_list
            price = result[1][0]
            prefix = result[1][1]

            return [True, company_name, price, prefix]
        else:

            return [False]

def INSERT(company_name, prefix, price):
    make_trie(prefix_dict, prefix, company_name, price)

def QUERY(phone_number):
    result_list = in_trie(prefix_dict, phone_number)

    if result_list[0]:
        company_name = result_list[1]
        price = str(result_list[2])
        prefix = str(result_list[3])

        return True, phone_number, company_name , prefix ,price
    
    else:

        return False, phone_number, "NA"

if __name__ == "__main__":
    while True:

        user_command = input()
        user_input = user_command.split()

        # empty string
        if len(user_input) == 0:
            continue
        
        if user_input[0] == "INSERT":
            try:
                company_name = str(user_input[1])

                prefix = user_input[2]
                if prefix.isdigit() is False:
                    raise ValueError('Prefix contains non-numeric value')

                price =  float(user_input[3])
            except Exception as e:
                print("Invalid input: {0}. Try Again.".format(e))
                continue

            INSERT(company_name, prefix, price)

        elif user_input[0] == "QUERY":
            try:
                phone_number = user_input[1]

                # strip all '+' and '-' in phone number
                phone_number = phone_number.translate(str.maketrans("", "","+- "))

                if phone_number.isdigit() is False:
                    raise ValueError('Phone number contains non-numeric value')
            except Exception as e:
                print("Invalid input: {0}. Try Again.".format(e) )
                continue
            
            query_result = QUERY(phone_number)
            
            if query_result[0]:
                print (query_result[1] + " " + ",".join(query_result[2]) + " " + query_result[3] + " " + query_result[4])
            else:
                print (query_result[1] + " " + query_result[2])
        else:
            print("Invalid input. Try Again.")