import streamlit as st
import random


# Function to load the word list from the file
@st.cache_data  # Cached to avoid reloading on every rerun
def load_words():
   wordlist = []
   with open("words.txt", 'r') as file:
      wordlist = [line.strip() for line in file if line.strip()]
   return wordlist


wordlist = load_words()


# Function to reset the game and rerun the app
def refresh():
   st.session_state.clear()
   st.experimental_rerun()


# Main function for Wordle game
def play_wordle():
   st.title("Wordle")  # Page title
   # Allow user to choose word length
   length = st.number_input("Enter the word length you want to play with:",
                            min_value=3,
                            max_value=10,
                            value=5,
                            step=1,
                            on_change=st.session_state.clear)
   # Filter word list of selected length
   currentlist = [word for word in wordlist if len(word) == length]
   # Randomly choose secret word from filtered list
   secret = random.choice(currentlist)
   # Set number of allowed attempts
   attempts = 6

   # Initialize session state variables
   if 'guesses' not in st.session_state:
      st.session_state['guesses'] = 0
      st.session_state['words'] = []
      st.session_state['results'] = []
      st.session_state['game_over'] = False
      st.session_state['secret'] = secret

   # Update secret word from session state
   secret = st.session_state['secret']

   # Game instructions
   st.write(f"Let's play {length}-letter Wordle! You have {attempts} attempts.")

   # Big and small hint buttons
   bighint, smallhint = st.columns(2)
   with bighint:
      if st.button("Big Hint"):
         location = random.randint(0, len(secret) - 1)
         st.write(f"The letter {secret[location]} is in position {location+1} of the word.")
   with smallhint:
      if st.button("Small Hint"):
         st.write(f"The letter {secret[random.randint(0, len(secret)-1)]} is in the word.")
   # Ask the user to input a guess
   guess = st.text_input("Enter your guess:", key="guess_input").lower()

   # Check if the game is still ongoing
   if st.session_state[
       'guesses'] < attempts and not st.session_state['game_over']:
      if st.button("Submit"):
         # Check guess length
         if len(guess) == length:
            # Check if guess is a valid word (in word list)
            if guess in currentlist:
               if guess in st.session_state['words']:
                  st.error("Duplicate guess!")
               else:
                  # Process the guess and update session state
                  st.session_state['guesses'] += 1
                  result = check_guess(guess, secret, length)
                  st.session_state['words'].append(guess)
                  st.session_state['results'].append((result, guess))
                  # Check if the guess is correct
                  if guess == secret:
                     st.success("Congratulations, you've guessed the word!")
                     st.balloons()  # Show balloons to celebrate!
                     st.session_state['game_over'] = True
                  elif st.session_state['guesses'] == 6:
                     st.rerun()
            else:
               st.error("Please enter a valid word")
         else:
            st.error("Please enter a word of correct length.")
   else:
      # Game over
      st.error(f"Game Over! The word was '{secret}'. Restart to play again.")


# Function to compare guess against secret
def check_guess(guess, secret, length):
   output = ["⬜"] * length
   letter_frequencies = {}

   # Check for correct letters in the correct positions (green boxes)
   for i in range(length):
      if secret[i] == guess[i]:
         output[i] = "🟩"
      else:
         if secret[i] in letter_frequencies:
            letter_frequencies[secret[i]] += 1
         else:
            letter_frequencies[secret[i]] = 1

   # Check for correct letters in the wrong positions (yellow boxes)
   for i in range(length):
      if output[i] == "⬜" and guess[
          i] in letter_frequencies and letter_frequencies[guess[i]] > 0:
         output[i] = "🟨"
         letter_frequencies[guess[i]] -= 1

   return "".join(output)


# Main block to run the web application
if __name__ == "__main__":
   if st.button("Restart"):
      refresh()
   play_wordle()
   # Display results of each guess
   if st.session_state['results'] != []:
      col1, col2 = st.columns(2)
      with col1:
         st.header("Guess")
      with col2:
         st.header("Result")
      for result, guess in st.session_state['results']:
         with col1:
            st.write(guess)
         with col2:
            st.write(result)
