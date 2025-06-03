# CISC 440 Final Project: AI-Powered Sustainability Project

**Authors:** Spencer Kubat, Uyen Thy Duong 

## Project Summary:

Our project explored sustainability through interactive games and predictive models using AI and machine learning. This repository encompasses three key deliverables: game development, supervised machine learning, and an evaluation of generative AI for GUI creation.

-----

## Deliverable 1: Game Development

This deliverable focuses on developing two AI-powered games with a sustainability theme. 

### Wheel of Fortune – Sustainability Edition

This game is a sustainability-themed adaptation of the classic Wheel of Fortune. Players take turns spinning a wheel and guessing letters to solve a hidden environmental phrase, blending entertainment with an educational focus on environmental awareness.

The game offers different versions for interaction:

  * A **console-based game** (`WheelOfFortune.py`) that handles the core game logic via text-based input/output.
  * A **graphical user interface (GUI) version** built by the team using Godot, which is distributed as an executable.

#### Key Features:

  * **Three Play Modes:** Engage in battles of wit with **Player vs Player**, challenge an intelligent **Player vs AI**, or test your luck against a **Player vs Random** AI[cite: 10].
  * **Dynamic Difficulty:** Gameplay difficulty affects the AI strategy and phrase complexity.
  * **Intelligent AI Guesses:** The AI uses several techniques:
      * **Constraint Satisfaction (CSP)** to filter valid phrases based on guessed letters.
      * **Uniform Cost Search (UCS)** to prioritize frequent, low-cost letters, optimizing player budget.
      * **Greedy Search** to select high impact guesses from likely phrases.
      * **SmartCoinFlip** is a heuristic used by the AI to dynamically shift its strategy based on difficulty.
  * **Special Wedges:** Navigate the wheel with special wedges like `JACKPOT`, `BANKRUPT`, `1/2 CAR`, and `LOSE A TURN` to add strategic depth.
  * **Vowel Purchases:** Players can buy vowels for a cost of $250.
  * **Sustainability Phrase Bank:** All game phrases are drawn from `sustainability_words.txt`, located at `./Prob_1/WheelOfSustainability/sustainability_words.txt` relative to the game's execution, reinforcing the educational theme.

#### Technologies Used:

  * **Console-Based Game Logic:** Python
  * **GUI Executable:** Godot Engine and GDScript

#### Installation & Setup:

There are two distinct ways to run the game:

##### Option 1: Using the GUI Executable (Recommended for Full Game Experience)

This option provides the complete game with a graphical user interface.

1.  **Download the Game Files:** Download the entire `CISC440_Final_Project` repository. It is crucial that the `Wheel Of Sustainability.exe` file, `WheelOfFortune.py`, `GeneratedPyQtWoF.py`, and the `Prob_1/WheelOfSustainability` directory (which contains `sustainability_words.txt`) are all kept in their relative positions as found in the repository. The executable relies on these accompanying files and the correct directory structure.
2.  **Run the Executable:** Simply double-click the `Wheel Of Sustainability.exe` file located in the main project directory to launch the game with its graphical interface.

##### Option 2: Running the Console-Based Game from Source (No GUI)

This option allows you to run the core game logic directly from the Python script, interacting via the command line/console.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourGitHubUsername/CISC440_Final_Project.git
    cd CISC440_Final_Project
    ```
2.  **Install Python:** Ensure you have Python (preferably Python 3.x) installed on your system.
3.  **Run the Console Game:** From the root of the `CISC440_Final_Project` directory, execute the `WheelOfFortune.py` script. The script expects `sustainability_words.txt` to be at `./Prob_1/WheelOfSustainability/sustainability_words.txt` relative to its execution.
    ```bash
    python WheelOfFortune.py
    ```

#### Usage:

  * **For the GUI Executable:** Launch the `Wheel Of Sustainability.exe` file. The game will open in a new window, and you can interact with it using the graphical interface. Follow the on-screen instructions to select game modes and play.
  * **For the Console-Based Game:** Launch the `WheelOfFortune.py` script from your terminal/command prompt. All interactions (inputs, outputs) will occur directly within the console window. Follow the text-based prompts to select game modes and play.
      * **Difficulty Levels:** When playing against an AI, you can choose from Easy, Medium, or Hard difficulty. These correspond to internal difficulty values of 1, 5, and 8 respectively, influencing AI decision-making.

-----

## Deliverable 2: Supervised Machine Learning

This deliverable explores various machine learning models for sustainability-related predictions and analysis.

### Logistic Regression Model (Heat Wave Frequency Prediction)

This model predicts whether a U.S. state will experience more than one heat wave in a given month using logistic regression trained via Stochastic Gradient Descent (SGD).

#### Dataset Details:

  * **Source:** [Data Commons](https://datacommons.org/tools/download).
  * **Contents:** Monthly records from U.S. states.
  * **Features:**
      * `Electricity Consumers in a Month` 
      * `Average Retail Price of Electricity (All Sectors, Monthly)` 
      * `Net Generation (All Fuels, Electric Power Total, Monthly)` 
      * `Net Generation (All Fuels, Electric Utility, Monthly)` 
  * **Target:** `Heat_High` (Binary label) 
      * `1` = More than 1 heat wave occurred in the month 
      * `0` = 0 or 1 heat wave occurred 

#### Model Details:

  * **Model Type:** Logistic Regression classifier 
  * **Task:** Binary classification to predict `Heat_High`.
  * **Important Note on Target Variable:** The dataset only includes months with at least one heat wave; months with zero events are not recorded. Therefore, the model's task focuses on predicting *frequency severity* (among recorded heat wave months, predict if more than 1 event occurred) rather than full event presence/absence. This avoids introducing false negatives and aligns with the dataset's structure.

#### Performance & Insights:

  * **Accuracy:** The model achieved 77% accuracy.
  * **Performance on High Heat Wave Months:** Strong performance with a precision of 0.83, recall of 0.91, and F1-score of 0.87 for months with more than one heat wave.
  * **Class Imbalance:** Performed poorly on low/no event months due to class imbalance.
  * **Feature Correlation:** Utility-based electricity generation showed a strong positive correlation with frequent heat waves, while higher electricity consumer counts were negatively associated. These insights suggest that centralized energy generation patterns may contribute to climate vulnerability.

#### Technologies Used:

  * **Python**
  * **Jupyter Notebook** (likely uses `pandas`, `numpy`, `scikit-learn` for data handling and modeling)

#### Installation & Setup:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YourGitHubUsername/CISC440_Final_Project.git
    cd CISC440_Final_Project
    ```
