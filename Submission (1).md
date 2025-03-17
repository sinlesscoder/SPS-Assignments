<center>

## Assignment 5

---
Ali Ahmed
<br />
03-16-2025

</center>

<br />

In this report, I will demonstrate how to prepare inventory data for analysis by formatting it into four different formats:

1. JSON
2. HTML
3. XML
4. Parquet 

Each section includes R code for generating and importing the data, along with a discussion of the Pros and Cons of each format.

### Data Source

The inventory data is sourced from a CSV file located at the following:

```r
url <- "c:\Users\Ali\Documents\R-documents\data607.csv"
```

I begin by reading the CSV file into an R dataframe:

```r
# Load necessary library
library(readr)

# Read the CSV file into a dataframe
data <- read_csv(url)
```


### JSON Format

- JavaScript Object Notation (JSON) is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate.

#### Exporting Data to JSON

```r
# Load necessary library
library(jsonlite)

# Convert dataframe to JSON
json_data <- toJSON(data, pretty = TRUE)

# Write JSON to file
writeLines(json_data, "data.json")

Importing Data from JSON

# Read JSON from file
imported_json_data <- fromJSON("data.json")
```

#### Pros and Cons of JSON

- Pros:
	- Human-readable: JSON’s text-based format is easy to read and understand.
	- Widely used in web applications: JSON is a standard format for data interchange in web development.
	- Language-independent: JSON is supported by most programming languages, making it versatile for data exchange.

- Cons:
	- Larger file size: JSON files can be larger compared to binary formats like Parquet, leading to increased storage requirements.
	- Slower parsing: Parsing JSON can be slower compared to binary formats, which may affect performance with large datasets.

### HTML Format

- HyperText Markup Language (HTML) is the standard language for creating web pages. Representing data in HTML allows for easy visualization in web browsers.

#### Exporting Data to HTML

```r
# Load necessary library
library(xtable)

# Convert dataframe to HTML
html_table <- print(xtable(data), type = "html", include.rownames = FALSE)

# Write HTML to file
writeLines(html_table, "data.html")
```

#### Pros and Cons of HTML

- Pros:
	- Easy visualization: HTML tables can be directly rendered in web browsers, facilitating data presentation.
	- Formatting capabilities: HTML allows for rich formatting options, enhancing the readability of data.

- Cons:
	- Not optimized for data storage: HTML is primarily designed for web content, not for efficient data storage or analysis.
	- Parsing complexity: Extracting data from HTML can be more complex compared to other formats.

### XML Format

- eXtensible Markup Language (XML) is a markup language that defines rules for encoding documents in a format that is both human-readable and machine-readable.

#### Exporting Data to XML

```r
# Load necessary library
library(XML)

# Function to convert dataframe to XML
df_to_xml <- function(df) {
  # Create root node
  root <- newXMLNode("data")
  
  # Add each row as a child node
  for (i in 1:nrow(df)) {
    row_node <- newXMLNode("row", parent = root)
    for (col in names(df)) {
      newXMLNode(col, df[i, col], parent = row_node)
    }
  }
  
  return(root)
}

# Convert dataframe to XML
xml_data <- df_to_xml(data)

# Save XML to file
saveXML(xml_data, file = "data.xml")
```

#### Pros and Cons of XML

- Pros:
	- Self-descriptive: XML tags provide metadata about the data, making it self-descriptive.
	- Extensible: XML allows for custom tags, providing flexibility in data representation.
	- Widely used in enterprise systems: XML is commonly used in various enterprise applications for data interchange.

- Cons:
	- Verbose: XML’s tag-based structure can lead to large file sizes.
	- Complex parsing: Parsing XML can be resource-intensive and complex compared to other formats.

### Parquet Format

- Parquet is a columnar storage file format optimized for use with big data processing frameworks. It is efficient in terms of storage and performance.

#### Exporting Data to Parquet

```r
# Load necessary library
library(arrow)

# Write dataframe to Parquet file
write_parquet(data, "data.parquet")

Importing Data from Parquet

# Load necessary library
library(arrow)

# Read Parquet file into dataframe
imported_parquet_data <- read_parquet("data.parquet")
```

#### Pros and Cons of Parquet

- Pros:
    - Efficient storage: Parquet’s columnar format leads to highly efficient data compression and encoding schemes.
    - Optimized for analytical queries: Columnar storage is ideal for analytical operations, allowing for faster query performance.
    - Schema evolution: Parquet supports schema evolution, enabling changes to the data structure over time without breaking compatibility.

- Cons:
	- Not human-readable: Parquet files are in a binary format, making them unsuitable for manual inspection.
	- Limited support in some tools: While support for Parquet is growing, some tools and environments may not natively support this format.

### Conclusion

Each data format has its own strengths and weaknesses. The choice of format depends on the specific requirements of the analysis, the tools being used, and considerations such as file size, readability, and performance. 

- JSON and XML are suitable for data interchange between systems with JSON being more lightweight. 
- HTML is ideal for presenting data in a human-readable form on the web. 
- Parquet is highly efficient for storage and analytical querying, especially with large datasets.

### Full R Code

```r
library("XML")
library("arrow")
library("jsonlite")
library("xtable")

# Get the URL

url <- "c:/Users/Ali/Documents/R-documents/data607.csv"

file_path <- "data/assignments/assignment_five/assignment.csv"

data <- read.csv(file_path)

print(head(data))

column_names <- colnames(data)

print(column_names)

# Logic to go from DataFrame to XML
# Function to convert DataFrame to XML
df_to_xml <- function(df) {
  # Create root node
  root <- newXMLNode("data")
  
  # Add each row as a child node
  for (i in 1:length(df$index)) {
    row_node <- newXMLNode("row", parent = root)
    for (col in names(df)) {
      newXMLNode(col, df[i, col], parent = row_node)
    }
  }
  
  return(root)
}

# Convert DataFrame to XML
xml_data <- df_to_xml(data)

file_path <- "data.xml"

# Save XML to file
saveXML(xml_data, file = file_path)

file_path <- "data.parquet"

write_parquet(data, file_path)

file_path <- "data.json"

# Write to JSON
# Convert DataFrame to JSON
json_data <- toJSON(data, pretty = TRUE)

# Write JSON to file
writeLines(json_data, file_path)

# Write to HTML file

# Convert DataFrame to HTML
html_table <- print(xtable(data), type = "html", include.rownames = FALSE)

file_path <- "data.html"

# Write HTML to file
writeLines(html_table, "output_table.html")
```
