# accepting states
def accepting_the_list(number_of_states):
  accept_list = input("What are the acception state numbers(index 0 to n-1)(Seperate them by commas): ").split(',')
  for num in range(0, len(accept_list)):
    if(int(accept_list[num]) >= number_of_states or int(accept_list[num]) < 0):
      print(num + " is out of range. Please enter the numbers again." )
      accept_list = accepting_the_list(number_of_states)
    else:
      accept_list[num] = int(accept_list[num])
  return accept_list
# dict = {q1 : [(a1, t1, r1, w1), (a2, t2, r2, w2)], 'q2' : [(a3, a3, r3, w3), (a4, t4, r4, w4)]}
def add_to_dict(q, a, t, r, w, transform_dict):
  if(transform_dict.get(q) is None):
      transform_dict[q] = []
  else:
      # test a
      if(transform_dict[q][0][1] == 'eps' and transform_dict[q][0][0] == 'eps'):
          print("Violation of DPDA due to epsilon input/epsilon stack transition from state (1)")
          return
      elif(a == '-' and t == '-'):
          if(transform_dict.get(q) is not None):
              print("Violation of DPDA due to epsilon input/epsilon stack transition from state (1)")
              return
      # test b
      elif(a == '-' and t != '-'):
          for tup in transform_dict[q]:
              if(tup[1] == t):
                  print("Violation of DPDA due to epsilon input/epsilon stack transition from state (2)")
                  return
      # test c
      elif(a != '-' and t == '-'):
          for tup in transform_dict[q]:
              if(tup[0] == a):
                  print("Violation of DPDA due to epsilon input/epsilon stack transition from state (3)")
                  return
      # test d
      else:
          for tup in transform_dict[q]:
              if(tup[0] == a and tup[1] == t):
                  print("Violation of DPDA due to epsilon input/epsilon stack transition from state (4)")
                  return
  a = 'eps' if a == '-' else a
  t = 'eps' if t == '-' else t
  w = 'eps' if w == '-' else w
  transform_dict[q].append((a, t, w, r))
# transform_dict[q].append((a, t, w, r))
def print_transition(read, pop, push):
  tempPush = ''
  if isinstance(push, list):
    for item in push:
      tempPush += str(item)
  else:
    tempPush = push
  print('[' + read + ',' + pop + '->' + tempPush + ']')
# runs through the transform_dict rescursively and changes state based on input
def acc_or_dec(transform_dict, input_str, initial_str, accepted, curr_state, final, stack, running_trans=''):
  # print("curr_state" + str(curr_state))
  # print(running_trans, end='\n')
  if(not running_trans): #just starting sequence
    running_trans += ("(q" + str(curr_state) + ";" + input_str + ';eps)')
  if (transform_dict.get(curr_state) is not None):
    arr_of_tup = transform_dict.get(curr_state)
  else:
    print ("There are no transitions for state " + str(curr_state) + ".")
    return [initial_str, running_trans, False]
  
  if(not input_str): #no more input, base case
    for num in range(0, len(arr_of_tup)):
      if arr_of_tup[num][0] == 'eps':
        if(stack and stack[-1] == arr_of_tup[num][1]):
          stack.pop()
        elif(stack):
          continue
        curr_state = arr_of_tup[num][3]
        tempStack = ''
        if stack:
          for item in stack:
            tempStack += str(item)
        running_trans += ("--[" + str(arr_of_tup[num][0]) + ',' + arr_of_tup[num][1] + "->" + str(arr_of_tup[num][2]) + "]-->(q" + str(curr_state) + ";eps;" + ('eps' if not tempStack else tempStack)+ ")")
        break
    for state in accepted:
          if(state == curr_state):
            final = True
    if(stack):
      print("Stack is still filled: " + str(stack) + " so string is not accepted")
      return [initial_str, running_trans, False]
    elif(not final):
      print("String ended in state " + str(curr_state) + " which is not an accepting state.")
      return [initial_str, running_trans, False]
    else:
      return [initial_str, running_trans, True]
  curr_char = input_str[0]
  seen_after_seen = False
  for tup in arr_of_tup:
    if(tup[0] == curr_char):
      seen_after_seen = True
      if(tup[1] != 'eps' and tup[1] == stack[-1]):
        stack.pop()
      elif(tup[1] != 'eps' and tup[1] != stack[-1]):
        continue
      if(tup[2] != 'eps'):
        if(isinstance(tup[2], list)):
          for char in tup[2]:
            stack.append(char)
        else:
          stack.append(tup[2])
      curr_state = tup[3]
      tempStack = ''
      for num in range(1, len(stack) + 1):
        tempStack += str(stack[len(stack) - num])
      running_trans += ("--[" + str(tup[0]) + ',' + tup[1] + "->" + str(tup[2]) + "]-->(q" + str(curr_state) + ";" + ('eps' if not input_str[1:] else input_str[1:]) + ";" + tempStack + ")")
      return acc_or_dec(transform_dict, input_str[1:], initial_str, accepted, curr_state, final, stack, running_trans)
    elif(tup[0] == 'eps'):
      if(tup[1] != 'eps'):
        stack.pop()
      if(tup[2] != 'eps'):
        if(isinstance(tup[2], list)):
          for char in tup[2]:
            stack.append(char)
        else:
          stack.append(tup[2])
      curr_state = tup[3]
      tempStack = ''
      for num in range(1, len(stack) + 1):
        tempStack += str(stack[len(stack) - num])
      running_trans += ("--[" + str(tup[0]) + ',' + tup[1] + "->" + str(tup[2]) + "]-->(q" + str(curr_state) + ";" + ('eps' if not input_str else input_str)+ ";" + ('eps' if not tempStack else tempStack) + ")")
      return acc_or_dec(transform_dict, input_str, initial_str, accepted, curr_state, final, stack, running_trans)
    elif(seen_after_seen):
      break

  print("Error, no transition for " + curr_char + " where you pop " + str(stack[-1]) + ". Restart DPDA.")
  return [initial_str, running_trans, False]
