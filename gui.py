import streamlit as st
import os
import json
import io
import pandas as pd

from contextlib import redirect_stdout

# ==========================================
# CONTEXT BUILDER
# ==========================================

from context_builder.context_builder import (
    build_context
)

# ==========================================
# ANALYSIS NODE
# ==========================================

from analysis_node.runner import (
    run_analysis
)

# ==========================================
# ANALYSIS REVIEW NODE
# ==========================================

from analysis_review_node.review_runner import (
    run_analysis_review
)

# ==========================================
# REMEDIATION NODE
# ==========================================

from remediation_node.remediation_node_runner import (
    run_remediation
)

# ==========================================
# ACCURACY VALIDATION NODE
# ==========================================

from accuracy_validation_node.runner import (
    run_accuracy_validation
)

# ==========================================
# COMPILER NODE
# ==========================================

from compiler_node.compiler_runner import (
    run_compiler
)

# ==========================================
# RETRY NODE
# ==========================================

from retry_compilation_node.retry_runner import (
    run_retry_node
)

# ==========================================
# REVIEW NODE
# ==========================================

from review_node.review_runner import (
    run_review
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="STM32 GenAI Analyzer",

    layout="wide"

)

st.title(
    "STM32 GenAI Analyzer"
)

# ==========================================
# USER INPUTS
# ==========================================

api_key = st.text_input(

    "OpenAI API Key",

    type="password"

)

model = st.selectbox(

    "Model",

    [

        "gpt-4.1",

        "gpt-4o"

    ]

)

temperature = st.slider(

    "Temperature",

    min_value=0.0,

    max_value=1.0,

    value=0.2,

    step=0.1

)

project_path = st.text_input(

    "STM32 Project Location"

)

guidelines = st.file_uploader(

    "Upload Coding Guidelines",

    type=["json"]

)

# ======================================================
# STEP 1 : CONTEXT BUILDER
# ======================================================

st.markdown("---")

st.subheader(
    "Step 1 : Context Builder"
)

if st.button(
    "Generate Context"
):

    if project_path.strip() == "":

        st.error(
            "Please enter STM32 project location."
        )

        st.stop()

    if not os.path.exists(
        project_path
    ):

        st.error(
            "STM32 project path not found."
        )

        st.stop()

    try:

        output_container = st.empty()

        buffer = io.StringIO()

        with redirect_stdout(
            buffer
        ):

            context = build_context(
                project_path
            )

            with open(
                "context.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    context,
                    f,
                    indent=4
                )

            print(
                "Context Generated Successfully"
            )

            print(
                "Output : context.json"
            )

        output_container.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Context Generated Successfully"
        )

        st.download_button(

            label="Download context.json",

            data=json.dumps(

                context,

                indent=4

            ),

            file_name="context.json",

            mime="application/json"

        )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 2 : ANALYSIS NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 2 : Analysis Node"
)

if st.button(
    "Run Analysis"
):

    if not api_key.strip():

        st.error(
            "Please enter OpenAI API Key."
        )

        st.stop()

    if guidelines is None:

        st.error(
            "Please upload Coding Guidelines."
        )

        st.stop()

    try:

        coding_guidelines = json.load(
            guidelines
        )

    except Exception:

        st.error(
            "Invalid Coding Guidelines JSON."
        )

        st.stop()

    if not os.path.exists(
        "context.json"
    ):

        st.error(
            "Generate Context first."
        )

        st.stop()

    with open(
        "context.json",
        "r",
        encoding="utf-8"
    ) as f:

        project_context = json.load(
            f
        )

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            analysis_report = run_analysis(

                api_key=api_key,

                model=model,

                temperature=temperature,

                project_root=project_path,

                project_context=project_context,

                coding_guidelines=coding_guidelines

            )

        st.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Analysis Completed Successfully."
        )

        # ==========================================
        # Store in Session
        # ==========================================

        st.session_state["project_context"] = (
            project_context
        )

        st.session_state["coding_guidelines"] = (
            coding_guidelines
        )

        st.session_state["analysis_report"] = (
            analysis_report
        )

        st.session_state["analysis_report_path"] = (
            os.path.join(
                "analysis_reports",
                "final_analysis_report.json"
            )
        )

        st.session_state["project_root"] = (
            project_path
        )

        # ==========================================
        # Summary
        # ==========================================

        summary = analysis_report["summary"]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Files",
                summary["total_files"]
            )

        with col2:

            st.metric(
                "Functions",
                summary["total_functions"]
            )

        with col3:

            st.metric(
                "Issues",
                summary["total_issues"]
            )

        st.subheader(
            "Analysis Summary"
        )

        st.json(
            summary
        )

        report_path = st.session_state[
            "analysis_report_path"
        ]

        if os.path.exists(
            report_path
        ):

            with open(
                report_path,
                "r",
                encoding="utf-8"
            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Analysis Report",

                data=report_data,

                file_name="final_analysis_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 3 : ANALYSIS REVIEW NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 3 : Analysis Review Node"
)

