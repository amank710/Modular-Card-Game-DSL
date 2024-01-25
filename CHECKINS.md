Use this file to commit information clearly documenting your check-ins' content. If you want to store more information/details besides what's required for the check-ins that's fine too. Make sure that your TA has had a chance to sign off on your check-in each week (before the deadline); typically you should discuss your material with them before finalizing it here.

# Check-in 1 Report Items

## Provide a brief description of your planned DSL:

1. What is the high-level purpose of your DSL? What kind of users is it aimed at? What will it enable users to do?
   - Modular 2 person card game, allows a user to program a set of rules for the card game like Go Fish or BlackJack
   - Target users are card game enthusiasts or people who want to try creating multiplayer card games
   - Enables users to create 2 person custom card games with customized rules. Our vision for this project is to provide our users a virtual representation of a deck of cards and basic rules like “picking up a card”, “skip turn”, “shuffle cards”, and more to facilitate the user’s creativity.
2. What are the 2-3 rich features of your DSL? A rich feature should be more complex than a choice in a set (e.g., the ability to choose between colours for a title is not a “rich” feature). What customization will each feature enable? Which features can be combined to interact in useful or creative ways?
   - Loops: a user can create a game in which they can perform multiple actions in a single turn using the looping feature. For example, in Blackjack, a player can HIT as many times as the player wants using the loop whereas in Go Fish each player can perform a single action each turn.
   - Conditionals: User can create many conditions or scenarios which influence the mechanics of the game. For example, in regular BlackJack one game ending condition is sum of a users card going above 21. Users are able to create custom version of BlackJack where the conditional could be 25.
   - Mutable Variable: For storing variables related to the game
     - Eg. Storing the “bust” value of BlackJack as a variable so that the user has the option to change the value
3. Example snippets of your DSL that illustrate at least each rich feature, and any interesting interaction between those.

```
# Config
_CONFIG:
	use_jokers = NO
	number_of_decks = 1
	number_of_players = 2

# Looping
on_user_turn:
	# turn mechanics for playing Blackjack
	action = wait_for(Action::HIT, Action::STAY)
	loop if action is Action::HIT and player is _ALIVE:
		action = wait_for(Action::HIT, Action::STAY)

# Mutable Variables
blackjack_limit = 25

check_user_action:
	# Conditionals
	if cards_in_hand > blackjack_limit:
		game.end()
```

## Note any important changes/feedback from TA discussion.

- We need to prioritize ensuring the rich features are available for the user within the DSL
- Ensure that we are coding an interpreter and not a compiler (due to scope issues)
- User stories are important, but should not take precedent over the rich features

## Note any planned follow-up tasks or features still to design.

- Create a standard representation of our DSL and divide tasks.
- Design a state machine for the overall game logic: Pre-Game, In-Game and Post-Game states





# Check-in 2 Report Items
## Planned division of main responsibilities between team members, considering how to enable working in parallel as much as possible. Consider the following points:
Modular design for the software system: what is the input, output of each component? Who is responsible for each component? Do you want to be jointly responsible for some components?
- Input: `.game` file
- Output: CLI/PyGame with user interaction

- Lexer/Parser
    - Input: lexer and parser files
    - Output: AST
    - Role: Read input files and return AST
- Checker
    - Input: AST (possibly with syntax issues)
    - Output: AST (clean, no syntax issues)
    - Role: Throw an error if AST is invalid
- Factory:
    - Input: AST (assumed clean)
    - Output: Game objects
    - Role: Create the Game objects defined by User
- Game
    - Input: Game objects
    - Output: User Action
    - Role:
        - Take user interaction and map it to the created Actions
        - “Play” the Game (logic for setting up, turn mechanisms and ending the game)
- GUI (PyGame/CLI)
    - Input: “commands” from the Game
    - Role:
        - Prompts user actions
        - Displays game state
        - Forwards user action to the Game
- Note:
    - These components may have different amount of work needed for completion
        - Expecting Parser, Checker to be completed by 1 person
        - Expecting Factory, Game, GUI needing 2 or more people
        - Current Plan: Assign 1 member to Parser, 1 member to Checker, 1 member to Factory, 1 member to Game and 1 member to CLI
            - As Parser and Checker gets completed, those members can hop on to help the other modules
            - 
What is the data at each interface point? Are there invariants over the data other than the class structure?
- In our DSL, a user must program with the three given states:
    - Config - Defining user variables, actions, and card value overrides
    - Game State - Defining functions, loops, and conditionals
    - End State - Defining what leads termination of the game
