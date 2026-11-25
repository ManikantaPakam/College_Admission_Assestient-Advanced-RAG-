import os
import json
import asyncio
import pandas as pd
import instructor

import random
from openai import InternalServerError

from pathlib import Path
from dotenv import load_dotenv
from google import genai
from openai import AsyncOpenAI

from app.rag.pipeline import advanced_retrieval_pipeline
from app.generation.answer_generator import generate_answer

from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)


# --------------------------------------------------
# STEP 1: Load Environment Variables
# --------------------------------------------------

load_dotenv()

DATASET_PATH = Path("evaluation/test_dataset.json")

RESULTS_DIR = Path("evaluation/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# STEP 2: Configure Gemini Evaluator
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing in .env"
    )


# Create asynchronous Gemini-compatible client

evaluator_client = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Initialize RAGAS LLM using Instructor adapter

evaluator_llm = llm_factory(
    model="gemini-3.8-flash",
    provider="openai",
    client=evaluator_client,
    adapter="instructor",
    mode=instructor.Mode.MD_JSON,
    max_tokens=4096
)


# Initialize Google GenAI client for embeddings

embedding_client = genai.Client(
    api_key=GOOGLE_API_KEY
)


evaluator_embeddings = GoogleEmbeddings(
    client=embedding_client,
    model="gemini-embedding-001"
)


print("\nGemini Evaluator Initialized Successfully!")

print(
    "Evaluator Async Status:",
    evaluator_llm.is_async
)


if not evaluator_llm.is_async:
    raise RuntimeError(
        "RAGAS evaluator is not using an asynchronous client. "
        "Check AsyncOpenAI and Instructor configuration."
    )


# --------------------------------------------------
# STEP 3: Initialize RAGAS Metrics
# --------------------------------------------------

faithfulness_metric = Faithfulness(
    llm=evaluator_llm
)


answer_relevancy_metric = AnswerRelevancy(
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)


context_precision_metric = ContextPrecision(
    llm=evaluator_llm
)


context_recall_metric = ContextRecall(
    llm=evaluator_llm
)


print("\nRAGAS Metrics Initialized Successfully!")


# --------------------------------------------------
# STEP 4: Load Evaluation Dataset
# --------------------------------------------------

def load_test_dataset():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {DATASET_PATH}"
        )

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)

    if not dataset:
        raise ValueError(
            "Evaluation dataset is empty."
        )

    return dataset


# --------------------------------------------------
# STEP 5: Execute RAG Pipeline
# --------------------------------------------------

def collect_evaluation_samples():

    test_questions = load_test_dataset()

    evaluation_samples = []

    for item in test_questions:

        question = item["question"]
        reference = item["reference"]

        print("\n" + "=" * 60)

        print("Question:", question)


        # ------------------------------------------
        # Step 1: Advanced Retrieval Pipeline
        # ------------------------------------------

        retrieval_result = advanced_retrieval_pipeline(
            question=question,
            top_k=5,
            top_n=3,
            metadata_filter=None
        )

        documents = retrieval_result["documents"]


        if not documents:
            print(
                "Warning: No documents retrieved for:",
                question
            )

            continue


        # ------------------------------------------
        # Step 2: Generate Answer
        # ------------------------------------------

        answer_result = generate_answer(
            question,
            documents
        )

        answer = answer_result["answer"]


        # ------------------------------------------
        # Step 3: Extract Retrieved Contexts
        # ------------------------------------------

        contexts = [
            document.page_content
            for document in documents
        ]


        # ------------------------------------------
        # Step 4: Prepare Evaluation Sample
        # ------------------------------------------

        evaluation_samples.append({

            "user_input": question,

            "response": answer,

            "retrieved_contexts": contexts,

            "reference": reference

        })


        print("\nGenerated Answer:")
        print(answer)

        print("\nRetrieved Context Count:")
        print(len(contexts))


    if not evaluation_samples:
        raise ValueError(
            "No valid evaluation samples were collected."
        )

    return evaluation_samples

# --------------------------------------------------
# Retry Utility for Temporary Gemini API Errors
# --------------------------------------------------

async def execute_metric_with_retry(
    metric,
    max_retries=4,
    **kwargs
):

    for attempt in range(max_retries):

        try:

            return await metric.ascore(**kwargs)

        except InternalServerError as error:

            if error.status_code != 503:
                raise

            if attempt == max_retries - 1:
                raise

            wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(
                f"\nGemini API temporarily unavailable."
            )

            print(
                f"Retrying in {wait_time:.2f} seconds..."
            )

            await asyncio.sleep(wait_time)

    raise RuntimeError("Metric evaluation failed.")


