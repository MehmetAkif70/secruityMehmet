# Flask Webapplicatie Test-Correct met TestGPT API

## Overzicht
Deze Flask-webapplicatie is ontworpen voor educatieve doeleinden, waarmee leraren notities en gerelateerde vragen kunnen beheren. Leraren kunnen notities toevoegen, bijwerken en verwijderen, en vragen genereren op basis van de inhoud van de notities.

## Functies
- Beheer van notities en vragen.
- Aanmaken van open en meerkeuzevragen met behulp van een geïntegreerde AI-gestuurde vraaggeneratie.
- Beheer van gebruikersaccounts voor leraren.
- Exporteren van vragen naar een CSV-bestand.

## Packages
- Python 3.x
- Flask
- SQLite
- OpenAI's GPT voor vraaggeneratie.

## Installatie en Uitvoering
1. Clone de repository: `git clone https://github.com/Rac-Software-Development/wp2-2023-mvc-1d2-ressurection.git`.
2. Navigeer naar de projectmap: `cd wp2-2023-mvc-1d2-ressurection`.
3. Installeer de vereiste bibliotheken: `pip install -r requirements.txt`.
4. Start de Flask-applicatie: `python website.py`.

## Gebruik
- Open een webbrowser en navigeer naar `http://localhost:5000` om de applicatie te gebruiken.
- Log in als leraar om toegang te krijgen tot de beheerfuncties.


## Referenties

https://platform.openai.com/docs/api-reference/chat
https://python-adv-web-apps.readthedocs.io/en/latest/flask_db3.html
https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/

HTML:
1. Codecademy. (n.d.). Learn HTML. Retrieved from https://www.codecademy.com/learn/learn-html
2. W3Schools. (n.d.). HTML Tutorial. Retrieved from https://www.w3schools.com/html/
3. The Net Ninja. (2018, April 16). HTML Tutorial for Beginners [Video]. YouTube. https://www.youtube.com/watch?v=qz0aGYrrlhU
4. The Net Ninja. (2015, August 27). HTML Tutorial 1 - Designing A Website In Notepad - Basics and Beginnings [Video]. YouTube. https://www.youtube.com/watch?v=kUMe1FH4CHE
5. The Net Ninja. (2015, August 28). HTML Tutorial 2 - Colours & Fonts [Video]. YouTube. https://www.youtube.com/watch?v=G3e-cpL7ofc

CSS:
6. DesignCourse. (2017, October 26). CSS Crash Course For Absolute Beginners [Video]. YouTube. https://www.youtube.com/watch?v=OXGznpKZ_sA
7. DesignCourse. (2017, November 2). Responsive CSS Tutorial [Video]. YouTube. https://www.youtube.com/watch?v=phWxA89Dy94
8. Codecademy. (n.d.). Learn CSS. Retrieved from https://www.codecademy.com/learn/learn-css
9. W3Schools. (n.d.). CSS Tutorial. Retrieved from https://www.w3schools.com/css/

Flask:
10. Pallets. (n.d.). Flask Tutorial. Retrieved from https://flask.palletsprojects.com/en/3.0.x/tutorial/
11. Codecademy. (n.d.). Learn Flask. Retrieved from https://www.codecademy.com/learn/learn-flask
12. Corey Schafer. (2018, September 17). Flask Tutorial [Video]. YouTube. https://www.youtube.com/watch?v=2YOBmELm_v0

Jinja:
13. UltraConfig. (n.d.). Jinja2: A crash course for beginners. Retrieved from https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/
14. Pallets. (n.d.). Jinja Templates. Retrieved from https://jinja.palletsprojects.com/en/3.1.x/templates/

Python:
15. Real Python. (n.d.). The Model-View-Controller (MVC) Paradigm Summarized with Legos. Retrieved from https://realpython.com/the-model-view-controller-mvc-paradigm-summarized-with-legos/
16. OpenClassrooms. (n.d.). Structure an Application with the MVC Design Pattern. Retrieved from https://openclassrooms.com/en/courses/6900866-write-maintainable-python-code/7009312-structure-an-application-with-the-mvc-design-pattern

Voor de beginpagina heb ik de code van Testcorrect moeten overnemen. Dit is gedaan door middel van de volgende chrome extensions: https://chromewebstore.google.com/detail/snipcss/hbdnoadcmapfbngbodpppofgagiclicf
Daarna heb ik alle onnodige delen eruit gehaald en de bestanden gedownload via chrome developer tools. 
gefinetuned met https://chat.openai.com/ met de volgende prompts:
      - show me how I can delete several not used parts from a css file. 
