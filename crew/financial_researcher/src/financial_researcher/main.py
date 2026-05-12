#!/usr/bin/env python
# src/financial_researcher/main.py
import sys
from unittest import result
import warnings

from datetime import datetime

from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """ Run the Financial Researcher crew. """
    inputs = {
        'company': 'Apple'
    }

    # Create and run the crew
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    if __name__ == "__main__":
        run()