2.  **Install Python:** Ensure you have Python (preferably Python 3.x) installed on your system.
3.  **Install Jupyter Notebook and Dependencies:**
    ```bash
    pip install jupyter pandas numpy scikit-learn matplotlib seaborn # Install common data science libraries
    ```
4.  **Launch Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```
5.  Your web browser will open with the Jupyter Notebook interface. Navigate to the relevant directory (`/Machine_Learning`) and open the `.ipynb` file (`USA_State_Heat_Logistic_Regression.ipynb`).

#### Usage:

1.  Once the Jupyter Notebook is open, you can run the cells sequentially to re-execute the data loading, preprocessing, model training, and evaluation steps.
2.  Explore the code and markdown cells to understand the dataset, model methodology, and analysis results.

-----

## Deliverable 3: Generative AI Evaluation

This deliverable involved testing the capabilities of generative AI models (ChatGPT and Claude) for GUI generation, specifically for the Wheel of Fortune and Golf Card Game.

### Wheel of Sustainability GUI Generation

This section details the attempt to generate a PyQt-based GUI for the Wheel of Fortune game using ChatGPT-40.

#### Process & Results:

1.  **Initial Prompt:** ChatGPT-40 was provided with the existing Python game code and prompted to create a PyQt GUI (`“Here is my python code in a txt file. Please make a GUI for this using PyQt.”`).
2.  **Iterative Prompting:** Subsequent prompts were needed to integrate game logic and enable input after a spin (`“Can you integrate my python game logic into the gui you gave me”`, `“This gui doesn't allow for input after the spin, can you integrate the logic for input after a spin”`).
3.  **Outcome:** Despite multiple prompts, the generated output was a "very bare framework that did not function properly".
4.  **Conclusion:** Continuing with generative AI for GUI development would have required significant additional work and knowledge of PyQt. It was found to be as much effort as building the Godot version manually.

### Overall Generative AI Conclusion

The evaluation of generative AI for GUI creation provided key insights:

  * Building a custom GUI (e.g., in Godot) offers more control and functionality, especially when familiar with the framework.
  * The PyQt framework generated by AI was unsatisfactory, underscoring the importance of human knowledge and effort in learning frontend frameworks.
  * Generative AI can be helpful for small code snippets but cannot be relied upon for complete project generation.

-----

## Future Enhancements

The project has several potential avenues for future development:

  * **Audio Enhancements:** Add background music and sound effects for button clicks and in-game events.
  * **User Interface Feedback:** Implement pop-ups for better user guidance.
  * **Accessibility:** Integrate a text-to-speech feature for game rules.
  * **Golf AI Improvement:** Train the Golf Card Game AI model using logistic regression to fine-tune heuristic weights for a stronger, more difficult AI.
  * **UX/UI Design:** Improve card and button designs in the GUI.
  * **AI Efficiency:** Optimize AI code to reduce AI deliberation time (currently 10-30 seconds for deep searches).
  * **Multi-Player Support:** Add features to allow more than two players in the Golf Card Game, though screen size considerations would need to be addressed.
  * **Educational Content:** Add more fun facts to the Golf cards that cycle on hover, increasing variety and educational content.

-----

## Demos

Demo videos for the "Wheel of Fortune – Sustainability Edition" game are available in the same directory within this repository. These videos showcase the game's features and different play modes.

