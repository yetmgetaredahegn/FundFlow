from langchain_ollama import ChatOllama

from app.schemas import (
    Evidence,
    ExtractionResult,
    InterviewQuestion,
    InterviewState,
)


MODEL_NAME = "llama3.1:8b"


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

INTERVIEW_QUESTIONS = [
    InterviewQuestion(
        field="company_name",
        question="What is the name of your business?",
    ),
    InterviewQuestion(
        field="type_of_business",
        question="What type of business do you operate?",
    ),
    InterviewQuestion(
        field="description",
        question=(
            "Please briefly describe what your business does."
        ),
    ),
    InterviewQuestion(
        field="address",
        question="Where is your business located?",
    ),
    InterviewQuestion(
        field="number_of_years_in_operation",
        question=(
            "How many years has your business been operating?"
        ),
    ),
    InterviewQuestion(
        field="funding_problem",
        question=(
            "What business problem are you seeking funding to solve?"
        ),
    ),
]


def extract_answer(
    question: InterviewQuestion,
    transcript: str,
) -> ExtractionResult:
    """
    Extract information only for the field currently being asked.

    The model must not infer or invent information that is not clearly
    established by the applicant's transcript.
    """
    structured_llm = llm.with_structured_output(
        ExtractionResult
    )

    prompt = f"""
You are extracting one piece of information from an applicant's
spoken answer for a funding application.

Target field: {question.field}

Question asked:
{question.question}

Applicant transcript:
{transcript}

Extract only information relevant to the target field.

Rules:
- Do not invent or infer missing facts.
- If the answer clearly establishes the requested value, return it.
- If the requested information is not established, return null for value.
- If the answer is vague or ambiguous, set ambiguous to true.
- Do not extract information for other application fields.
- Return the value in an appropriate simple form.

Examples:

Example of a valid extraction:

{{
    "value": "Adama Furniture Manufacturing",
    "ambiguous": false
}}

Example of information that is not established:

{{
    "value": null,
    "ambiguous": true
}}

For target field company_name:
Transcript: "My business is Adama Furniture Manufacturing."

The extracted value is the business name only, without unnecessary
introductory words.

For target field number_of_years_in_operation:
Transcript: "We have been operating for several years."

The number of years is not specifically established, so do not guess.
"""

    return structured_llm.invoke(prompt)

def start_interview() -> InterviewState:
    state = InterviewState()

    state.current_question = INTERVIEW_QUESTIONS[0]

    return state


def process_interview_answer(
    state: InterviewState,
    transcript: str,
) -> InterviewState:
    """
    Process one interview answer and update only the current target
    field when the information is clearly established.
    """
    current_question = state.current_question

    if current_question is None:
        return state

    extraction = extract_answer(
        question=current_question,
        transcript=transcript,
    )

    field = current_question.field

    state.application.evidence.append(
        Evidence(
            source="voice",
            value={
                "field": field,
                "transcript": transcript,
                "extracted_value": extraction.value,
                "established": extraction.value is not None,
                "ambiguous": extraction.ambiguous,
            },
        )
    )

    if extraction.value is not None:
        update_application_field(
            state=state,
            field=field,
            value=extraction.value,
        )

        state.completed_fields.append(field)

        state.current_question = get_next_question(
            completed_fields=state.completed_fields,
        )

    return state


def get_next_question(
    completed_fields: list[str],
) -> InterviewQuestion | None:
    for question in INTERVIEW_QUESTIONS:
        if question.field not in completed_fields:
            return question

    return None


def update_application_field(
    state: InterviewState,
    field: str,
    value: object,
) -> None:
    company_profile = (
        state.application.applicant.company_profile
    )

    if field == "company_name":
        company_profile.company_name = str(value)

    elif field == "type_of_business":
        company_profile.type_of_business = str(value)

    elif field == "description":
        state.application.applicant.company_overview.description = str(value)

    elif field == "address":
        company_profile.address = str(value)

    elif field == "number_of_years_in_operation":
        try:
            company_profile.number_of_years_in_operation = int(
                value
            )
        except ValueError:
            pass

    elif field == "funding_problem":
        state.application.intervention.problem_description = str(value)