# Email Classifier – Machine Learning Project

This project implements an email classification pipeline inspired by academic
literature on keyword-based text processing and developed for a Machine Learning
course.

## Project Overview
The goal of the project is to automatically classify corporate support emails
into semantic categories using text preprocessing, keyword extraction, and
rule-based classification strategies.

## Dataset
The original dataset consists of anonymized corporate emails stored in JSON
format. Due to privacy constraints, the raw data is not publicly available.
The dataset includes email metadata, content, and thread structure.

## Classification Logic
Emails are classified into the following categories:
- farming
- storage
- network
- sysop

The classification is performed by analyzing email subjects and contents,
including thread-level information and category-specific keyword dictionaries.

## Methods
- Text preprocessing and cleaning
- Keyword extraction
- Email summarization
- Rule-based classification
- Thread-level label propagation

## Technologies
- Python
- Pandas
- NLTK

## References
This project is inspired by academic work on email classification and text
summarization, adapted and implemented for educational purposes.
