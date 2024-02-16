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

# Check-in 3 Report Items
## Explain a mockup of your concrete language design, including descriptions of both the syntax and what is meant to happen
For our language design, the grammar currently remains largely the same as last week's check-in: 
``` 
program: config game result
``` 
Our program will consist of 3 main parts: 
1. Config, which sets up the configuration for the card game. 
2. Game, which establishes the rules and actions for the card game. 
3. Result, which establishes the logic for deciding the end of the game and for determining the winner of the game. 
For the Config portion, we came up with this grammar: 
``` 
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
Within the Config portion, users should be able to create different statements and config_structs that set up different parts of the game. The statements are for establishing roles within the card game (such as creating a Player or a Dealer), while the config_structs serve multiple purposes. The config_structs can be one of 3 things: 
1. Overriding the values of certain cards (eg. setting king=10 for a game of blackjack) 
2. Defining actions that the user can take (eg. setting HIT=pickCard()) 
3. Defining user variables 
For the Game portion, we came up with this grammar:
``` 
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
Within the Game portion, users should be able to define different functions that act as the rules to the card game. These functions can be applied to either all players (by inculding them in the common block) or to specific players (by including those functions in an role_override block). Within those functions, users can define different types of callbacks, which tell us when/where the user wants the function to execute (eg. execute this function on_turn(), which means that on each player's turn this function will execute). Within those callbacks, users can then setup different variable assignments, conditionals, loops, and call actions defined in Config. 
For the Result portion, we have: 
``` 
result: "RESULT:" conditional+ "END RESULT" 
``` 
Within the Result portion, users only have to define certain conditionals for when/how the game ends. The user can also define conditionals for how the game decides who the winner of the game is. 
### Include the example snippets you used in your user study, and their outputs.
For the example snippets used in our user study, we essentially gave them an overview of our grammar and let them try to make the card game Blackjack out of it. The outputs from our user study are as follows: 
User 1: 
``` 
# CONFIG
CONFIGURATION:

	CARD VALUE OVERRIDE:
		ace = 1 or 11 
		king, queen, jack = 10
		joker = false
	END CARD VALUE OVERRIDE
	
	roles = {DEALER, PLAYER}
	
	ACTIONS:
		HIT = Game::pickCard() // need to preserve order
		STAY = Game::skipTurn()
		SHOW = Game::showCard()
		HIDE = Game::hideCard()
		FORFIT = Game::skipTurn() and Game::gameOver()
		HITHIDE = Game::pickCard() and Game::hideCard()
		HITSHOW = Game::pickCard() and Game::showCard()
		PICK2CARDS = Game::pickCard() and Game::pickCard()
	END ACTIONS
	
	VARIABLES: // user variable
		DEALER score
		PLAYER score
	END VARIABLES:

END CONFIGURATION

# GAME
DEALER:

	setup():
		cards = 2
		HIDE
		end
	
	on_turn():
		loop if score < 17:
			HIT
		end
		
	on_HIT():
		score = score + card
	
		if score >= 21:
			Game::gameOver()

END DEALER
PLAYER:

	setup:
		cards = 2
		end
	
	on_turn:
		# turn mechanics for playing Blackjack
		action = wait_for(HIT, STAY)
		loop if action is HIT:
			action = wait_for(HIT, STAY)
		end
	
	on_HIT():
		score = score + card
	
		if score >= 21:
			Game::gameOver()
		
	
	on_STAY():
		none


END PLAYER

# RESULT
DEALER score > 21
PLAYER score > 21
``` 
User 2: 
``` 
# CONFIG
CONFIGURATION:
	CARD VALUE OVERRIDE:
		joker = false
	END CARD VALUE OVERRIDE

	roles = {PLAYER1, PLAYER2}

	ACTIONS:
		COMPARE = Game::showCard() and Game::showCard()
		FISH = Game::pickCard() 
		GOFISH = Game::skipTurn()
		GIVE = Game::giveCard(card)
		TAKE = Game::getCard(card)
		PICK = Game::showCard()


	END ACTIONS

	VARIABLES:
		PLAYER1 numPairs
		PLAYER2 numPairs
		PLAYER1 comparisonCard
		PLAYER2 comparisonCard
		PLAYER1 found
		PLAYER2 found

	END VARIABLES

END CONFIGURATION

# GAME 
COMMON:

	setup():
		cards = 10
		SHOW
		loop card in cards
			COMPARE
			comparisonCard = card
		end

	on_turn():
		found = false
		PICK
		response = Game::request(GIVE or GOFISH)
		if response == GIVE
			TAKE
			numPairs = numPairs + 1
		else 
			FISH
			comparisonCard = card
			COMPARE 
	end
			
		
	on_COMPARE():
		if card == comparisonCard
			numPairs = numPairs + 1
			found = TRUE
		comparisonCard = none


	on_request():
		comparisonCard = request
		COMPARE
		if found
			GIVE
		else
			GOFISH


END COMMON
``` 
## Notes about first user study 
### What did they find easy/difficult?
In terms of what they found easy: 
- The overall structure was clear and easy to understand
- The idea behind the DSL was straightforward 
In terms of what they found difficult: 
- Not having an ability to communicate between players or different roles was an issue 
- No global variables (that are accessible in any scope)
- A lot of bloat; there seems to be a lot of unnecessary syntax
- Limited options for actions, and how to use them was unclear 
### What did you learn from your user(s)? 
From our users, we learned that:
- Our language doesn’t support interaction between players, so some games might not longer be possible
- We abstracted some syntax out, but the syntax still feels bloated 
- Some parts of the syntax were confusing and unclear 
### Is there anything you would have done differently? Can this be done for your final user study?
For what we would have done differently: 
- Explain/give more context behind how to use the language 
- Rework parts of our syntax to make it easier to work with and more clear 
Both of these should be easily doable in our final user study. 
## What changes to your language design have you made so far, or are considering?
We are considering the following changes: 
- Rename 'on_first_turn' to 'setup' (to make it clear that this block should contain functions for setting up the game) 
- Allowing for more function calls 
- Reworking a lot of the grammar to make it easier to understand and reduce the amount of unneccessary syntax 
### How does this affect the example snippets you include here?
- Any 'on_first_turn' blocks will be replaced with 'setup' blocks 
- The structure of the syntax would likely change for a lot of the Config and Game portions of the example snippets 
## Any changes to your project timeline/plan that you need to make? 
Since we are behind schedule with regards to our original timeline/plan, we will need to push back our core development to include the week of Feb 12th. Additionally, since we are thinking of reworking parts of our grammar, that delays our completion of the parser and checker, which means we will have to push the completion of those components further back as well (likely by a week). 
## Are there new tests you can write now, based on your current project status?
For our current project status, since we are still in the process of both reworking the grammar and completing the parser and lexer, we can write tests to ensure that the parser and lexer are providing the correct output. 
### How can your snippets be made into unit tests, and for which component(s)?
We can use the snippets as input for tests on different components, particularly the lexer and parser to ensure that the tokens are being created and parsed correctly. As well, we can translate snippets into sample ASTs, then use those mock ASTs both for development of other components and to ensure that the output from our lexer and parser is correct. 
#### What about planned error handling in your components? Tests for these?
We will have planned error handling or lexer and parser in case we see tokens being generated that are invalid or not what we expect. These errors can then be validated with error tests (tests to ensure that our error handling is throwing and catching errors as intended). Furthermore, we will have error handling for our game factory component to ensure that the input from our AST doesn't include any errors (as an additional check after the AST has gone through our checker component). 


# Check-in 4 Report Items
## Status of implementation
### Component-wise progress
- We have five main components in our design: the Parser, Checker, Factory, Game and User Interface
    - Parser: We’ve finished the parser and we are able to parse an input file correctly in a predictable manner without errors
    - Checker: As next steps, we need to convert the ANTLR parse tree into a simpler AST so that we can use the visitor pattern to perform static checks on consistent variable and function declarations. We aim to finish this module by the end of next week.
    - Factory: We have designing the high-level objects used in our game. We started implementing this design and started parsing the input data to construct these objects.
    - Game: Not yet started. The work on the Game depends on work from the Factory being completed. It is a simpler component than the others, so it is acceptable to start this module later.
    - User Interface: Not yet started. We have been focusing on setting up the backend for now.

### Which tests are passing, and which not?
We have made tests for the Parser module and a basic test for the Factory module. The Parser module tests stress-tests the grammar with basic inputs as well as challenging, incorrect inputs.

### Which extra tests still need to be written/made?
We need tests for:
- Converting the ANTLR4 parse tree to the AST
- Correctness of the Checker (throwing an error when a static check fails)
- Testing the correctness of the objects generated by the Factory module
- Game module logic
- End-to-end manual tests with the GUI

## Plans for final user study.
### Are there any major differences from the previous one? If so, what are the reasons?
- The main difference is that we will have a MVP platform that users can test their code as they write it, providing them with useful feedback so that they are less reliant on us to explain the DSL to them.
- Another difference is that we will provide them with a starter template that they can work from since our language requires a lot of upfront configuration, which was confusing to our testers in the first user study.
- We will also provide smaller, understandable examples for using the DSL since initial test users found the syntax confusing.

## Planned timeline for the remaining days.
- Week of Feb 12: We plan to have some sort of a basic UI running, finishing the Checker, Factory and the Game module. By next weekend, we hope to be able to perform some user studies with our DSL.
- Week of Feb 19: We plan to create the final video, testing the DSL thoroughly end-to-end from input to Game and challenging it with unusual scenarios and fixing issues as they come up.

# Check-in 5 Report Items

## Status of user study (should be completed this week at the latest) 
- The user study will be done by February 18th (this week).

## Last minute changes to design, implementation, or tests

- Syntax updates:
    - To improve code clarity and simplicity, the 'END' was removed from our state syntax.
    - The syntax now supports complex arithmetic operations.
    - The introduction of a DOT feature allows for direct access to internal variables or functions declared within the role module
    - Mock implemented of BlackJack using our DSL:
```
CONFIGURATION
    CARD_VALUE_OVERRIDE
        ace = 11;
        king = 10;
        queen = 10;
        joker = FALSE;
        roles = PLAYER and DEALER;
    ACTIONS
        set HIT does pickCard();
        set STAND does endTurn();
    VARIABLES
		set PLAYER has score;
        set PLAYER has input;
        set DEALER has score;
        set DEALER has input;
GAME
    COMMON
        setup()
            DEALER.score = 0;
            PLAYER.score = 0;
        end function

    USER_OVERRIDE PLAYER
            on_turn()
                PLAYER.input = InputFromPlayer(PLAYER);
                loop (PLAYER.score < 22)

                    if(input == HIT)
                        PLAYER.score = PLAYER.score + PLAYER.HIT;
                        if((card == ace) and (PLAYER.score > 21))
                            PLAYER.score = PLAYER.score - 11 + 1;
                        end if
                    end if

                    if(input == STAND)
                        PLAYER.STAND;
                    end if

                    PLAYER.score = card + PLAYER.score;
                    PLAYER.SHOW;
                end loop
                PLAYER.STAND;
            end function

    USER_OVERRIDE DEALER
            on_turn()
                loop (DEALER.score < 17)
                    card = DEALER.HIT;
                    DEALER.score = card + DEALER.score;
                    DEALER.SHOW;
                end loop
                DEALER.STAND;
								on_show_result()
	           end function

RESULT
    if (PLAYER.score > 21)
        PLAYER = BUST;
    end if
    if (DEALER.score > 21)
        DEALER = BUST;
    end if
    if (PLAYER.score > DEALER.score)
        PLAYER = WIN;
    else
        DEALER = WIN;
    end if
```
- AST updates:
    - Refactored the structure of the tree to make it clearer and more intuitive for human interpretation.
    - Add new AST nodes, resulting in a total of approximately 20 nodes
    - Mock implemented: e.g value(node name)  
```
'PROGRAM' (ProgramNode)
  | 'CONFIGURATION' (ConfigurationNode)
  |   | 'CARD_VALUE_OVERRIDE' (CardValueOverrideNode)
  |   |   | 'CARDS' (CardsNode)
  |   |   |   | 'ace' (CardTypeNode)
  |   |   |   |   | '11' (CardValueNode)
  |   |   |   | 'king' (CardTypeNode)
  |   |   |   |   | '10' (CardValueNode)
  |   |   |   | 'queen' (CardTypeNode)
  |   |   |   |   | '10' (CardValueNode)
  |   |   |   | 'joker' (CardTypeNode)
  |   |   |   |   | 'FALSE' (CardValueNode)
  |   |   | 'ROLES' (RoleNode)
  |   |   |   | 'DEALER' (RoleNameNode)
  |   |   |   | 'PLAYER' (RoleNameNode)
  |   | 'ACTIONS' (ActionsNode)
  |   |   | 'HIT' (ActionNode)
  |   |   | 'STAND' (ActionNode)
  |   | 'VARIABLES' (VariablesNode)
  |   |   | 'DEALER' (VariableRoleNode)
  |   |   |   | 'score' (VariableAssigneeNode)
  |   |   | 'PLAYER' (VariableRoleNode)
  |   |   |   | 'score' (VariableAssigneeNode)
  | 'GAME' (GameNode)
  |   | 'COMMON' (CommonNode)
  |   |   | 'setup()' (FunctionNode)
  |   |   |   | 'DEALER' (VariableAssigneeNode)
  |   |   |   |   | '0' (ExpressionValueNode)
  |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   | '0' (ExpressionValueNode)
  |   | 'USER_OVERRIDES' (CommonNode)
  |   |   | 'on_turn()' (FunctionNode)
  |   |   |   | 'input' (VariableAssigneeNode)
  |   |   |   |   | 'InputFromPlayer' (FunctionNameNode)
  |   |   |   |   |   | 'PLAYER' (ExpressionValueNode)
  |   |   |   | 'LOOP' (LoopNode)
  |   |   |   |   | '<' (OperatorNode)
  |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   |   | '22' (ExpressionValueNode)
  |   |   |   |   | 'IF' (IfNode)
  |   |   |   |   |   | '==' (OperatorNode)
  |   |   |   |   |   |   | 'input' (ExpressionValueNode)
  |   |   |   |   |   |   | 'HIT' (ExpressionValueNode)
  |   |   |   |   |   | 'THEN' (IfNode)
  |   |   |   |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   |   |   |   | '+' (OperatorNode)
  |   |   |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   |   |   | 'HIT' (UserActionNode)
  |   |   |   |   |   |   | 'IF' (IfNode)
  |   |   |   |   |   |   |   | 'and' (OperatorNode)
  |   |   |   |   |   |   |   |   | '==' (OperatorNode)
  |   |   |   |   |   |   |   |   |   | 'card' (ExpressionValueNode)
  |   |   |   |   |   |   |   |   |   | 'ace' (ExpressionValueNode)
  |   |   |   |   |   |   |   |   | '>' (OperatorNode)
  |   |   |   |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   |   |   |   |   |   | '21' (ExpressionValueNode)
  |   |   |   |   |   |   |   | 'THEN' (IfNode)
  |   |   |   |   |   |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   |   |   |   |   |   | '+' (OperatorNode)
  |   |   |   |   |   |   |   |   |   |   | '-' (OperatorNode)
  |   |   |   |   |   |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   |   |   |   |   |   |   |   | '11' (ExpressionValueNode)
  |   |   |   |   |   |   |   |   |   |   | '1' (ExpressionValueNode)
  |   |   |   |   | 'IF' (IfNode)
  |   |   |   |   |   | '==' (OperatorNode)
  |   |   |   |   |   |   | 'input' (ExpressionValueNode)
  |   |   |   |   |   |   | 'STAND' (ExpressionValueNode)
  |   |   |   |   |   | 'THEN' (IfNode)
  |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   | 'STAND' (UserActionNode)
  |   |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   |   | '+' (OperatorNode)
  |   |   |   |   |   |   | 'card' (ExpressionValueNode)
  |   |   |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   |   | 'SHOW' (UserActionNode)
  |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   | 'STAND' (UserActionNode)
  |   | 'USER_OVERRIDES' (CommonNode)
  |   |   | 'on_turn()' (FunctionNode)
  |   |   |   | 'LOOP' (LoopNode)
  |   |   |   |   | '<' (OperatorNode)
  |   |   |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   |   | '17' (ExpressionValueNode)
  |   |   |   |   | 'card' (VariableAssigneeNode)
  |   |   |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   |   |   | 'HIT' (UserActionNode)
  |   |   |   |   | 'DEALER' (VariableAssigneeNode)
  |   |   |   |   |   | '+' (OperatorNode)
  |   |   |   |   |   |   | 'card' (ExpressionValueNode)
  |   |   |   |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   |   |   |   | 'score' (UserActionNode)
  |   |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   |   | 'SHOW' (UserActionNode)
  |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   | 'STAND' (UserActionNode)
  | 'RESULT' (ResultNode)
  |   | 'IF' (IfNode)
  |   |   | '>' (OperatorNode)
  |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   | 'score' (UserActionNode)
  |   |   |   | '21' (ExpressionValueNode)
  |   |   | 'THEN' (IfNode)
  |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   | 'BUST' (ExpressionValueNode)
  |   | 'IF' (IfNode)
  |   |   | '>' (OperatorNode)
  |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   | 'score' (UserActionNode)
  |   |   |   | '21' (ExpressionValueNode)
  |   |   | 'THEN' (IfNode)
  |   |   |   | 'DEALER' (VariableAssigneeNode)
  |   |   |   |   | 'BUST' (ExpressionValueNode)
  |   | 'IF' (IfNode)
  |   |   | '>' (OperatorNode)
  |   |   |   | 'PLAYER' (UserNode)
  |   |   |   |   | 'score' (UserActionNode)
  |   |   |   | 'DEALER' (UserNode)
  |   |   |   |   | 'score' (UserActionNode)
  |   |   | 'THEN' (IfNode)
  |   |   |   | 'PLAYER' (VariableAssigneeNode)
  |   |   |   |   | 'WIN' (ExpressionValueNode)
  |   |   | 'ELSE' (IfNode)
  |   |   |   | 'DEALER' (VariableAssigneeNode)
  |   |   |   |   | 'WIN' (ExpressionValueNode)
```
- To manage the UI and game logic efficiently, we plan to employ a queue-based system involving two separate queues: one dedicated to the UI and another for the game mechanics. 
    - The front end will be responsible for retrieving game actions from its queue, and then re-queuing these actions for the game to interpret and execute the action.

## Plans for final video 
- One team member will set up a random game scenario(e.g BlackJack) and provide a brief explanation of the underlying code.
- A code demonstration will be followed by a live game demo to showcase the practical implementation and effects of the code on the game.
- The video will conclude with a segment highlighting the progress made based on feedback from initial to final user studies.


## Planned timeline for the remaining days.
- Feb 16:
    - Complete AST (Abstract Syntax Tree) and Static Checker development.
    - Implement tests to convert ANTLR4 parse tree to AST, ensuring errors are thrown for syntax mistakes.
    - Implement tests to verify the correctness of objects generated by the Factory module.
- Feb 18:
    - Finish integration of the Factory and Game modules.
    - Finalize the MVP
    - Conduct a user study to gather feedback on our DSL
    - Film the final video presentation.
- Feb 22:
    - Focus on bug fixes and final refinements.
