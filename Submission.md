<center>

# Assignment 3 Submission

Ali Ahmed
<br />
February 16, 2025

</center>

## Question 1

### Table Creation and Normal Forms in R DataFrames

#### 1NF (First Normal Form) - `table_1nf`

The `table_1nf` DataFrame represents the initial table in First Normal Form (1NF). It was created with synthetic records using the following criteria:

1. Each column contains single values (atomic).
2. There are no repeating groups.
3. Each row is unique, identified by a combination of StudentID and CourseID.

```r
table_1nf <- data.frame(
  StudentID = c(1, 1, 2, 3, 3),
  CourseID = c(101, 102, 101, 102, 103),
  CourseName = c("Math", "Physics", "Math", "Physics", "Chemistry"),
  Instructor = c("Dr. Smith", "Dr. Johnson", "Dr. Smith", "Dr. Johnson", "Dr. Brown"),
  Grade = c(85, 92, 78, 95, 88)
)
```

#### 2NF (Second Normal Form) - `table_2nf_students` and `table_2nf_courses`

To achieve 2NF, the original table was separated into two DataFrames to separate student-specific and course-specific information:

```r
table_2nf_students <- data.frame(
  StudentID = c(1, 2, 3),
  Grade = c(85, 78, 95)
)

table_2nf_courses <- data.frame(
  CourseID = c(101, 102, 103),
  CourseName = c("Math", "Physics", "Chemistry"),
  Instructor = c("Dr. Smith", "Dr. Johnson", "Dr. Brown")
)
```

These tables are in 2NF because:
- They meet all 1NF requirements.
- All non-key attributes are fully functionally dependent on the primary key of each respective table.
    - `table_2nf_students` contains student-specific information.
    - `table_2nf_courses` contains course-specific information.

#### 3NF (Third Normal Form)

- **Tables**:
    - `table_3nf_students` 
    - `table_3nf_courses`
    - `table_3nf_instructors`

To achieve 3NF, further normalization was applied to the tables currently in 2NF:

```r
table_3nf_students <- table_2nf_students

table_3nf_courses <- data.frame(
  CourseID = c(101, 102, 103),
  CourseName = c("Math", "Physics", "Chemistry"),
  InstructorID = c(1, 2, 3)
)

table_3nf_instructors <- data.frame(
  InstructorID = c(1, 2, 3),
  Instructor = c("Dr. Smith", "Dr. Johnson", "Dr. Brown")
)
```

These tables are in 3NF because:
- They meet all 2NF requirements.
- There are no transitive dependencies between non-key attributes.
- `table_3nf_students` remains unchanged from 2NF.
- `table_3nf_courses` now references instructors using InstructorID.
- `table_3nf_instructors` contains instructor-specific information.

By structuring the data in this way, data redundancy is eliminated and there is improved data integrity across the tables.

### Question 2

The R code for identifying the majors that have either `DATA` or `STATISTICS` in their names is shown below:

```r
# Read CSV data into a R DataFrame
df <- read.csv("https://raw.githubusercontent.com/fivethirtyeight/data/refs/heads/master/college-majors/majors-list.csv")

# Filter the DataFrame to either have major that contain DATA or STATISTICS 
## in the name - column name is Major
filtered_df <- df[grep("DATA|STATISTICS", df$Major), ]

# View the records from the DataFrame that contain the DATA or STATISTICS majors
print(filtered_df)
```

### Question 3

- `(.)\1\1`

The regular expression above would match any single character as long as that character is repeating two more times. In total, the character shows up three times.

#### Examples:

- `aaa`
    - `a` repeats twice after the first `a`.
- `111`
    - `1` repeats twice after the first `1`.

---

- `(.)(.)\\2\\1`

The expression above has extra `\` so the way it is written would lead to a typo. The correct way to write it would be `(.)(.)\2\1`. This expression would match any two characters as long as the second character is repeating after the first character.

#### Examples:

- `abba`
    - `a` and `b` are the two characters and `b` repeats after `a`.
- `1221`
    - `1` and `2` are the two characters and `2` repeats after `1`.

---

- `(..)\1`

The expression above matches a pair of characters that repeat.

#### Examples:

- `abab`
    - `ab` repeats.
- `1212`
    - `12` repeats.

---

- `(.).\\1.\\1`

The expression above has extra `\` after the `.` characters not surrounded by `()` so the way it is written would lead to a typo. The correct way to write it would be `(.).\1.\1`. This expression would match any single character as long as that character is repeating two more times im between two other characters. In total, the character shows up three times.

#### Examples:

- `abaca`
    - `a` shows up three times total in between two other characters.
- `12131`
    - `1` shows up three times total in between two other characters.

---

- `(.)(.)(.).*\\3\\2\\1`

The expression above has extra `\` after the `.*` characters not surrounded by `()` so the way it is written would lead to a typo. The correct way to write it would be `(.)(.)(.).*\3\2\1`. This expression would match any three characters as long as they are repeated in the reverse order at the end of the string.

#### Examples:

- `abccba`
    - `abc` is repeated in reverse order at the end of the string.
- `123321`
    - `123` is repeated in reverse order at the end of the string.
- `abcddddddddddcba`
    - `abc` is repeated in reverse order at the end of the string.

### Question 4

- Expression that starts and ends with the same character.

    - `(.).*\1`

---

- Expression that contains a repeated pair of letters (e.g. "church" contains "ch" repeated twice).

    - `(..).*\1`

---

- Expression in which one character is repeated in at least three places (e.g. "eleven" contains three "e"'s)

    - `(.).*\1.*\1`