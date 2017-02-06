ThoughtWorks Code Assignment
============================

Rules
-----

1. You may not use any external libraries to solve this problem, but
   you may use external libraries or tools for building or testing
   purposes. Specifically, you may use unit-testing libraries or build
   tools available for your chosen language (e.g., JUnit, Ant, NUnit,
   Rspec, Rake, etc.).

2. Please name your code with the problem and language used. Remember
   to also include a brief explanation of your design and assumptions,
   along with your code, as well as detailed instructions to run your
   application.
3. We assess a number of things including the design aspect of your
   solution and your object oriented programming skills. While these
   are small problems, we expect you to submit what you believe is
   production-quality code; well-tested code that you’d be able to
   run, maintain, and evolve. You don’t need to gold plate your
   solution, however we are looking for something more than a
   bare-bones algorithm
4. We want our hiring process to be fair, and for everyone to start
   from the same place. To enable this, we request that you do not
   share or publish these problems or your solutions.


Problem: Conference Track Management
------------------------------------

You are planning a big programming conference and have received many
proposals which have passed the initial screen process but you're
having trouble fitting them into the time constraints of the day --
there are so many possibilities!

So you write a program to do it for you.

- The conference has multiple tracks each of which has a morning and afternoon session.
- Each session contains multiple talks.
- Morning sessions begin at 9am and must finish by 12 noon, for lunch.
- Afternoon sessions begin at 1pm and must finish in time for the networking event.
- The networking event can start no earlier than 4:00 and no later than 5:00.
- No talk title has numbers in it.
- All talk lengths are either in minutes (not hours) or lightning (5 minutes).
- Presenters will be very punctual; there needs to be no gap between sessions.

.. note:: Depending on how you choose to complete this problem, your
          solution may give a different ordering or combination of talks into
          tracks. This is acceptable; you don’t need to exactly duplicate the
          sample output given here.


Test input:
-----------

Writing Fast Tests Against Enterprise Rails 60min
Overdoing it in Python 45min
Lua for the Masses 30min
Ruby Errors from Mismatched Gem Versions 45min
Common Ruby Errors 45min
Rails for Python Developers lightning
Communicating Over Distance 60min
Accounting-Driven Development 45min
Woah 30min
Sit Down and Write 30min
Pair Programming vs Noise 45min
Rails Magic 60min
Ruby on Rails: Why We Should Move On 60min
Clojure Ate Scala (on my project) 45min
Programming in the Boondocks of Seattle 30min
Ruby vs. Clojure for Back-End Development 30min
Ruby on Rails Legacy App Maintenance 60min
A World Without HackerNews 30min
User Interface CSS in Rails Apps 30min


Test output:
------------

Track 1:
~~~~~~~~

09:00AM Writing Fast Tests Against Enterprise Rails 60min
10:00AM Overdoing it in Python 45min
10:45AM Lua for the Masses 30min
11:15AM Ruby Errors from Mismatched Gem Versions 45min
12:00PM Lunch
01:00PM Ruby on Rails: Why We Should Move On 60min
02:00PM Common Ruby Errors 45min
02:45PM Pair Programming vs Noise 45min
03:30PM Programming in the Boondocks of Seattle 30min
04:00PM Ruby vs. Clojure for Back-End Development 30min
04:30PM User Interface CSS in Rails Apps 30min
05:00PM Networking Event

Track 2:
~~~~~~~~

09:00AM Communicating Over Distance 60min
10:00AM Rails Magic 60min
11:00AM Woah 30min
11:30AM Sit Down and Write 30min
12:00PM Lunch
01:00PM Accounting-Driven Development 45min
01:45PM Clojure Ate Scala (on my project) 45min
02:30PM A World Without HackerNews 30min
03:00PM Ruby on Rails Legacy App Maintenance 60min
04:00PM Rails for Python Developers lightning
05:00PM Networking Event
