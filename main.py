from pawpal_system import Task, Pet, Schedule, Owner

groom = Task("groom", 20, "low")
walk = Task("walk", 30, "high", "prefers to walk fast")
do_a_trick = Task("do a trick", 40, "medium")

mo = Pet("Mo", "dog", "terrier", 2, [groom, walk, do_a_trick])
eve = Pet("Eve", "frog", "glass", 3, [do_a_trick])

mccrea = Owner("McCrea", [mo, eve])

today = Schedule(mccrea)

today.build_plan(120)
today.print_plan()