# --------------------------------------------------
# STEP 6: Evaluate Individual Metrics
# --------------------------------------------------

async def evaluate_metrics(evaluation_samples):

    evaluation_results = []


    for index, sample in enumerate(
        evaluation_samples,
        start=1
    ):

        print("\n" + "=" * 60)

        print(f"Evaluating Question {index}")

        print("Question:", sample["user_input"])


        # ------------------------------------------
        # Metric 1: Faithfulness
        # ------------------------------------------

        print("\nCalculating Faithfulness...")

        faithfulness_result = await execute_metric_with_retry(
            faithfulness_metric,
            user_input=sample["user_input"],
            response=sample["response"],
            retrieved_contexts=sample["retrieved_contexts"]
        )


        # ------------------------------------------
        # Metric 2: Answer Relevancy
        # ------------------------------------------

        print("\nCalculating Answer Relevancy...")

        answer_relevancy_result = await execute_metric_with_retry(
            answer_relevancy_metric,
            user_input=sample["user_input"],
            response=sample["response"]
        )


        # ------------------------------------------
        # Metric 3: Context Precision
        # ------------------------------------------

        print("\nCalculating Context Precision...")

        context_precision_result = await execute_metric_with_retry(
            context_precision_metric,
            user_input=sample["user_input"],
            reference=sample["reference"],
            retrieved_contexts=sample["retrieved_contexts"]
        )


        # ------------------------------------------
        # Metric 4: Context Recall
        # ------------------------------------------

        print("\nCalculating Context Recall...")

        context_recall_result = await execute_metric_with_retry(
            context_recall_metric,
            user_input=sample["user_input"],
            reference=sample["reference"],
            retrieved_contexts=sample["retrieved_contexts"]
        )


        # ------------------------------------------
        # Collect Evaluation Results
        # ------------------------------------------

        result = {

            "question": sample["user_input"],

            "faithfulness": faithfulness_result.value,

            "answer_relevancy": answer_relevancy_result.value,

            "context_precision": context_precision_result.value,

            "context_recall": context_recall_result.value

        }


        evaluation_results.append(result)


        # ------------------------------------------
        # Print Individual Scores
        # ------------------------------------------

        print("\nEvaluation Scores:")

        print(
            "Faithfulness:",
            result["faithfulness"]
        )

        print(
            "Answer Relevancy:",
            result["answer_relevancy"]
        )

        print(
            "Context Precision:",
            result["context_precision"]
        )

        print(
            "Context Recall:",
            result["context_recall"]
        )


    return evaluation_results


# --------------------------------------------------
# STEP 7: Save Evaluation Results
# --------------------------------------------------

def save_evaluation_results(results):

    if not results:
        raise ValueError(
            "No evaluation results available to save."
        )


    dataframe = pd.DataFrame(results)

    output_file = RESULTS_DIR / "ragas_report.csv"


    # Save CSV Report

    dataframe.to_csv(
        output_file,
        index=False
    )


    print("\n" + "=" * 60)

    print(
        "RAGAS Evaluation Completed Successfully!"
    )

    print(
        "Report saved at:",
        output_file
    )


    # ------------------------------------------
    # Calculate Average Scores
    # ------------------------------------------

    metric_columns = [

        "faithfulness",

        "answer_relevancy",

        "context_precision",

        "context_recall"

    ]


    average_scores = dataframe[
        metric_columns
    ].mean()


    print("\nAverage Evaluation Scores:")

    print(average_scores)


# --------------------------------------------------
# STEP 8: Main Execution
# --------------------------------------------------

async def main():

    print("\nCollecting RAG Evaluation Samples...")


    # Step 1: Collect Samples

    evaluation_samples = collect_evaluation_samples()


    print(
        "\nTotal Evaluation Questions:",
        len(evaluation_samples)
    )


    # Step 2: Run RAGAS Evaluation

    print("\nStarting RAGAS Evaluation...")


    results = await evaluate_metrics(
        evaluation_samples
    )


    # Step 3: Save Results

    save_evaluation_results(results)


# --------------------------------------------------
# STEP 9: Application Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    asyncio.run(main())