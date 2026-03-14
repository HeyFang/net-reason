from fact_base import FactBase
from inference_engine import InferenceEngine
from question_engine import ask_questions
from explanation import print_diagnosis


def main():

    fact_base = FactBase()

    ask_questions(fact_base)

    engine = InferenceEngine(
        fact_base,
        "rules/network_rules.json"
    )

    engine.run()

    print_diagnosis(fact_base.facts)


if __name__ == "__main__":
    main()
