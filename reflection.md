# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1) Create tasks including their duration, priority, and a description of preferences
2) Create schedules of tasks factoring in their duration and priority
3) Explain reasoning used to choose the order of tasks in a schedule

Classes:
- Task should have fields for activity, duration, priority, and preferences
- Schedule should be initialized with a list of Tasks that is sorted based on duration and priority. Schedule should also have a field for the name of the pet the schedule is for, and have a method to return the reasoning used for its sorting.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Pet and Owner objects were added later at the request of the assignment.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Priority is considered before duration.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses duration instead of time of day since the time of day depends on what block of time is available for the user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

> I used AI mostly for refactoring and implementing method from the logic.

- What kinds of prompts or questions were most helpful?

> The AI assistant performed well when given exact details about how methods should be implemented.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

> When I prompted the AI to add Pet and Owner objects to the pawpal logic, it initially chose to only handle one Pet per Schedule.

- How did you evaluate or verify what the AI suggested?

> I verified the interaction of the objects by writing and running the main.py file.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

> I tested the functionality of features such as Schedule sorting and adding recurring Tasks. I also tested the Scheduler's handling of malformed inputs and incorrect inputs.

- Why were these tests important?

> These tests ensure that the app functions as intended and covers the users needs.

**b. Confidence**

- How confident are you that your scheduler works correctly?

> I am very confident that it works correctly between the test file, main.py, and manipulating the streamlit UI.

- What edge cases would you test next if you had more time?

> I would test for duplicated names for the various objects.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

> Functionality of the logic

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

> Redesign the UI to be more user-friendly

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

> It is important to clarify as much as possible about what you want the AI to design so that the implementation is exactly as you intended.