if st.button(
    "Run Analysis Review"
):

    # ----------------------------------
    # Validation
    # ----------------------------------

    if not api_key.strip():

        st.error(
            "Please enter OpenAI API Key."
        )

        st.stop()

    if "project_context" not in st.session_state:

        st.error(
            "Run Analysis first."
        )

        st.stop()

    if "coding_guidelines" not in st.session_state:

        st.error(
            "Run Analysis first."
        )

        st.stop()

    if "project_root" not in st.session_state:

        st.error(
            "Run Analysis first."
        )

        st.stop()

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            review_report = run_analysis_review(

                api_key=api_key,

                model=model,

                temperature=temperature,

                project_root=st.session_state[
                    "project_root"
                ],

                project_context=st.session_state[
                    "project_context"
                ],

                coding_guidelines=st.session_state[
                    "coding_guidelines"
                ]

            )

        st.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Analysis Review Completed Successfully."
        )

        # ----------------------------------
        # Store Results
        # ----------------------------------

        st.session_state[
            "analysis_review_report"
        ] = review_report

        st.session_state[
            "analysis_review_report_path"
        ] = os.path.join(

            "analysis_review_reports",

            "analysis_review_report.json"

        )
        # ----------------------------------
        # Display Summary
        # ----------------------------------

        summary = review_report.get(
            "summary",
            {}
        )

        metrics = review_report.get(
            "metrics",
            {}
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Initial Issues",

                summary.get(
                    "initial_analysis_issues",
                    0
                )

            )

        with col2:

            st.metric(

                "Additional Issues",

                summary.get(
                    "new_issues",
                    0
                )

            )

        with col3:

            st.metric(

                "Coverage %",

                metrics.get(
                    "coverage_percent",
                    0
                )

            )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Final Issues",

                summary.get(
                    "second_analysis_issues",
                    0
                )

            )

        with col2:

            st.metric(

                "Assessment",

                review_report.get(
                    "assessment",
                    "-"
                )

            )

        st.subheader(
            "Analysis Review Summary"
        )

        st.json(
            review_report
        )

        # ----------------------------------
        # Download Report
        # ----------------------------------

        report_path = os.path.join(

            "analysis_review_reports",

            "analysis_review_report.json"

        )

        if os.path.exists(
            report_path
        ):

            with open(

                report_path,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Analysis Review Report",

                data=report_data,

                file_name="analysis_review_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 4 : REMEDIATION NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 4 : Remediation Node"
)