-	Did I do it right? 
-	How can I delete some javascript while keeping the key parts
-	What is javascript
-	Tell me about javascript
-	How can I see if something is javascript
-	{snippet code} is this javascript.
-	Still seeing eye 
-	The button is not in the box
-	Tell me about css and boxing
Admin panels: 
17.	The Net Ninja. (2019, February 19). Python Flask Tutorial: Full-Featured Web App Part 1 - Getting Started [Video]. YouTube. https://www.youtube.com/watch?v=WqHtmz8Ibn8
18.	Corey Schafer. (2020, April 13). Flask Tutorial #12 - Blueprints and Configuration [Video]. YouTube. https://www.youtube.com/watch?v=8BB3UK_pQy8
19.	Corey Schafer. (2020, April 20). Flask Tutorial #13 - Custom Error Pages [Video]. YouTube. https://www.youtube.com/watch?v=0cySORIhkCg
20.	Flask-Admin contributors. (n.d.). Introduction to Flask-Admin. Retrieved from https://flask-admin.readthedocs.io/en/latest/introduction/
21.	Reddit community. (2021, March 8). Need some help understanding the use of a Flask blueprint [Online forum post]. Reddit. https://www.reddit.com/r/flask/comments/m0z7s1/need_some_help_understanding_the_use_of_a_flask/?rdt=54760
22.	Stack Overflow community. (2018, August 13). Flask-Admin permissions for adding user with specific role [Online forum discussion]. Stack Overflow. https://stackoverflow.com/questions/51929968/flask-admin-permissions-for-adding-user-with-specific-role
23.	Flask-User contributors. (n.d.). Authorization. Retrieved from https://flask-user.readthedocs.io/en/latest/authorization.html
24.	The Net Ninja. (2019, February 22). Python Flask Tutorial: Full-Featured Web App Part 2 - Templates [Video]. YouTube. https://www.youtube.com/watch?v=bjcIAKuRiJw
25.	Reddit community. (2021, November 4). How to restrict access to admin panel in Flask [Online forum post]. Reddit. https://www.reddit.com/r/flask/comments/q8spq6/how_to_restrict_access_to_admin_panel_in_flask/
Header and jinja: 
26.	W3Schools. (n.d.). How To Create a Responsive Header. Retrieved from https://www.w3schools.com/howto/howto_css_responsive_header.asp
27.	The Net Ninja. (2018, November 19). Responsive Navbar Tutorial | HTML CSS & JavaScript [Video]. YouTube. https://www.youtube.com/watch?v=CgxEA9iMMWI
28.	Kevin Powell. (2020, April 7). Responsive Header / Navbar with CSS Grid [Video]. YouTube. https://www.youtube.com/watch?v=Oa9LTDR9ugU
29.	Ultimate Member. (n.d.). Header - Logged Out. Retrieved from https://docs.ultimatemember.com/article/1354-header-logged-out
30.	WordPress Community. (n.d.). What size should my SVG logo be for the header? [Online forum discussion]. WordPress Support Forum. https://wordpress.org/support/topic/what-size-should-my-svg-logo-be-for-the-header/
31.	Stack Overflow Community. (2014, August 16). Flask Jinja2 - How to separate header, base, and footer [Online forum discussion]. Stack Overflow. https://stackoverflow.com/questions/24847753/flask-jinja2-how-to-separate-header-base-and-footer
32.	Pallets. (n.d.). Templates. Retrieved from https://jinja.palletsprojects.com/en/2.11.x/templates/
Forum maken:
33.	W3Schools. (n.d.). HTML Forms. Retrieved from https://www.w3schools.com/html/html_forms.asp
34.	Mozilla Developer Network. (n.d.). Your first form. Retrieved from https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form
35.	W3Schools. (n.d.). How To Create a Contact Form. Retrieved from https://www.w3schools.com/howto/howto_css_contact_form.asp
36.	The Net Ninja. (2018, December 3). HTML Forms & Input Types (Web Development Tutorial for Beginners #10) [Video]. YouTube. https://www.youtube.com/watch?v=E5MEzC0prd4
37.	Academind. (2019, June 24). HTML Forms - All The Tags and Attributes You Need To Know [Video]. YouTube. https://www.youtube.com/watch?v=qelcFC6B_Nw
38.	Academind. (2019, June 25). Advanced HTML Forms - New HTML5 Form Fields [Video]. YouTube. https://www.youtube.com/watch?v=UEZ60e4MsgA
39.	The Net Ninja. (2019, October 7). Flask Tutorial for Beginners - HTML Forms & POST Requests (with Flask & Python) [Video]. YouTube. https://www.youtube.com/watch?v=v3CSQkPJtAc
40.	The Net Ninja. (2019, October 8). Flask Tutorial for Beginners - GET & POST Methods (with Flask & Python) [Video]. YouTube. https://www.youtube.com/watch?v=_KGMT9mjF0Y
41.	Codecademy. (n.d.). Flask Templates and Forms: Cheatsheet. Retrieved from https://www.codecademy.com/learn/learn-flask/modules/flask-templates-and-forms/cheatsheet