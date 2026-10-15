

# Quiz Maker with AI Query Integration

**Quiz Maker with AI Query Integration** is a desktop application developed in Python designed to generate and run educational quizzes through an intuitive graphical interface. The platform provides an interactive learning environment where users can test their knowledge using predefined questions or quizzes generated with AI.

The application offers two primary play modes: users can select questions from predefined topic categories or dynamically generate new quizzes on any subject using an external AI API (DeepSeek). The integration features structured prompt formatting to return multiple-choice questions with answer choices and automated fallback handling. Additionally, the system manages game logic, tracks response times, and evaluates performance in real time. All quiz data is persisted locally in JSON format, while user scores and rankings are maintained in a leaderboard text file for performance tracking and comparison.

---

## User Interface (Tkinter GUI)

The graphical user interface is built using Python's `tkinter` library, designed to provide a smooth, intuitive, and responsive experience throughout the quiz workflow. It controls the interaction between the user and the system, guiding the player through menu selection, question answering, and performance review.

### 1. Main Menu & Mode Selection
The home screen allows users to enter their player name, choose between predefined topics, or initiate an AI-generated quiz session on a custom subject.

<p align="center">
  <img width="70%" alt="Main Menu" src="https://github.com/user-attachments/assets/b7f4cab1-c5a4-432e-8a31-27349077e775" />
</p>

### 2. Category Selection & AI Generation
Players can either choose from existing built-in categories or open the prompt dialog to generate questions on custom topics via AI:

| Existing Categories | AI Topic Prompt |
| :---: | :---: |
| <img width="100%" src="https://github.com/user-attachments/assets/1692716c-2815-4890-8671-cd00de8a54a7" /> | <img width="100%"  src="https://github.com/user-attachments/assets/6c8130a3-84a1-4294-af16-9d257e5c96d7" /> |

### 3. Quiz Gameplay & Question View
During the quiz session, the interface presents multiple-choice questions, tracks the response time per question, provides immediate visual feedback, and updates score progress dynamically.

<p align="center">
  <img width="70%" alt="Gameplay Screen" src="https://github.com/user-attachments/assets/a23d5aa7-74b1-4484-821d-495949551f84" />
</p>

### 4. Final Results & Score Summary
Upon answering all questions, the application displays a comprehensive result screen featuring personalized feedback, total score, accuracy percentage, and category details, automatically updating the persistent leaderboard.

<p align="center">
  <img width="70%" alt="Final Results" src="https://github.com/user-attachments/assets/943c9739-1bed-4d95-bb9c-e0058eda4d92" />
</p>

---