- Invariants:
    - Actions defined by us [system actions] (Game::pickCard(), Game::showCard(), etc.)
    - Logical operators for conditionals
    - Primitive types like integer and string(types cannot be changed)
    - Names/types of cards (Only the cards in a standard deck of cards will be represented)
        - Values for cards can be overwritten however

How will you be able to build component X independently? Can you write tests for component X independently of its dependent components?
- Standard representation (AST)
- Mocks
    - Mock Input and Output data to help independent module testing
- Components are the modules: Lexer/Parser, Checker, Factory, Game, UI (CLI/PyGame)
Who will be responsible for writing which tests, and when (will the same people write the tests as the code)?
- Potentially the same people that write the code will write the tests for that code. It is possible that some coding would not require tests until combined with others
    - Test-driven development (TDD)
    - We can review each other’s tests in the PRs
- Smoke test could be somewhat collaborative and written by more than one person (**Regression test**)
    - If we have time and depending on scope, this could be included
Are there design or other project tasks (possibly including team management), other than these components, that need to be assigned/completed?
- Kanban board needs setup (will be created after AST)
- User study design and implementation still needs to be assigned/completed

## Roadmap/timeline(s) for what should be done when, and how you will synchronise/check-in with each other to make sure progress is on-track. Talk clearly with your team members about your expectations for communication and progress, and what you will do as a team if someone falls behind.
- Project Due: Feb 25 (4 weeks or so)
- Week of Jan 22nd → Get standard representation setup, high level segregation of system into components, properly defining what those components will be.
- Week of Jan 29th → Writing failing tests for components individually + development of core components
- Week of Feb 5th → Writing failing tests for components individually + development of core components
- Week of Feb 12th → Some sort of UI completed, Design revisions and development of CLI + Plan for video
- Week of Feb 19th → PyGame + Testing, Final Video
- Project Check-in 2: Jan 26
- Project Check-in 3: Feb 2
    - Mockup of concrete language Syntax
    - Done a user study for syntax
    - What tests have been done, and what tests still need to be done
- Project Check-in 4: Feb 9
    - Plans for final user study
    - Planned timeline for remaining days
- Project Check-in 5: Feb 16
    - User study done for full DSL
    - Plans for final video
    - Planned timeline for remaining days

## Summary of progress so far.
- Finalized high-level grammar that will be converted to ANTLR rules
```
program: config game result

config : 'CONFIGURATION:' (statement | config_struct)* 'END CONFIGURATION' ;
statement: roles
config_struct : card_val_override | actions | variables ;

card_val_override : 'CARD VALUE OVERRIDE:' entity_card* joker_card 'END CARD VALUE OVERRIDE';
entity_card : 'ace' | 'king' | 'queen' | 'jack' '=' [0-9]+( 'or' [0-9]+)*;

// can be truetrue -> needs cleanup
joker_card : 'joker' = ^(true|false)$; 

actions : 'ACTIONS' user_actions+ 'END ACTIONS';


user_actions : user_action '=' system_actions( 'and' system_actions)*;
user_action: TEXT;
system_actions : "pickCard()"|"showCard()"|"hideCard()"|"skipTurn()"|"gameOver()";

roles : 'roles' '=' '{' role ',' role '}'
role : TEXT

variables_struct: 'VARIABLES:' role variable 'END VARIABLES'
variable : TEXT

TEXT: ^[A-Za-z0-9]+ (?!system_actions);
```

```
(* Definition of the game structure *)
game: "GAME:" functions "END GAME"

functions: function+
function: function_callback ":" func_statements "end"

(* Callback types for functions *)
function_callback: on_first_turn() | on_turn() | action_callback
action_callback: "on_" user_action

(* Statements within a function *)
func_statements: func_statement+
func_statement: assignment | user_action | system_action | loop | conditional

(* Assignment statement *)
assignment: variable "=" TEXT

(* Conditional statement *)
(* if they want multiple conditionals, they will have to nest their conditionals *)
conditional: "if" variable relational (variable | integer | string | boolean) ":" func_statements

(* Loop statement *)
loop: "LOOP" conditional ":" func_statements "END LOOP"

(* Relational operators *)
relational: ">" | "<" | "==" | "!=" | ">=" | "<="

(* Types of values *)
integer: [0-9]+
string: [A-Za-z]+ 
boolean: "TRUE" | "FALSE"

(* common functions between both roles *)
commons: "COMMON:" function+ "END COMMON"

(* Role override for rules/actions that are different between the two roles *)
role_override: role ":" function* "END " role
```
```
result: "RESULT:" conditional+ "END RESULT"
```
- High level structure of modules
- Timeline finished
