# Markdown Lecture Notes

## Overview
This repository provides a **React-TypeScript framework** for dynamically rendering lecture notes using **Markdown (MDX)** with mathematical support. It is designed to facilitate structured and interactive learning experiences in subjects like **Mathematics, Logic, and Computer Science**.

## Directory Structure
Each lecture note is organized hierarchically within categories and subcategories.

```
📂 markdown_api/
 ├── 📂 mathematics/
 │   ├── 📂 set_theory/
 │   │   ├── 📝 note.mdx
 │   │   ├── 📄 meta.json
 │   ├── 📂 binary_operations/
 │   │   ├── 📝 note.mdx
 │   │   ├── 📄 meta.json
 ├── 📂 logic/
 │   ├── 📂 propositional_logic/
 │   │   ├── 📝 note.mdx
 │   │   ├── 📄 meta.json
 │   ├── 📂 predicate_logic/
 │   │   ├── 📝 note.mdx
 │   │   ├── 📄 meta.json
```

## File Descriptions
### `note.mdx`
- Contains the **Markdown (MDX)** content for the lecture note.
- Supports **dynamic content**, **LaTeX math rendering**, and **React components**.
- Example:

```mdx
# Introduction to Set Theory

Mathematics is built upon **sets**. A set is a well-defined collection of objects.

$$ A = \{1,2,3,4\} $$
```

### `meta.json`
- Stores metadata for the lecture note.
- Defines **objectives**, **prerequisites**, and other metadata.
- Example:

```json
{
  "title": "Introduction to Set Theory",
  "category": "mathematics",
  "subcategory": "set_theory",
  "prerequisites": ["Basic Algebra"],
  "objectives": [
    "Understand the concept of sets",
    "Learn set notation and operations"
  ]
}
```



## License
This project is licensed under the **MIT License**.

---
🚀 **Abstract Classroom - Enhancing Math & CS Education with Markdown & React**