# return an array arr = [str, transition str, acc or fail]
def main():
  transitions_dict = {}
  # number of states
  number_of_states = int(input("How many states for your DPDA(n): "))
  # alphabet list
  alphabet_lst = input("What is the input alphabet (Seperate them by commas): ").split(',')
  accepting_list = accepting_the_list(number_of_states)

  # getting transitions
  for stateNum in range(number_of_states):
    while (True):
        print ("\nTransiitions on state " + str(stateNum) + ":")
        if(transitions_dict.get(stateNum) is not None):
            for tup in transitions_dict[stateNum]:
                print_transition(tup[0], tup[1], tup[2])
        yes_or_no = input("Do you want to add a transition rule for state " + str(stateNum) + "?**Enter Transitions grouped together by input char**(y for yes, anything else for no): ")
        if(yes_or_no != 'y'):
            break
        else:
            input_symbol = input("Input Symbol to Read(enter - for epsilon): ")
            stack_pop = input("Stack symbols to match and pop(enter - for epsilon): ")
            to_state = int(input("State to transition to: "))
            stack_push = input("Stack symbols to push as comma separated list, first symbol to top of stack (enter - for epsilon): ")
            for char in stack_push:
              if(char == ','):
                stack_push = stack_push.split(',')
                break
            add_to_dict(stateNum, input_symbol, stack_pop, to_state, stack_push, transitions_dict)
            #              q           a             t       r            w    
            #   delta(q, a, t) = (r, w)
            #   (current state, symbol read, pop) = (next state, push)
  print("\nPrinting all transitions...")
  for stateNum in range(number_of_states):
      print ("Transiitions on state " + str(stateNum) + ":")
      if(transitions_dict.get(stateNum) is not None):
          for tup in transitions_dict[stateNum]:
              print_transition(tup[0], tup[1], tup[2])

  # verifying input string
  while True:
    test_str = input("\nTest string for DPDA (hit enter to exit): ")
    print()
    if (test_str == ''):
      break
    flag = False
    for char in test_str:
      if char not in alphabet_lst:
        print(char + " is not in the given alphabet.")
        flag = True
    if(flag):
      continue
    result = acc_or_dec(transitions_dict, test_str, test_str, accepting_list, 0, False, [])
    print("The string " + test_str + (" is " if result[2] else " is not ") + "accepted.")
    print(result[1])
  print("Thank you!")
if __name__ == '__main__':
  main()