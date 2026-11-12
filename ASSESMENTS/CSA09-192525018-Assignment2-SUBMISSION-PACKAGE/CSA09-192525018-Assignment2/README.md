# Programming in Java – Assignment 2 (CO2)

**Register Number:** 192525018  
**Repository name:** `CSA09-192525018-Assignment2`  
**Java version:** Use the JDK installed on your computer (Java 17 is recommended).

This repository is a starter implementation for Q1–Q7 of the supplied Assignment 2 PDF. It contains Java examples, benchmark scaffolding, and evidence templates. **Run every program yourself and replace all `PENDING` measurements with your actual results. Do not submit predicted or fabricated measurements as actual evidence.**

## Folder structure

- `Q1_StringComparison/` – String, StringBuilder and StringBuffer workloads
- `Q2_ListComparison/` – ArrayList, LinkedList and ArrayDeque comparison
- `Q3_HashSetContract/` – equals/hashCode and HashSet de-duplication
- `Q4_MapComparison/` – HashMap, TreeMap and LinkedHashMap
- `Q5_GenericLeaderboard/` – generic leaderboard and comparator
- `Q6_HospitalTriage/` – severity and arrival-order priority queue
- `Q7_DesignChallenge/` – original and redesigned inventory lookup
- `ExperimentalData/` – CSV templates for actual measurements
- `Screenshots/` – add screenshots of your own program executions
- `Report/` – add the final assignment report

## Check Java installation

Open Command Prompt or Terminal and run:

```bash
java -version
javac -version
```

If `javac` is not recognised, install a JDK and configure `JAVA_HOME`/PATH.

## Compile and run

Open a terminal in the relevant question folder. For a single source file:

```bash
javac FileName.java
java ClassName
```

For example:

```bash
cd Q3_HashSetContract
javac Attendance.java
java Attendance
```

## Suggested Git workflow

Create a GitHub repository named `CSA09-192525018-Assignment2`, then:

```bash
git init
git add .
git commit -m "Add assignment 2 project structure"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CSA09-192525018-Assignment2.git
git push -u origin main
```

Commit progressively, at least once for each question, as required by the assignment.

## Evidence checklist

- [ ] Q1: execute three approaches over three workloads; record repeated averages.
- [ ] Q2: compare list operations at three playlist sizes.
- [ ] Q3: run the incomplete/broken demonstration if required by your instructor, then run the corrected implementation.
- [ ] Q4: test three inventory sizes, 100,000 lookups, and both report orders.
- [ ] Q5: run ranking examples and additional comparator tests.
- [ ] Q6: test approximately eight patients and multiple queue sizes.
- [ ] Q7: compare original and redesigned implementations under identical conditions.
- [ ] Add genuine screenshots and actual CSV measurements.
- [ ] Add your completed report in `Report/`.

The included code is a learning baseline, not proof of execution. Review it, run it, understand it, and adapt it to the exact assignment instructions.


## GitHub Repository URL

Create the required repository `CSA09-192525018-Assignment2` under your GitHub account, then replace this line with its actual URL. Do not submit with a placeholder URL.