if st.button(
    "Run Remediation"
):

    if not api_key.strip():

        st.error(
            "Please enter OpenAI API Key."
        )

        st.stop()

    if "analysis_report_path" not in st.session_state:

        st.error(
            "Run Analysis first."
        )

        st.stop()

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            remediation_result = run_remediation(

                api_key=api_key,

                model=model,

                temperature=temperature,

                workspace_root=project_path,

                analysis_report_path=st.session_state[
                    "analysis_report_path"
                ]

            )

        st.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Remediation Completed Successfully."
        )

        # ==========================================
        # Store Results In Session
        # ==========================================

        st.session_state[
            "remediation_report"
        ] = remediation_result

        st.session_state[
            "remediation_report_path"
        ] = os.path.join(

            "remediation_reports",

            "remediation_report.json"

        )

        st.session_state[
            "remediated_project_root"
        ] = os.path.join(

            project_path,

            "workspace",

            "remediated_project"

        )

        # ==========================================
        # Display Summary
        # ==========================================

        if isinstance(
            remediation_result,
            dict
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Files Processed",

                    remediation_result.get(

                        "files_processed",

                        "-"

                    )

                )

            with col2:

                st.metric(

                    "Functions Updated",

                    remediation_result.get(

                        "functions_updated",

                        "-"

                    )

                )

            with col3:

                st.metric(

                    "Issues Fixed",

                    remediation_result.get(

                        "issues_fixed",

                        "-"

                    )

                )

            st.subheader(
                "Remediation Summary"
            )

            st.json(
                remediation_result
            )

        remediation_report = os.path.join(

            "remediation_reports",

            "remediation_report.json"

        )

        if os.path.exists(
            remediation_report
        ):

            with open(

                remediation_report,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Remediation Report",

                data=report_data,

                file_name="remediation_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
        # ----------------------------------
        # Display Summary
        # ----------------------------------

        summary = accuracy_report.get(
            "summary",
            {}
        )

        metrics = accuracy_report.get(
            "metrics",
            {}
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Implemented",

                summary.get(
                    "implemented",
                    0
                )

            )

        with col2:

            st.metric(

                "Partial",

                summary.get(
                    "partially_implemented",
                    0
                )

            )

        with col3:

            st.metric(

                "Not Implemented",

                summary.get(
                    "not_implemented",
                    0
                )

            )

        with col4:

            st.metric(

                "Accuracy %",

                metrics.get(
                    "accuracy_percent",
                    0
                )

            )

        st.markdown("---")

        st.subheader(
            "Accuracy Summary"
        )

        st.json(
            summary
        )

        # ----------------------------------
        # Validation Results
        # ----------------------------------

        validation_results = accuracy_report.get(
            "validation_results",
            []
        )

        if validation_results:

            st.subheader(
                "Validation Results"
            )

            table = []

            for result in validation_results:

                table.append(

                    {

                        "File":
                            result["file"],

                        "Function":
                            result["function"],

                        "Rule":
                            result["rule_id"],

                        "Status":
                            result["status"]

                    }

                )

            st.dataframe(

                pd.DataFrame(
                    table
                ),

                use_container_width=True

            )

        # ----------------------------------
        # Download Accuracy Report
        # ----------------------------------

        report_path = os.path.join(

            "accuracy_reports",

            "accuracy_report.json"

        )

        if os.path.exists(
            report_path
        ):

            with open(

                report_path,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Accuracy Report",

                data=report_data,

                file_name="accuracy_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 6 : COMPILER NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 6 : Compiler Node"
)

if st.button(
    "Run Compiler"
):

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            compile_report = run_compiler()

        st.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Compilation Completed."
        )

        # ==========================================
        # Store Results In Session
        # ==========================================

        st.session_state[
            "compile_report"
        ] = compile_report

        st.session_state[
            "compile_report_path"
        ] = os.path.join(

            "compile_reports",

            "compile_report.json"

        )

        # ==========================================
        # Metrics
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Build Status",

                compile_report.get(

                    "build_status",

                    "-"

                )

            )

        with col2:

            st.metric(

                "Compiler Errors",

                compile_report.get(

                    "error_count",

                    0

                )

            )

        with col3:

            st.metric(

                "Compiler Warnings",

                compile_report.get(

                    "warning_count",

                    0

                )

            )

        st.subheader(
            "Compiler Summary"
        )

        st.json(
            compile_report
        )

        compile_report_path = os.path.join(

            "compile_reports",

            "compile_report.json"

        )

        if os.path.exists(
            compile_report_path
        ):

            with open(

                compile_report_path,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Compile Report",

                data=report_data,

                file_name="compile_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 7 : RETRY COMPILATION NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 7 : Retry Compilation Node"
)

