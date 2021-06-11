# Exam Automation Python
![GitHub](https://img.shields.io/github/license/oguzhnatly/Exam-Automation-Python)
![Python Version](https://img.shields.io/badge/python-v3.7-blue?style=flat&logo=python&logoColor=lightblue)
![GitHub last commit](https://img.shields.io/github/last-commit/oguzhnatly/Exam-Automation-Python)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/oguzhnatly@gmail.com)

## Getting Started
Project can be started with `npm start` command in terminal.

## Project Description
In this project, you are supposed to work on a system for university placement exam. We already
have the following information related with this exam; student information, their answers to
questions, their choices of universities and university information. There are 40 questions in the
exam book and each question has five possible choices. (a,b,c,d,e). 4 wrong answers will take away
one of the correct ones. Every correct answer is worth 15 points.

## File Requirements
`key.txt` It contains the answers of 40 questions. There are two lines for question book type A and B
in this file.<br>
`university.txt` It contains the list of the universities, their base points and capacity. <br>
`student.txt` It contains the 6 digit id, name and last name of a student. <br>
`answers.txt` It contains the student id, question book type, answers and the id of choices of
universities a student. There will be only two choices for universities. The placement will be done
based on student’s score and choices. The answers that left blank is shown with "*".

## Menu
1) Search for a student with a given id and display his/her name and last name.
2) List the university/universities and departments with a maximum base points.
3) Create a file named results.txt which will have, student id, name, last name, book type,
number of correct, incorrect and blank answers, number of answers after reducing the wrong
ones based on the formula given above, score, name of the schools given as a choice.
4) List the student information (id, name, last name) sorted by their score.
5) List the students placed in every university/department. Display the name of the university
and the department first and then the list of students who were place into that
department.
6) List the students who were not be able to placed anywhere and who didn't take the exam. 
7) List all the departments.
8) Display the menu again.
9) Exit.
