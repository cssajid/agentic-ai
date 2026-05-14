#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from backoffice_app.crew import BackofficeApp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
         "application_id": "GCAA-001-XYZ",

    "current_step_business_logic": "Introduction of application",

    "form_data": {
        "name": "Sajid Ahmad",
        "age": 20
    },

    "documents": [
        {
            "document_type": "passport",
            "file_name": "passport.pdf"
        }
    ],

    "document_rules": {
        "required_documents": [
            "passport"
        ],
        "allowed_formats": [
            "pdf",
            "jpg",
            "png"
        ]
    },

    "comparison_rules": {
        "fields_to_match": [
            "name",
            "age"
        ]
    },

    "business_rules": {
        "minimum_age": 21
    },

    "available_actions": [
        {
            "action_title": "approved",
            "rule": "confidence >= 90"
        },
        {
            "action_title": "reject",
            "rule": "confidence < 50"
        },
        {
            "action_title": "more_info",
            "rule": "confidence between 50 and 90"
        }
    ]
    }

    # Create and run the crew
    result = BackofficeApp().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
