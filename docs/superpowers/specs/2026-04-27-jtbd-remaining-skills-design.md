# Design Specification: Final JTBD Skills (Forces, Map, Brief)

**Date:** 2026-04-27
**Topic:** Completion of the JTBD Skills Package

## 1. Overview
The goal of this project is to implement the remaining three skills outlined in the `jtbd` repository's `README.md`. These tools take the raw and pattern-matched customer demand evidence and turn it into actionable artifacts for product development.

The three skills are:
*   `/jtbd-forces`: Generates a visual HTML diagram of the four forces.
*   `/jtbd-map`: Synthesizes patterns into a structured Job Map (YAML + Markdown).
*   `/jtbd-brief`: Drafts a JTBD-native product brief from the Job Map data.

## 2. Architecture & Workflow
These skills are designed to chain sequentially from the existing tools (`/jtbd-switch` -> `/jtbd-patterns` -> `/jtbd-forces` -> `/jtbd-map` -> `/jtbd-brief`) or be run standalone with specific input files.

All output artifacts are stored in the git-versioned `.jtbd/` directory.

### 2.1 `/jtbd-forces`
**Purpose:** Create a standalone, shareable visual representation of the four forces (Push, Pull, Anxiety, Habit) driving a switch.

**Input:**
*   Accepts either a single switch file (e.g., `.jtbd/switches/sarah-ops.yml`) OR a pattern file (e.g., `.jtbd/patterns/patterns-2026.yml`).
*   The skill must auto-detect the schema/structure of the input file to determine if it is rendering individual quotes or aggregate pattern summaries.

**Processing:**
*   Parses the input YAML.
*   Extracts the relevant forces (push, pull, anxiety, habit), including verbatim quotes and intensity scores (for individual files) or overarching patterns (for pattern files).
*   Generates a standalone HTML file using embedded CSS for layout (no external dependencies required). The layout should visually oppose Push/Pull against Anxiety/Habit as per Moesta's methodology.

**Output:**
*   A standalone HTML file saved to `.jtbd/forces/[filename-base].html`.

### 2.2 `/jtbd-map`
**Purpose:** Synthesize interview patterns into a structured Job Map that breaks down the customer's exact steps, friction points, and opportunities.

**Input:**
*   Accepts a pattern file (e.g., `.jtbd/patterns/patterns-2026.yml`).
*   If no file is provided, it should default to the most recent pattern file in `.jtbd/patterns/`.

**Processing:**
*   Reads the clustered jobs, emerging signals, and timeline patterns from the input file.
*   Instructs the LLM to deduce the chronological steps of the dominant job identified in the patterns.
*   For each step, identifies the specific friction points and proposes high-level product opportunities.

**Output:**
*   **Data File:** A machine-readable YAML file saved to `.jtbd/jobs/[job-slug].yml`. This must contain a `steps` array with `name`, `friction`, and `opportunity` keys.
*   **Visual File:** A human-readable Markdown rendering saved to `.jtbd/jobs/[job-slug].md`. This file should use Markdown tables to cleanly display the steps, friction, and opportunities.

### 2.3 `/jtbd-brief`
**Purpose:** Translate the structured Job Map data into an actionable Product Brief for engineering and design teams.

**Input:**
*   Accepts a Job Map YAML file (e.g., `.jtbd/jobs/job-01-reliable-numbers.yml`).
*   Optionally reads the parent pattern file to incorporate broader context (timeline patterns, forces).

**Processing:**
*   Instructs the LLM to draft a "JTBD-Native" product brief.
*   The brief must explicitly link proposed features or interventions back to specific customer quotes and the friction points identified in the Job Map.

**Output:**
*   A Markdown document saved to `.jtbd/briefs/[feature-slug].md`.
*   **Structure Requirements:**
    *   **The Job:** What the customer is trying to achieve.
    *   **The Forces:** What is pushing/pulling them, and what anxieties/habits must be overcome.
    *   **Timeline Interventions:** Where in the customer's journey the product should intercept them.
    *   **Map Opportunities:** Specific feature proposals directly linked to the friction points in the Job Map.

## 3. Self-Review & Verification
*   **Placeholders:** None. All file paths and structures are explicitly defined based on the existing `.jtbd/` convention.
*   **Consistency:** The outputs of `jtbd-patterns` feed directly into `jtbd-forces` and `jtbd-map`, and the output of `jtbd-map` feeds directly into `jtbd-brief`.
*   **Scope:** This spec is tightly scoped to adding three CLI commands (skills) to the existing repository.

## 4. Next Steps
Once approved, transition to the `writing-plans` skill to generate the implementation plan.