if st.button(
    "Run Retry Compilation"
):

    if not api_key.strip():

        st.error(
            "Please enter OpenAI API Key."
        )

        st.stop()

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            retry_report = run_retry_node(
                api_key=api_key,
                model=model
            )

        st.code(
            buffer.getvalue(),
            language="text"
        )

        st.success(
            "Retry Compilation Completed."
        )

        # ==========================================
        # Store Results In Session
        # ==========================================

        st.session_state[
            "retry_report"
        ] = retry_report

        st.session_state[
            "retry_report_path"
        ] = os.path.join(

            "retry_reports",

            "retry_report.json"

        )

        # ==========================================
        # Metrics
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Files Identified",

                retry_report.get(
                    "files_identified",
                    0
                )

            )

        with col2:

            st.metric(

                "Files Fixed",

                retry_report.get(
                    "files_fixed",
                    0
                )

            )

        with col3:

            st.metric(

                "Files Failed",

                retry_report.get(
                    "files_failed",
                    0
                )

            )

        st.subheader(
            "Retry Summary"
        )

        summary = {

            "Build Status":
                retry_report.get(
                    "build_status"
                ),

            "Compiler Errors":
                retry_report.get(
                    "error_count"
                ),

            "Compiler Warnings":
                retry_report.get(
                    "warning_count"
                ),

            "Files Identified":
                retry_report.get(
                    "files_identified"
                ),

            "Files Fixed":
                retry_report.get(
                    "files_fixed"
                ),

            "Files Failed":
                retry_report.get(
                    "files_failed"
                )
        }

        st.json(
            summary
        )

        # ==========================================
        # Processed Files
        # ==========================================

        retry_tasks = retry_report.get(
            "retry_tasks",
            []
        )

        if retry_tasks:

            st.subheader(
                "Processed Files"
            )

            table = []

            for task in retry_tasks:

                table.append(

                    {

                        "File":
                            task["file"],

                        "Errors":
                            task["error_count"],

                        "Path":
                            task["actual_path"]

                    }

                )

            st.dataframe(

                pd.DataFrame(table),

                use_container_width=True

            )

        # ==========================================
        # Download Retry Report
        # ==========================================

        retry_report_path = os.path.join(

            "retry_reports",

            "retry_report.json"

        )

        if os.path.exists(
            retry_report_path
        ):

            with open(

                retry_report_path,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Retry Report",

                data=report_data,

                file_name="retry_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )
# ======================================================
# STEP 8 : REVIEW NODE
# ======================================================

st.markdown("---")

st.subheader(
    "Step 8 : Review Node"
)

if st.button(
    "Run Review"
):

    # ==========================================
    # Verify Required Reports
    # ==========================================

    required_reports = [

        "analysis_reports/final_analysis_report.json",

        "analysis_review_reports/analysis_review_report.json",

        "accuracy_reports/accuracy_report.json",

        "compile_reports/compile_report.json",

        "retry_reports/retry_report.json"

    ]

    missing_reports = [

        report

        for report in required_reports

        if not os.path.exists(report)

    ]

    if len(missing_reports) > 0:

        st.error(
            "The following reports are missing:"
        )

        for report in missing_reports:

            st.write(report)

        st.stop()

    buffer = io.StringIO()

    try:

        with redirect_stdout(
            buffer
        ):

            review_report = run_review()

        st.code(

            buffer.getvalue(),

            language="text"

        )

        st.success(
            "Review Report Generated Successfully."
        )

        # ==========================================
        # Store Report
        # ==========================================

        st.session_state[
            "review_report"
        ] = review_report

        st.session_state[
            "review_report_path"
        ] = os.path.join(

            "review_reports",

            "review_report.json"

        )

        # ==========================================
        # Extract Values
        # ==========================================

        summary = review_report.get(

            "summary",

            {}

        )

        metrics = review_report.get(

            "metrics",

            {}

        )

        retry_summary = review_report.get(

            "retry_summary",

            {}

        )

        total_files = summary.get(

            "total_files",

            0

        )

        total_functions = summary.get(

            "total_functions",

            0

        )

        total_issues = summary.get(

            "total_issues_found",

            0

        )

        coverage = metrics.get(

            "coverage_percent",

            0

        )

        accuracy = metrics.get(

            "accuracy_percent",

            0

        )

        build_status = summary.get(

            "build_status",

            "UNKNOWN"

        )

        compiler_errors = summary.get(

            "compiler_errors",

            0

        )

        files_fixed = retry_summary.get(

            "files_fixed",

            0

        )

        files_failed = retry_summary.get(

            "files_failed",

            0

        )

        final_assessment = review_report.get(

            "final_assessment",

            "UNKNOWN"

        )
        # ==========================================
        # Project Overview
        # ==========================================

        st.subheader(
            "Project Overview"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Files",
                total_files
            )

        with col2:

            st.metric(
                "Functions",
                total_functions
            )

        with col3:

            st.metric(
                "Issues Found",
                total_issues
            )

        st.markdown("---")

        # ==========================================
        # Coverage / Accuracy / Build
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Coverage %",
                f"{coverage}%"
            )

        with col2:

            st.metric(
                "Accuracy %",
                f"{accuracy}%"
            )

        with col3:

            st.metric(
                "Build Status",
                build_status
            )

        st.markdown("---")

        # ==========================================
        # Retry Summary
        # ==========================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Files Fixed",
                files_fixed
            )

        with col2:

            st.metric(
                "Files Failed",
                files_failed
            )

        with col3:

            st.metric(
                "Compiler Errors",
                compiler_errors
            )

        st.markdown("---")

        # ==========================================
        # Final Assessment
        # ==========================================

        st.subheader(
            "Overall Assessment"
        )

        if final_assessment == "SUCCESS":

            st.success(
                final_assessment
            )

        elif final_assessment == "PARTIALLY SUCCESSFUL":

            st.warning(
                final_assessment
            )

        else:

            st.error(
                final_assessment
            )

        st.markdown("---")

        # ==========================================
        # Complete Review Report
        # ==========================================

        with st.expander(
            "View Complete Review Report"
        ):

            st.json(
                review_report
            )

        # ==========================================
        # Download Review Report
        # ==========================================

        review_report_path = os.path.join(

            "review_reports",

            "review_report.json"

        )

        if os.path.exists(
            review_report_path
        ):

            with open(

                review_report_path,

                "r",

                encoding="utf-8"

            ) as f:

                report_data = f.read()

            st.download_button(

                label="Download Review Report",

                data=report_data,

                file_name="review_report.json",

                mime="application/json"

            )

    except Exception as e:

        st.error(
            str(e)
        )